import paramiko

def list_files():
    hostname = "localhost"
    port = 2222
    username = ""    #username (not filled for security)
    key_path = "" #using ssh key (not filled for security)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.Ed25519Key(filename=key_path)
        ssh.connect(hostname, port=port, username=username, pkey=private_key)
       
       
        #this runs command to lsit all folders in home directory
        #while connected to wsl 
        sftp = ssh.open_sftp()
        file_list = sftp.listdir('/home/' + username)
        sftp.close()
        ssh.close()
        return file_list
    
    except Exception as e:
        print(f"Error connecting to WSL: {e}")
        return []
