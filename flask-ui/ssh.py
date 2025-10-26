import paramiko, stat 
from flask import session

FILE = '/home/'
USERNAME = 'cbackus'


#establish SSH & SFTP connection
def get_sftp(username=USERNAME):
    host_name = 'localhost'
    port = 2222
    username = username
    key_path = 'C:/Users/pizza/.ssh/id_ed25519'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.Ed25519Key(filename=key_path)
    ssh.connect(hostname=host_name, port=port, username=username, pkey=private_key)
    sftp = ssh.open_sftp()
    return ssh, sftp


#returns lists of files and folders in directory
def get_files_and_folders(subfolder=''):
    try:
        ssh, sftp = get_sftp()
        base_path = FILE    #make whatever root folder is
        remote_path = f'{base_path}/{subfolder}'.rstrip('/')

        #reads user from session for use in path creation for file/folder lists
        user = session.get('user', None)
        if not user:
            raise Exception('Not logged in')
        
        remote_path = f'{base_path}/{subfolder}'.rstrip('/')

        all_items = sftp.listdir_attr(remote_path)

        #separate strings for template
        folders = [f.filename for f in all_items if stat.S_ISDIR(f.st_mode)]
        files   = [f.filename for f in all_items if stat.S_ISREG(f.st_mode)]

        sftp.close()
        ssh.close()
        return folders, files
    except Exception as e:
        print(f'Error listing folder: {e}')
        return [], []
