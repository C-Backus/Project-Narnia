import paramiko, stat, json
from flask import session

IP_ADDRESS = ''    #change per server
ROOT_FILE = '/upload'


#establish SSH & SFTP connection with username & password passed from login.html
def get_sftp(username, password):
    host_name = IP_ADDRESS          #change per server
    port = 22                       #change per server (if needed)
    username = username             
    password = password             

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host_name, port=port, username=username, password=password)
    sftp = ssh.open_sftp()
    return ssh, sftp


#returns lists of files and folders in user root directory (no hidden folders/files)
def get_files_and_folders(username, password, subfolder=''):
    try:
        ssh, sftp = get_sftp(username, password)
        
        remote_path = f'{ROOT_FILE}/{subfolder}'.replace('//', '/')
        print(f'remote_path: {remote_path}')    #prints to conda env terminal

        #reads user from session for use in path creation for file/folder lists
        user = session.get('user', None)
        if not user:
            raise Exception('Not logged in')

        all_items = sftp.listdir_attr(remote_path)

        #separate strings for template & returns all files/folders that are not hidden
        folders = [f.filename for f in all_items if stat.S_ISDIR(f.st_mode) and not f.filename.startswith('.') and not f.filename.startswith('snap')]
        files = [f.filename for f in all_items if stat.S_ISREG(f.st_mode) and not f.filename.startswith('.')]

        sftp.close()
        ssh.close()
        return folders, files
    
    except Exception as e:
        print(f'Error listing folder: {e}')
        return [], []
