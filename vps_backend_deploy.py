import paramiko

def run_ssh_command(host, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Connecting to {host}...")
    client.connect(hostname=host, port=port, username=username, password=password)
    
    print(f"Executing: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    
    if out:
        print("--- STDOUT ---")
        try:
            print(out)
        except Exception:
            print(out.encode('utf-8', errors='replace').decode('cp1252', errors='replace'))
    if err:
        print("--- STDERR ---")
        try:
            print(err)
        except Exception:
            print(err.encode('utf-8', errors='replace').decode('cp1252', errors='replace'))
        
    client.close()
    print("Connection closed.")

if __name__ == "__main__":
    HOST = "91.108.125.253"
    USER = "root"
    PASS = "N4pee0BVZsL@r6dJz4R+"
    
    COMMAND = """
    cd /var/www/html/research
    
    # 1. Crear entorno virtual e instalar requerimientos
    python3 -m venv venv
    source venv/bin/activate
    pip install fastapi uvicorn supabase python-dotenv playwright
    playwright install chromium
    playwright install-deps chromium
    
    # Asegurar permisos en backend
    chmod +x backend/api_market.py
    chmod +x backend/scraper_peru.py
    
    # 2. Configurar el Systemd Service para Uvicorn
    cat << 'EOF' > /etc/systemd/system/research_api.service
[Unit]
Description=Gunicorn instance to serve Research FastAPI Backend
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/html/research/backend
Environment="PATH=/var/www/html/research/venv/bin"
# Ejecutamos con Uvicorn en el puerto 8000
ExecStart=/var/www/html/research/venv/bin/uvicorn api_market:app --host 127.0.0.1 --port 8000

[Install]
WantedBy=multi-user.target
EOF

    # 3. Recargar y habilitar servicio
    systemctl daemon-reload
    systemctl start research_api
    systemctl enable research_api
    systemctl status research_api --no-pager
    """
    
    run_ssh_command(HOST, 22, USER, PASS, COMMAND)
