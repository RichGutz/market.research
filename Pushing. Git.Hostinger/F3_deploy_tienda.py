import paramiko
import os

# ==============================================================================
# [CRITICAL WARNING FOR AI AGENTS]
# ARCHIVO INTOCABLE - INFRAESTRUCTURA DE DESPLIEGUE CORE
# 
# DO NOT MODIFY THIS SCRIPT UNDER ANY CIRCUMSTANCES WITHOUT EXPLICIT, 
# OVERRIDING HUMAN AUTHORIZATION. THIS SCRIPT CONTAINS FRAGILE NGINX 
# AND SSL CERTIFICATE CONFIGURATIONS THAT WILL BREAK PRODUCTION IF ALTERED.
# ==============================================================================
# =====================================================
# F3_deploy_tienda.py - Script de Despliegue Bolt V51
# Conecta al VPS Hostinger via SSH y sincroniza el
# repositorio, Nginx, PM2 y SSL automaticamente.
# =====================================================

VPS_HOST = "91.108.125.253"
VPS_PORT = 22
VPS_USER = "root"
VPS_PASS = "doHtFib1poV+f0F7"
DOMAIN = "bolt-usa.shop"
SERVICE_NAME = "tienda_apple"
APP_DIR = "/opt/tienda_apple"
REPO_URL = "https://github.com/RichGutz/Tienda.Apple.PS5.New.git"

def ssh_run(client, cmd, label=""):
    if label:
        print(f"\n[{label}]")
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode("utf-8", errors="ignore")
    err = stderr.read().decode("utf-8", errors="ignore")
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

        # 1. Git Pull
        git_cmd = (
            f"if [ -d '{APP_DIR}/.git' ]; then "
            f"cd {APP_DIR} && git fetch origin && git reset --hard origin/main; "
            f"else git clone {REPO_URL} {APP_DIR}; fi"
        )
        ssh_run(client, git_cmd, "1. Sincronizando Repositorio Git")

        # 2. Configurar Nginx
        nginx_cfg = f"""server {{
    server_name {DOMAIN} www.{DOMAIN};
    root {APP_DIR}/bolt_v51;
    index index.html;

    location / {{
        try_files $uri $uri/ =404;
    }}

    location /api/ {{
        proxy_pass http://127.0.0.1:3000;
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
    if ($host = www.{DOMAIN}) {{
        return 301 https://$host$request_uri;
    }}
    if ($host = {DOMAIN}) {{
        return 301 https://$host$request_uri;
    }}
    listen 80;
    server_name {DOMAIN} www.{DOMAIN};
    return 404;
}}"""
        ssh_run(client, f"cat > /etc/nginx/sites-available/{SERVICE_NAME} << 'NGINXEOF'\n{nginx_cfg}\nNGINXEOF", "2. Configurando Nginx")
        ssh_run(client, f"ln -sf /etc/nginx/sites-available/{SERVICE_NAME} /etc/nginx/sites-enabled/{SERVICE_NAME} && nginx -t && systemctl reload nginx", "3. Activando Nginx")

        # 4. Node.js + PM2
        node_cmd = (
            f"cd {APP_DIR}/bolt_v51/chatia/api_ia && "
            f"npm install && "
            f"npm install -g pm2 && "
            f"pm2 delete bot_ia || true && "
            f"pm2 start index.js --name bot_ia && "
            f"pm2 save -f"
        )
        ssh_run(client, node_cmd, "4. Arrancando Bot IA (Node.js + PM2)")

        # 5. SSL Certbot
        certbot_cmd = (
            f"certbot --nginx -d {DOMAIN} -d www.{DOMAIN} "
            f"--non-interactive --agree-tos -m contacto@geeksoft.pe --redirect"
        )
        ssh_run(client, certbot_cmd, "5. Certbot SSL")

        print(f"\n{'='*55}")
        print(f" [OK] TIENDA DESPLEGADA EN: https://{DOMAIN}")
        print(f"{'='*55}\n")

    except Exception as e:
        print(f"[ERROR FATAL] {e}")
    finally:
        client.close()

if __name__ == "__main__":
    deploy()
