import paramiko
import stat 

FILE = '' #redacted
USERNAME = '' #redacted


#establish SSH & SFTP connection
def get_sftp():
    hostname = "localhost"
    port = 2222
    username = USERNAME
    key_path = "" #redacted

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.Ed25519Key(filename=key_path)
    ssh.connect(hostname=hostname, port=port, username=username, pkey=private_key)
    sftp = ssh.open_sftp()
    return ssh, sftp

def get_file_list_from_folder(subfolder=""):
    try:
        ssh, sftp = get_sftp()
        base_path = FILE    #make whatever root folder is
        remote_path = f"{base_path}/{subfolder}".rstrip('/')

        all_items = sftp.listdir_attr(remote_path)

        # Separate strings for template
        folders = [f.filename for f in all_items if stat.S_ISDIR(f.st_mode)]
        files   = [f.filename for f in all_items if stat.S_ISREG(f.st_mode)]

        sftp.close()
        ssh.close()
        return folders, files
    except Exception as e:
        print(f"Error listing folder: {e}")
        return [], []
    

def list_files():
   
    try:
       ssh, sftp = get_sftp()
       file_list = sftp.listdir({FILE})
       
       #this runs command to list all folders in home directory
       #while connected to wsl 
       sftp.close()
       ssh.close()
       return file_list
    
    except Exception as e:
       print(f"Error connecting to WSL: {e}")
       return []
