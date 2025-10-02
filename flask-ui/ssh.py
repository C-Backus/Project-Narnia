import paramiko

def list_files():
    hostname = "localhost"
    port = 2222
    username = ""    #username (not here for security)
    password = ""   #password (not here for security)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=port, username=username, password=password)
       
       
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
