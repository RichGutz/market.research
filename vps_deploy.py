import paramiko
import time

def run_ssh_command(host, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Connecting to {host}...")
    client.connect(hostname=host, port=port, username=username, password=password)
    
    print(f"Executing: {command}")
    stdin, stdout, stderr = client.exec_command(command)
    
    out = stdout.read().decode('utf-8')
    err = stderr.read().decode('utf-8')
    
    if out:
        print("--- STDOUT ---")
        print(out)
    if err:
        print("--- STDERR ---")
        print(err)
        
    client.close()
    print("Connection closed.")

if __name__ == "__main__":
    HOST = "91.108.125.253"
    USER = "root"
    PASS = "N4pee0BVZsL@r6dJz4R+"
    
    COMMAND = """
    if [ -d "/var/www/html/research/.git" ]; then
        cd /var/www/html/research
        git fetch --all
        git reset --hard origin/main
    else
        mkdir -p /var/www/html/research
        cd /var/www/html/research
        git clone https://github.com/RichGutz/Tienda.Apple.PS5.git .
        # Ensure it cloned correctly
        ls -la
    fi
    """
    
    run_ssh_command(HOST, 22, USER, PASS, COMMAND)
