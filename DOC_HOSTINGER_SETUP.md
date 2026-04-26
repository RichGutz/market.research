# Guía de Automatización: Scraping Semanal en Hostinger

Para que los precios de tu Web App se actualicen solos cada semana desde tu servidor de Hostinger, sigue estos pasos:

## 1. Subir los Archivos
Asegúrate de que en tu carpeta del proyecto en Hostinger estén presentes:
- `backend/scraper_peru.py` (Ya tiene la lógica de Supabase y ruteo).
- `.env` (Con tus credenciales de SUPABASE_URL y SUPABASE_KEY).

## 2. Instalar Dependencias en Hostinger
Desde la terminal SSH de Hostinger, instala Playwright y sus navegadores:
```bash
pip install playwright supabase python-dotenv
playwright install chromium
```

## 3. Configurar el Cron Job (Tarea Programada)
1. Ve a tu **Panel de Control de Hostinger**.
2. Busca la sección **Avanzado > Tareas Cron**.
3. Crea una nueva tarea con esta configuración:

- **Tipo**: PHP (o Custom si permite Python directo).
- **Comando**:
  ```bash
  bash /var/www/html/research/backend/run_scraper.sh
  ```
  *(NOTA: Primero debes asegurarte de haberle dado permisos de ejecución al archivo subiéndolo y ejecutando `chmod +x run_scraper.sh`)*.

- **Frecuencia**: Todos los días a las 3:33 AM. Usa esta expresión personalizada:
  - `33 3 * * *`

## 4. Verificación
El script `scraper_peru.py` está configurado para leer todo tu catálogo de Supabase, buscar los precios en Perú y guardar los resultados automáticamente en la tabla de la categoría que corresponda (`prices_iphone`, `prices_iwatch`, etc.).

---
> [!TIP]
> Puedes probar que todo funciona corriendo el comando manualmente una vez desde SSH antes de programar el Cron.
