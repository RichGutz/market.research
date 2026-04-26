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
    cat << 'EOF' > /etc/nginx/sites-available/research.conf
server {
    listen 80;
    server_name research.geeksoft.tech;
    
    root /var/www/html/research/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Reescribe /api/algo a /algo sin el slash final extra
        rewrite ^/api/(.*)$ /$1 break;
    }
}
EOF

    nginx -t
    systemctl reload nginx
    """
    
    run_ssh_command(HOST, 22, USER, PASS, COMMAND)
