import paramiko

VPS_HOST = "91.108.125.253"
VPS_PORT = 22
VPS_USER = "root"
VPS_PASS = "doHtFib1poV+f0F7"
APP_DIR = "/var/www/html/research"
REPO_URL = "https://github.com/RichGutz/market.research.git"

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
            f"cd {APP_DIR} && git remote set-url origin {REPO_URL} && git fetch --all && git reset --hard origin/main; "
            f"else "
            f"mkdir -p {APP_DIR} && cd {APP_DIR} && git init && git remote add origin {REPO_URL} && git fetch --all && git reset --hard origin/main; "
            f"fi"
        )
        ssh_run(client, git_cmd, "1. Sincronizando Repositorio Git")

        # 2. Restarting API
        ssh_run(client, "systemctl restart research_api", "2. Reiniciando servicio FastAPI")
        
        # 3. Setting permissions
        ssh_run(client, f"chmod +x {APP_DIR}/backend/run_scraper.sh", "3. Permisos cron")

        print("\n[OK] DESPLIEGUE MARKET RESEARCH COMPLETADO.")

    except Exception as e:
        print(f"[ERROR FATAL] {e}")
    finally:
        client.close()

if __name__ == "__main__":
    deploy()
