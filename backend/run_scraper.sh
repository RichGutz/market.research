#!/bin/bash

# --- Configuración Backend Market Tracker ---
# Adaptado del script robusto de Scraper.Neoauto
# Ajustar PROJECT_DIR a la ruta real de despliegue en el VPS (según DEPLOYMENT_A_HOSTINGER.md)
PROJECT_DIR="/var/www/html/research"
LOG_FILE="$PROJECT_DIR/cron_scraper.log"
PYTHON_EXEC="$PROJECT_DIR/venv/bin/python"

# --- Logging Setup ---
# Redirige toda la salida (stdout y stderr) al log file y a la consola
exec > >(tee -a "$LOG_FILE") 2>&1

echo ""
echo "=================================================="
echo "INICIANDO MARKET TRACKER SCRAPING - $(date)"
echo "=================================================="

# Moverse al directorio del backend
cd "$PROJECT_DIR/backend" || { echo "ERROR: No se pudo acceder a $PROJECT_DIR/backend"; exit 1; }

# Ejecutar el Scraper Principal
echo "--> Ejecutando scraper_peru.py..."
# -u asegura que el stdout no tenga buffer y se loguee en tiempo real
$PYTHON_EXEC -u "scraper_peru.py"

if [ $? -ne 0 ]; then
    echo "ERROR en la ejecución del Scraper. Revisa los logs en Supabase o el script."
    exit 1
fi

echo ""
echo "=================================================="
echo "SECUENCIA COMPLETADA - $(date)"
echo "=================================================="

echo ""
echo "PROCESO FINALIZADO."
exit 0
