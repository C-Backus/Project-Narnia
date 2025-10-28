'''
need from server: key_path, host_name, port 
'''

import paramiko, stat, json
from flask import session

FILE = '' #redacted
SERVER_NAME = '' #redacted
FILE_FOLDER = '' #redacted

#list users from json file
def user_list():
    try:
        ssh, sftp = get_sftp()

        with sftp.open(f'/home/{SERVER_NAME}/{FILE_FOLDER}/userpass.json', 'r') as f:
            users = json.load(f)

        sftp.close()
        ssh.close()
        return users
    
    except Exception as e:
        print(f'Failed to list users: {e}')
        return {}  #if exception, return empty dict

        
#save user dictionary to json file (overwrites)
def save_users(users):
    try:
        ssh, sftp = get_sftp()

        with sftp.open(f'/home/{SERVER_NAME}/{FILE_FOLDER}/userpass.json', 'w') as f:
            f.write(json.dumps(users))

        sftp.close()
        ssh.close()
        return users
    
    except Exception as e:
        print(f'Failed to save user list: {e}')


#establish SSH & SFTP connection
def get_sftp(username=SERVER_NAME):
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


#returns lists of files and folders in user root directory (no hidden folders/files)
def get_files_and_folders(subfolder='', username=SERVER_NAME):
    try:
        ssh, sftp = get_sftp()
        base_path = f'{FILE}/{username}'    #make whatever root folder is
        remote_path = f'{base_path}/{subfolder}'.rstrip('/')

        #reads user from session for use in path creation for file/folder lists
        user = session.get('user', None)
        if not user:
            raise Exception('Not logged in')
        
        remote_path = f'{base_path}/{subfolder}'.rstrip('/')

        all_items = sftp.listdir_attr(remote_path)

        #separate strings for template & returns all files/folders that are not hidden
        folders = [f.filename for f in all_items if stat.S_ISDIR(f.st_mode) and not f.filename.startswith('.')]
        files = [f.filename for f in all_items if stat.S_ISREG(f.st_mode) and not f.filename.startswith('.')]

        sftp.close()
        ssh.close()
        return folders, files
    except Exception as e:
        print(f'Error listing folder: {e}')
        return [], []
