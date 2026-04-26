# DEPLOYMENT A HOSTINGER
**Proyecto:** Tienda.APPLE.PS5
**Objetivo:** Desplegar el MVP (Frontend Estático + API FastAPI) en un subdominio de Hostinger (`research.geeksoft.tech`).

Esta guía documenta al detalle y paso a paso el proceso de despliegue exitoso realizado para conectar Nginx y FastAPI (Uvicorn) en el VPS, evitando los bloqueos de CORS y enrutamiento.

---

## 1. Infraestructura Base
- **VPS IP:** `91.108.125.253`
- **Subdominio DNS:** `research.geeksoft.tech` (Registro A apuntando a la IP del VPS).
- **Directorio Raíz VPS:** `/var/www/html/research`

## 2. Transferencia de Archivos (SFTP)
Dado que el VPS no se pudo autenticar para clonar el repositorio privado desde GitHub, el código fue transferido directamente desde el entorno local al VPS utilizando **SFTP** (vía Paramiko con Python), creando la copia del proyecto en `/var/www/html/research`.

## 3. Configuración del Backend (FastAPI + Uvicorn)

### A. Preparación del Entorno Virtual y Dependencias
Dentro del VPS, se ejecutaron los siguientes comandos para crear un entorno aislado seguro e instalar las herramientas de scraping (Playwright):
```bash
cd /var/www/html/research
apt update
apt install -y python3-venv
python3 -m venv venv
source venv/bin/activate

# Instalación de paquetes
pip install fastapi uvicorn supabase python-dotenv playwright

# Instalación de navegadores Chromium para scraping Headless
playwright install chromium
playwright install-deps chromium
```

### B. Credenciales (.env de Supabase)
El archivo `.env` se creó manualmente en el servidor, depositando las llaves del proyecto activo para evitar el error de "Schema cache" o "Table not found":
```bash
cat << 'EOF' > /var/www/html/research/backend/.env
SUPABASE_URL="https://kqorhlowmvroxalcrzqa.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
EOF
```

### C. Persistencia con Systemd (research_api.service)
Para garantizar que la API siempre esté viva y se reinicie en caso de falla, se creó un demonio en Linux:
1. Crear el archivo: `nano /etc/systemd/system/research_api.service`
2. Insertar configuración:
```ini
[Unit]
Description=Gunicorn instance to serve Research FastAPI Backend
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/html/research/backend
Environment="PATH=/var/www/html/research/venv/bin"
ExecStart=/var/www/html/research/venv/bin/uvicorn api_market:app --host 127.0.0.1 --port 8000

[Install]
WantedBy=multi-user.target
```
3. Activar el servicio:
```bash
systemctl daemon-reload
systemctl enable research_api
systemctl start research_api
```

## 4. Configuración del Proxy Inverso (Nginx)

### A. Archivo de Configuración de Host
Se creó el bloque de servidor en Nginx para recibir tráfico en `$host` (`research.geeksoft.tech`) y distribuirlo: los estáticos por defecto (Frontend) y `/api/` hacia el servicio Uvicorn local.

Ruta: `/etc/nginx/sites-available/research.conf`
```nginx
server {
    listen 80;
    server_name research.geeksoft.tech;
    
    root /var/www/html/research/frontend;
    index index.html;

    # Resolver las rutas del frontend
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy inverso hacia FastAPI
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Reescribe /api/algo a /algo borrando el slash extra
        # CRÍTICO: Previene el error de "Not Found" y problemas de CORS en FastAPI
        rewrite ^/api/(.*)$ /$1 break;
    }
}
```

### B. Activación de Nginx
```bash
ln -sf /etc/nginx/sites-available/research.conf /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

## 5. FrontEnd: Ajuste de URL y Conexión Final
Una vez que el backend y Nginx estuvieron funcionales, modificamos el archivo `app.js` localmente para definir la variable de producción `API_URL`:
```javascript
// Configuración Base de Producción
const API_URL = "http://research.geeksoft.tech/api";
```
Este archivo fue resubido al VPS. Con este cambio, el frontend en el navegador empezó a consumir el catálogo de precios scrapeados desde la nube con éxito.

## Resumen del Éxito
- **API Market (FastAPI):** Funciona y responde correctamente a las solicitudes Web.
- **Conectividad a Supabase:** Establecida tras asignar el correcto `.env`.
- **UI:** El Dashboard lee los márgenes de precios remotos usando el proxy inverso de Nginx sin errores CORS.
