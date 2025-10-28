'''
currently set up for /home/username folder view (not my_files) using username@localhost login style.
get_sftp() used w/o params in user_list and save_users (default param is USERNAME),
username variable sent in call in other funcs, works with cbackus as actively logging in user.

need from server: where are user passwords stored
How to create new users?


working on delete folder/file func
'''

import os, paramiko, stat, json
from flask import Flask, render_template, request, redirect, url_for, Response, session
from ssh import get_files_and_folders, get_sftp
from forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = ''           #allows accss to login page ((needs to be more secure later))

FILE_FOLDER = '' #redacted
USERNAME = '' #redacted
DOWNLOAD_FOLDER = ''   #routes directly to user's downloads folder #redacted
USER_PASS_FILE = f''    #user/password file #redacted


#login
@app.route('/login', methods=['GET', 'POST'])
def login():

    users = user_list()
    form = LoginForm()

    #retrieve username and password
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        #if new user, store username and generated password hash in json file, create user folder
        if username not in users:
            users[username] = generate_password_hash(password)
            save_users(users)

            user_folder = f'/home/{SERVER_NAME}/{username}'
            try:
                ssh, sftp = get_sftp(username)
                sftp.mkdir(user_folder)
                sftp.close()
                ssh.close()
                print(f'Created folder: {user_folder}')

                #user validated, show index
                session['user'] = username
                if form.validate_on_submit():
                    return redirect(url_for('index'))
            
            except Exception as e:
                print(f'Failed to create folder: {e}')
                return f'Failed to create folder: {e}', 500    #server error
            
        #if user in json file, check password
        if check_password_hash(users[username], password):
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid password', 400  #client error
            
    return render_template('login.html', form=form)


#logout
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))


#show file list
@app.route('/')
def index():

    #force redirect to login if not logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']

    subpath = request.args.get('path', '')  #folder user is in
    user_path = f'{subpath}'.strip('/')

    try:
        folders, files = get_files_and_folders(user_path)
        
    except Exception as e:
        print(f'Failed to list directory: {e}')
        return f'Failed to list directory: {e}', 500    #server error

    #find parent folder path
    if subpath == '' or subpath == user:
        parent_path = None  #we are at root
    else:
        #remove last piece of path
        parent_path = '/'.join(subpath.rstrip('/').split('/')[:-1])

    return render_template(
        'index.html',
        folders=folders,
        files=files,
        subpath=subpath,
        parent_path=parent_path,
        user=user
    )


#download file
@app.route('/download')
def download_file():
    
    #force redirect to login if not logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']

    filename = request.args.get('filename')
    path = request.args.get('path', '')  #folder user is in

    if not filename:
        return 'No file specified', 400     #client error

    #user folder path
    remote_path = f'/home/{username}/{path}/{filename}'.replace('//', '/')

    try:
        ssh, sftp = get_sftp(username)

        #open file from remote & stream its contents directly
        with sftp.open(remote_path, 'rb') as remote_file:
            file_data = remote_file.read()

        sftp.close()
        ssh.close()

        #return file as download w/o saving locally
        return Response(
            file_data,
            mimetype='application/octet-stream',
            headers={
                'Content-Disposition': f'attachment;filename={filename}'
            }
        )

    except Exception as e:
        print(f'Download failed: {e}')
        return f'Download failed: {e}', 500    #server error
    

#upload file
@app.route('/upload', methods=['POST'])
def upload_file():

    #force redirect to login if not logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']

    uploaded_file = request.files['file']
    current_path = request.form.get('current_path', '').strip()  #make sure this matches HTML hidden input in upload file!

    if uploaded_file.filename == '':
        return redirect(url_for('index'))

    filename = uploaded_file.filename

    #user folder path
    remote_path = f'/home/{username}/{current_path}/{filename}'.replace('//', '/')

    try:
        ssh, sftp = get_sftp(username)
      
        #open remote file & write directly from uploaded file
        with sftp.open(remote_path, 'wb') as remote_file:
            remote_file.write(uploaded_file.read())

        sftp.close()
        ssh.close()
        return redirect(url_for('index', path=current_path))
    except Exception as e:
        print(f'Upload failed: {e}')
        return f'Upload failed: {e}', 500    #server error


#create folder
@app.route('/create_folder', methods=['POST'])
def create_folder():

    #force redirect to login if not logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']

    folder_name = request.form.get('folder_name')
    current_path = request.form.get('current_path', '')  #make sure this matches HTML hidden input in create a new folder!

    if not folder_name:
        return 'No folder name specified', 400     #client error

    #user folder path
    remote_path = f'/home/{username}/{current_path}/{folder_name}'.replace('//', '/')


    try:
        ssh, sftp = get_sftp(username)
        sftp.mkdir(remote_path)
        ssh.close()
        sftp.close()
        print(f'Created folder: {remote_path}')
    except Exception as e:
        print(f'Failed to create folder: {e}')
        return f'Failed to create folder: {e}', 500    #server error

    #go back to the current directory (not root)
    return redirect(url_for('index', path=current_path))


#rename file/folder
@app.route('/rename', methods=['POST'])
def rename_item():
    
    #force redirect to login if not logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']

    current_path = request.form.get('current_path', '').strip()
    old_name = request.form.get('old_name', '').strip()
    new_name = request.form.get('new_name', '').strip()

    if not old_name or not new_name:
        return 'Old or new name not provided', 400     #client error
    
    #old & new user folder 
    old_remote_path = f'/home/{username}/{current_path}/{old_name}'.replace('//', '/')
    new_remote_path = f'/home/{username}/{current_path}/{new_name}'.replace('//', '/')


    try:
        ssh, sftp = get_sftp(username)
        sftp.rename(old_remote_path, new_remote_path)
        sftp.close()
        ssh.close()
        return redirect(url_for('index', path=current_path))
    except Exception as e:
        print(f'Rename failed: {e}')
        return f'Rename failed: {e}', 500    #server error
    

#delete file or folder
@app.route('/delete_item', methods=['POST'])
def delete_item():

    #force redirect to login if not logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    
    current_path = request.form.get('current_path', '').strip()
    filefolder = request.form.get('filefolder', '').strip()
    
    remote_path = f'/home/{username}/{current_path}/{filefolder}'.replace('//', '/')
    
    try:
        ssh, sftp = get_sftp(username)  
        remote_path_type = sftp.stat(remote_path)

        #check if path is folder or file & not hidden then remove
        if stat.S_ISREG(remote_path_type.st_mode) and not filefolder.startswith('.'):
            sftp.remove(remote_path)
        
        if stat.S_ISDIR(remote_path_type.st_mode) and not filefolder.startswith('.'):
            if not sftp.listdir(remote_path):
                sftp.rmdir(remote_path)

            else:
                print('Delete refused: folder has contents')
           
           
    except Exception as e:
        print(f'Remove failed: {e}')
        return f'Remove failed: {e}', 500    #server error

    sftp.close()
    ssh.close()
    return redirect(url_for('index', path=current_path))
    



if __name__ == '__main__':
    app.run(debug=True)
