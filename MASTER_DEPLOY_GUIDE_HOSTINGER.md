# MASTER GUIDE: Deploying Multiple Private Apps on Hostinger VPS

> [!IMPORTANT]
> **PROTOCOLO PARA AGENTES IA (ANTIGRAVITY/GEMINI):**
> 1. **NUNCA** subas archivos "basura" (videos, audios, zips gigantes, logs).
> 2. **SIEMPRE** verifica el `.gitignore` antes de cualquier `git add`.
> 3. **PASO A PASO**: No ejecutes comandos encadenados (`&&`). Hazlo uno por uno y pide autorización humana tras cada paso (`status` -> `add` -> `commit` -> `push`).

## 1. Architecture (The "Monorepo" Concept)

Instead of managing separate repositories for each app, we use **one central repository** (`Petral.MARK`) that contains all your applications as subfolders.

**Local Hierarchy (Your PC):**
```text
C:\Users\rguti\Petral.MARK\         <-- The Git Repo Root
├── .git/                           <-- The ONLY git folder (Vital!)
├── update.sh                       <-- The Automation Script
├── GeekSoft_Portal/                <-- The Landing Page (geeksoft.tech)
├── Dashboard_Puertos/              <-- App 1 (geeksoft.tech/petral)
├── Future_App_Finzas/              <-- App 2 (geeksoft.tech/finanzas)
└── Future_App_XYZ/                 <-- App 3 (geeksoft.tech/xyz)
```

**Server Hierarchy (VPS):**
```text
/files_repo/                        <-- Raw Code (Git Clone)
/var/www/html/                      <-- Live Website
├── index.html                      <-- Portal
├── petral/                         <-- App 1
├── finanzas/                       <-- App 2
└── xyz/                            <-- App 3
```

---

## 2. Cheat Sheet: Daily Deployment

When you have made changes to any app:

### Step A: Push from PC
```powershell
cd C:\Users\rguti\Petral.MARK
git add .
git commit -m "Update: Description of changes"
git push origin deploy-vps-2026.02.04.18.10
```
*(Make sure you are pushing to the active branch used by the server)*

### Step B: Update Server (Copy-Paste)

1.  **Abrir Terminal**: Busca "PowerShell" en tu Windows y ábrelo.
2.  **Conectarse** (Copia y pega este bloque):
    ```powershell
    ssh root@91.108.125.253
    ```
    *   **Password**: Copia tu contraseña (`...`), haz **CLIC DERECHO** en la ventana negra (no verás nada) y pulsa ENTER.

3.  **Ejecutar Actualización** (Copia y pega):
    ```bash
    cd /files_repo && sh update.sh
    ```
    *   *Espera hasta ver: "✅ DESPLIEQUE COMPLETADO".*

---

## 2.1. Protocolo Obligatorio para AGENTES IA

Si eres una IA, **DEBES** seguir estos pasos sin excepción para evitar subir archivos pesados o corromper el repo:

### Fase 1: Auditoría de Archivos
1. Ejecuta `git status` y revisa la lista de archivos.
2. Si ves archivos `.mp4`, `.mp3`, `.zip` o similares que no sean código puro, **DETENTE**.
3. Verifica que el `.gitignore` actual los bloquee. Si no, edítalo **PRIMERO**.

### Fase 2: Ejecución Atómica (Uno por Uno)
**No uses `&&`. Pide permiso antes de cada paso:**

1.  **Status**: Muestra el `git status` al usuario y espera autorización.
2.  **Add**: Usa `git add <archivo_especifico>` o `git add .` solo si estás 100% seguro. Muestra qué agregaste.
3.  **Commit**: Realiza el commit y muestra el mensaje.
4.  **Push**: Pregunta al usuario antes de hacer el push final.

> [!WARNING]
> La conexión SSH a Hostinger y el comando `update.sh` los realiza el **USUARIO MANUALMENTE** a menos que él pida lo contrario. No intentes automatizar el SSH si el usuario prefiere controlarlo.

---

## 3. Workflow: Adding a NEW App

Follow this strict process to add a new application (e.g., "Minera_KPIs"):

1.  **Create Folder**: Create `C:\Users\rguti\Petral.MARK\Minera_KPIs`.
2.  **Add Code**: Put your HTML/Python/JS files inside.
    *   *CRITICAL*: **DO NOT** run `git init` inside this folder. It must be a normal folder, not a git repo.
3.  **Register in Script**:
    *   Open `update.sh`.
    *   Copy the block for "Dashboard_Puertos".
    *   Paste it and rename to "Minera_KPIs", mapping it to `/var/www/html/minera`.
4.  **Push & Deploy**: Follow the "Daily Deployment" steps above.
5.  **Verify**: accurate `geeksoft.tech/minera`.

---

## 4. Troubleshooting (Common Errors)

**Error 403 Forbidden**
*   **Cause**: Missing `index.html` or bad permissions.
*   **Fix**: Run `update.sh` again (it auto-fixes permissions). Check if your app actually has an `index.html`.

**"Repository not found" / files not updating**
*   **Cause**: You might have a nested `.git` folder inside an app folder.
*   **Fix**:
    ```powershell
    # On your PC
    cd YourAppFolder
    rm -r -fo .git  # Delete the nested git
    cd ..
    git rm --cached YourAppFolder
    git add YourAppFolder/*
    ```

**"Permission denied" (SSH)**
*   **Fix**: You typed the password wrong. Copy text, Right-Click in terminal to paste.

---

## 5. Server Setup Reference (One-Time Only)

*If you ever destroy the VPS and start from scratch:*

**Credentials**:
*   **IP**: `91.108.125.253`
*   **User**: `root`
*   **Deploy Path**: `/files_repo`

**Initialization Commands:**
```bash
apt update && apt install -y nginx git
mkdir /files_repo
git clone -b deploy-vps-2026.02.04.18.10 https://github.com/RichGutz/MARK.git /files_repo
# Then run update.sh
```

---

## 6. Configurar el Portal (Login -> App Routing)

La "magia" de que cada usuario vaya a su App (ej: `admin` -> `/petral`, `rrhh` -> `/nominas`) está en el código del Portal.

Cuando subas una nueva App:

1.  Abre `GeekSoft_Portal/index.html`.
2.  Busca la sección de JavaScript (`// --- AUTH ---`).
3.  Agrega la lógica para el nuevo usuario.

**Ejemplo:**
```javascript
const user = document.getElementById('username').value;
// ...
if (user === 'petral') {
    window.location.href = '/petral/'; // Va a la App 1
} else if (user === 'rrhh') {
    window.location.href = '/rrhh/';   // Va a la App 2 (Nueva)
}
```
*Simplemente edita esto, haz Git Push, Update, y listo.*

---

## 8. Automated Data Scraper (24/7)

Tu aplicación puede scrapear datos automáticamente cada hora y subirlos a Supabase para análisis histórico.

### Configuración Inicial (Una Sola Vez)

**Requisitos:**
- Python 3 (ya instalado en el VPS)
- Dependencias: `requests`, `beautifulsoup4`, `python-dotenv`, `supabase`

**Instalación:**
```bash
# Conectarse al VPS
ssh root@91.108.125.253

# Instalar dependencias
pip3 install requests beautifulsoup4 python-dotenv supabase

# Crear directorio
mkdir -p /files_repo/Dashboard_Puertos
cd /files_repo/Dashboard_Puertos
```

### Archivos Necesarios

Los siguientes archivos deben estar en `/files_repo/Dashboard_Puertos/`:

1. **scraper_apu.py** - Scraper principal (scrapea APN y guarda `ships_data.js`)
2. **sync_supabase.py** - Sincroniza datos a Supabase
3. **.env** - Credenciales de Supabase
4. **/files_repo/run_scraper.sh** - Script de automatización

**Nota:** Estos archivos ya están configurados en el VPS. Ver implementación en el repositorio.

### Cron Job (Ejecución Automática)

El scraper se ejecuta **cada hora en punto** (24 veces al día):

```bash
# Ver configuración actual
crontab -l

# Debería mostrar:
# 0 * * * * /bin/bash /files_repo/run_scraper.sh
```

### Flujo Automático

Cada hora (00:00, 01:00, 02:00... 23:00):
1. Scraper descarga datos de https://eredenaves.apn.gob.pe
2. Guarda en `/var/www/html/petral/ships_data.js`
3. Frontend lee el archivo actualizado
4. Sync sube datos a Supabase (histórico)
5. Todo se registra en `/var/log/scraper.log`

### Verificación y Logs

```bash
# Ver últimas ejecuciones
tail -50 /var/log/scraper.log

# Ejecutar manualmente (para probar)
/bin/bash /files_repo/run_scraper.sh

# Ver archivo generado
ls -lh /var/www/html/petral/ships_data.js
```

### Troubleshooting

**El scraper no se ejecuta:**
```bash
# Verificar que el cron está activo
crontab -l | grep scraper

# Verificar permisos del script
ls -lh /files_repo/run_scraper.sh
# Debe mostrar: -rwxr-xr-x (ejecutable)

# Si no tiene permisos:
chmod +x /files_repo/run_scraper.sh
```

**Error de conexión a APN:**
- El sitio de APN puede estar en mantenimiento
- Verificar en el log: `tail -20 /var/log/scraper.log`
- El scraper reintentará en la próxima hora

**Error de Supabase:**
- Verificar credenciales en `/files_repo/Dashboard_Puertos/.env`
- Verificar que la tabla `port_arrivals` existe en Supabase
- Ver error específico en el log

---

## 9. Workflow: Actualizar Apps SIN Romper el Scraper

**⚠️ IMPORTANTE:** Cuando agregues funcionalidad a tu app, debes entender qué se actualiza y qué NO.

### Flujo Normal de Actualización

#### Paso 1: Modificar en tu PC
```powershell
cd C:\Users\rguti\Petral.MARK
# Editas tu código (HTML/CSS/JS)
git add .
git commit -m "Nueva funcionalidad X"
git push origin deploy-vps-2026.02.04.18.10
```

#### Paso 2: Actualizar en VPS
```bash
ssh root@91.108.125.253
cd /files_repo && sh update.sh
```

### ✅ Archivos que NO se Sobrescriben (SEGUROS)

Estos permanecen intactos después de `update.sh`:

| Archivo/Config | Ubicación | Descripción |
|----------------|-----------|-------------|
| **Cron job** | Sistema (`crontab`) | Configuración de ejecución automática |
| **Scraper Python** | `/files_repo/Dashboard_Puertos/` | Scripts de scraping |
| **Logs** | `/var/log/scraper.log` | Historial de ejecuciones |
| **ships_data.js** | `/var/www/html/petral/` | Se regenera automáticamente cada hora |
| **Dependencias Python** | Sistema | Librerías instaladas con `pip3` |

### ❌ Archivos que SÍ se Actualizan

Estos se sobrescriben con `update.sh`:

| Archivo | Ubicación | Solución |
|---------|-----------|----------|
| **Frontend** (HTML/CSS/JS) | `/var/www/html/petral/` | ✅ Normal, es lo que quieres actualizar |
| **Archivos en Git** | Todo lo que esté en el repo | Usar `.gitignore` para proteger archivos |

### 🛡️ Proteger Archivos Críticos

**Agregar a `.gitignore`:**
```
# Archivos del scraper que NO deben subirse a Git
Dashboard_Puertos/.env
Dashboard_Puertos/scraper_log.txt
Dashboard_Puertos/tanker_cache.json
Dashboard_Puertos/ships_data.js
```

### 📋 Workflows Específicos

#### Actualizar SOLO el Frontend
```powershell
# En tu PC
git add Dashboard_Puertos/*.html Dashboard_Puertos/*.css Dashboard_Puertos/*.js
git commit -m "Update UI"
git push

# En VPS
cd /files_repo && sh update.sh
```
✅ **Scraper NO se afecta**

#### Actualizar el Scraper

**Opción A: Editar directamente en VPS (Recomendado para cambios rápidos)**
```bash
ssh root@91.108.125.253
nano /files_repo/Dashboard_Puertos/scraper_apu.py
# Editar, guardar (Ctrl+O, Enter, Ctrl+X)
```

**Opción B: Desde Git (Para cambios importantes)**
```powershell
# 1. En tu PC
git add Dashboard_Puertos/scraper_apu.py
git commit -m "Update scraper logic"
git push

# 2. En VPS
cd /files_repo
git pull
# El scraper se actualiza automáticamente en la próxima ejecución
```

### ⚠️ Reglas de Oro

1. **NUNCA** borres el cron job (`crontab -e`)
2. **NUNCA** borres `/files_repo/Dashboard_Puertos/` manualmente
3. **SIEMPRE** usa `.gitignore` para archivos sensibles (`.env`)
4. **VERIFICA** después de actualizar: `tail -20 /var/log/scraper.log`

### 🔍 Verificación Post-Deploy

Después de cada actualización, verifica que todo sigue funcionando:

```bash
# 1. Verificar que el cron sigue activo
crontab -l | grep scraper

# 2. Verificar que el scraper existe
ls -lh /files_repo/Dashboard_Puertos/scraper_apu.py

# 3. Ver últimas ejecuciones
tail -20 /var/log/scraper.log

# 4. Probar manualmente
/bin/bash /files_repo/run_scraper.sh
```

---

## 10. 🚨 Plan de Emergencia: Si Algo Se Rompe

**Si el próximo agente (o tú) rompe algo, aquí está cómo recuperarlo.**

### 🔄 Backup Automático del Scraper

**Crear backup AHORA (antes de que algo se rompa):**

```bash
# Conectar al VPS
ssh root@91.108.125.253

# Crear backup completo
tar -czf /root/scraper_backup_$(date +%Y%m%d).tar.gz \
  /files_repo/Dashboard_Puertos/scraper_apu.py \
  /files_repo/Dashboard_Puertos/sync_supabase.py \
  /files_repo/Dashboard_Puertos/.env \
  /files_repo/run_scraper.sh

# Guardar cron job
crontab -l > /root/crontab_backup.txt

# Verificar backups
ls -lh /root/*backup*
```

### 🛟 Restaurar desde Backup

**Si algo se rompió:**

```bash
# 1. Conectar al VPS
ssh root@91.108.125.253

# 2. Ver backups disponibles
ls -lh /root/*backup*

# 3. Restaurar archivos
cd /
tar -xzf /root/scraper_backup_YYYYMMDD.tar.gz

# 4. Restaurar cron job
crontab /root/crontab_backup.txt

# 5. Verificar
crontab -l | grep scraper
ls -lh /files_repo/Dashboard_Puertos/scraper_apu.py
```

### 🔧 Fixes Rápidos para Problemas Comunes

#### Problema 1: Cron Job Desapareció

```bash
# Restaurar cron job manualmente
crontab -e
# Agregar esta línea:
# 0 * * * * /bin/bash /files_repo/run_scraper.sh
```

#### Problema 2: Scraper No Existe

```bash
# Verificar si existe
ls -lh /files_repo/Dashboard_Puertos/scraper_apu.py

# Si no existe, restaurar desde backup
tar -xzf /root/scraper_backup_*.tar.gz

# O copiar desde Git
cd /files_repo
git pull
cp Dashboard_Puertos/scraper_apu.py /files_repo/Dashboard_Puertos/
```

#### Problema 3: Permisos Incorrectos

```bash
# Arreglar permisos
chmod +x /files_repo/run_scraper.sh
chmod 644 /files_repo/Dashboard_Puertos/scraper_apu.py
chmod 644 /files_repo/Dashboard_Puertos/sync_supabase.py
chmod 600 /files_repo/Dashboard_Puertos/.env
```

#### Problema 4: Dependencias Faltantes

```bash
# Reinstalar todas las dependencias
pip3 install requests beautifulsoup4 python-dotenv supabase
```

### 📋 Checklist de Verificación Completa

**Ejecuta esto para verificar que TODO está bien:**

```bash
# 1. Cron job activo
echo "=== CRON JOB ==="
crontab -l | grep scraper

# 2. Archivos del scraper
echo "=== ARCHIVOS ==="
ls -lh /files_repo/Dashboard_Puertos/scraper_apu.py
ls -lh /files_repo/Dashboard_Puertos/sync_supabase.py
ls -lh /files_repo/run_scraper.sh

# 3. Dependencias Python
echo "=== DEPENDENCIAS ==="
pip3 list | grep -E "requests|beautifulsoup4|supabase|python-dotenv"

# 4. Última ejecución
echo "=== ÚLTIMO LOG ==="
tail -10 /var/log/scraper.log

# 5. Probar ejecución manual
echo "=== PRUEBA MANUAL ==="
/bin/bash /files_repo/run_scraper.sh
```

### 🆘 Comandos de Emergencia (Copia y Pega)

**Si TODO falla, ejecuta este bloque completo:**

```bash
# RESTAURACIÓN COMPLETA DE EMERGENCIA
ssh root@91.108.125.253 << 'ENDSSH'

# 1. Reinstalar dependencias
pip3 install requests beautifulsoup4 python-dotenv supabase

# 2. Recrear cron job
(crontab -l 2>/dev/null | grep -v scraper; echo "0 * * * * /bin/bash /files_repo/run_scraper.sh") | crontab -

# 3. Verificar estructura
mkdir -p /files_repo/Dashboard_Puertos

# 4. Arreglar permisos
chmod +x /files_repo/run_scraper.sh
chmod 644 /files_repo/Dashboard_Puertos/*.py
chmod 600 /files_repo/Dashboard_Puertos/.env

# 5. Probar
/bin/bash /files_repo/run_scraper.sh

echo "✅ Restauración completada"
ENDSSH
```

### 📞 Contacto de Emergencia

**Si nada funciona, contacta con:**
- Soporte de Hostinger: https://hpanel.hostinger.com
- Documentación de este setup: `MASTER_DEPLOY_GUIDE_HOSTINGER.md`

### 💾 Recomendación: Backups Programados

**Crear backup automático semanal:**

```bash
# Agregar a crontab
crontab -e

# Agregar esta línea (backup cada domingo a las 3am):
# 0 3 * * 0 tar -czf /root/scraper_backup_$(date +\%Y\%m\%d).tar.gz /files_repo/Dashboard_Puertos/ /files_repo/run_scraper.sh

---

## 11. Automatización Total con GitHub Actions (Nuevo)

Para evitar entrar por SSH manualmente, puedes configurar GitHub para que lo haga por ti.

### Paso 1: Configurar Secretos en GitHub
1.  Ve a tu repositorio en GitHub -> **Settings**.
2.  En el menú lateral: **Secrets and variables** -> **Actions**.
3.  Haz clic en **New repository secret** y agrega estos 3:

| Nombre | Valor (Ejemplo) |
|--------|-----------------|
| `VPS_HOST` | `91.108.125.253` |
| `VPS_USER` | `root` |
| `VPS_PASSWORD` | *(Tu contraseña del VPS)* |

### Paso 2: Funcionamiento
Una vez configurado, cada vez que hagas un **git push**, GitHub:
1.  Se conectará automáticamente al VPS.
2.  Ejecutará `update.sh`.
3.  Podrás ver el resultado en la pestaña **Actions** de tu repositorio.

> [!NOTE]
> Si el despliegue falla, recibirás un correo de GitHub. Revisa los logs en la pestaña Actions para ver qué pasó.
```
