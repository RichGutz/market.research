import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('91.108.125.253', 22, 'root', 'doHtFib1poV+f0F7')

cmd = "cd /var/www/html/research && source venv/bin/activate && python backend/scraper_peru_v2.py"
print(f"Ejecutando: {cmd}")
stdin, stdout, stderr = client.exec_command(cmd)

# Leer salida (puede tardar un rato porque es el scraper completo)
for line in iter(stdout.readline, ""):
    print(line, end="")
    
for line in iter(stderr.readline, ""):
    print(line, end="")

client.close()
