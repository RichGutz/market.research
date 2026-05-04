import paramiko
import os

# ============================================================
# F4_deploy_market_research.py
# Script de Despliegue: Market Research (GyP Module)
# Dominio: research.geeksoft.tech
# Conecta al VPS Hostinger vía SSH y sincroniza archivos
# ============================================================

VPS_HOST   = "91.108.125.253"
VPS_PORT   = 22
VPS_USER   = "root"
VPS_PASS   = "doHtFib1poV+f0F7"
DOMAIN     = "research.geeksoft.tech"
SERVICE_NAME = "market_research"
APP_DIR    = "/opt/market_research"
REPO_URL   = "https://github.com/RichGutz/market.research.git"

def ssh_run(client, cmd, label=""):
    if label:
        print(f"\n[{label}]")
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    # Sanitize for Windows console (remove non-ascii safely)
    out = out.encode("ascii", errors="replace").decode("ascii")
    err = err.encode("ascii", errors="replace").decode("ascii")
    if out.strip():
        print(f" >> {out.strip()[:500]}")
    if err.strip():
        print(f" !! {err.strip()[:300]}")

def deploy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(f"Conectando a {VPS_HOST}...")
        client.connect(hostname=VPS_HOST, port=VPS_PORT, username=VPS_USER, password=VPS_PASS, timeout=20)

        # 1. Git Pull / Clone
        git_cmd = (
            f"if [ -d '{APP_DIR}/.git' ]; then "
            f"cd {APP_DIR} && git fetch origin && git reset --hard origin/main; "
            f"else git clone {REPO_URL} {APP_DIR}; fi"
        )
        ssh_run(client, git_cmd, "1. Sincronizando Repositorio Git")

        # 1b. Limpiar configs nginx conflictivas previas de este dominio
        cleanup_cmd = (
            f"grep -rl '{DOMAIN}' /etc/nginx/sites-enabled/ | "
            f"grep -v '{SERVICE_NAME}' | xargs rm -f || true"
        )
        ssh_run(client, cleanup_cmd, "1b. Limpiando configs Nginx conflictivas")

        # 2. Configurar Nginx para Market Research
        nginx_cfg = f"""server {{
    server_name {DOMAIN};
    root {APP_DIR}/frontend;
    index login.html;

    location / {{
        try_files $uri $uri/ =404;
    }}

    location /api/ {{
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }}

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/{DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{DOMAIN}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}}

server {{
    if ($host = {DOMAIN}) {{
        return 301 https://$host$request_uri;
    }}
    listen 80;
    server_name {DOMAIN};
    return 404;
}}"""

        ssh_run(client,
            f"cat > /etc/nginx/sites-available/{SERVICE_NAME} << 'NGINXEOF'\n{nginx_cfg}\nNGINXEOF",
            "2. Configurando Nginx")
        ssh_run(client,
            f"ln -sf /etc/nginx/sites-available/{SERVICE_NAME} /etc/nginx/sites-enabled/{SERVICE_NAME} && nginx -t && systemctl reload nginx",
            "3. Activando Nginx")

        # 3. Python Backend (FastAPI via Uvicorn + PM2)
        backend_cmd = (
            f"cd {APP_DIR}/backend && "
            f"pip install -r requirements.txt -q && "
            f"pm2 delete market_research_api || true && "
            f"pm2 start 'uvicorn main:app --host 0.0.0.0 --port 8001' --name market_research_api && "
            f"pm2 save -f"
        )
        ssh_run(client, backend_cmd, "4. Arrancando Backend FastAPI (PM2)")

        # 4. SSL Certbot (solo si no existe certificado)
        certbot_cmd = (
            f"certbot --nginx -d {DOMAIN} "
            f"--non-interactive --agree-tos -m contacto@geeksoft.pe --redirect"
        )
        ssh_run(client, certbot_cmd, "5. Certbot SSL")

        print(f"\n{'='*55}")
        print(f" [OK] MARKET RESEARCH DESPLEGADO EN: https://{DOMAIN}")
        print(f"{'='*55}\n")

    except Exception as e:
        print(f"[ERROR FATAL] {e}")
    finally:
        client.close()

if __name__ == "__main__":
    deploy()
