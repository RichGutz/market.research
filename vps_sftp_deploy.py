import paramiko
import os
from stat import S_ISDIR

def deploy_via_sftp(host, port, username, password, local_dir, remote_dir):
    print(f"Connecting to {host}...")
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    # Check if remote directory exists, if not create it
    try:
        sftp.stat(remote_dir)
    except IOError:
        sftp.mkdir(remote_dir)
        
    print(f"Uploading files from {local_dir} to {remote_dir}...")
    
    # Traverse local directory and upload files
    for root, dirs, files in os.walk(local_dir):
        # Skip git and venv folders
        if '.git' in root or 'venv' in root or '.venv' in root or '__pycache__' in root:
            continue
            
        # Calculate relative path
        rel_path = os.path.relpath(root, local_dir)
        if rel_path == '.':
            remote_path = remote_dir
        else:
            remote_path = os.path.join(remote_dir, rel_path).replace('\\', '/')
            
        # Create directories remotely
        try:
            sftp.stat(remote_path)
        except IOError:
            sftp.mkdir(remote_path)
            
        for file in files:
            # Skip some files
            if file in ['.env', 'vps_deploy.py', 'vps_sftp_deploy.py'] or file.endswith('.pyc'):
                continue
                
            local_file = os.path.join(root, file)
            remote_file = os.path.join(remote_path, file).replace('\\', '/')
            
            # Print a dot for each file to show progress
            print(f"Uploading: {remote_file}")
            sftp.put(local_file, remote_file)
            
    sftp.close()
    
    # Otorgamos permisos de ejecución al bash script del cron en el VPS
    print("\nAsegurando permisos de ejecución (chmod +x) para run_scraper.sh...")
    session = transport.open_session()
    session.exec_command(f'chmod +x {remote_dir}/backend/run_scraper.sh')
    
    transport.close()
    print("\nUpload complete!")

if __name__ == "__main__":
    HOST = "91.108.125.253"
    USER = "root"
    PASS = "N4pee0BVZsL@r6dJz4R+"
    
    LOCAL_DIR = r"C:\Users\rguti\Tienda.APPLE.PS5\Market.Research"
    REMOTE_DIR = "/var/www/html/research"
    
    deploy_via_sftp(HOST, 22, USER, PASS, LOCAL_DIR, REMOTE_DIR)
