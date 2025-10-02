import os
import paramiko
from flask import Flask, render_template, request, send_file, redirect, url_for
from ssh import list_files, get_file_list_from_folder, get_sftp

app = Flask(__name__)
#UPLOAD_FOLDER = 'uploads'       not working
#os.makedirs(UPLOAD_FOLDER, exist_ok=True)  #make uploads folder if not there

FILE_FOLDER = 'my_files'
USERNAME = '' #redacted
DOWNLOAD_FOLDER = ''   #routes directly to user's downloads folder #redacted


#show file list
@app.route('/')
def index():
    files =  get_file_list_from_folder(FILE_FOLDER)   #for ssh file list in specific folder
    return render_template('index.html', files=files)  # loads templates/index.html

#download file
@app.route('/download')
def download_file():
    filename = request.args.get('filename')
    if not filename:
        return "No filename specified", 400

    folder = FILE_FOLDER  #same folder you list from
    local_path = os.path.join(DOWNLOAD_FOLDER, filename)
    remote_path = f'/home/{USERNAME}/{FILE_FOLDER}/{filename}'  #note variables from above

    try:
        ssh, sftp = get_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()
        ssh.close()
        return f"Saved {filename} to {local_path}"
    except Exception as e:
        print(f"Download failed: {e}")
        return f"Download failed: {e}", 500

#upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return redirect(url_for('index'))

    filename = uploaded_file.filename
    remote_path = f'/home/{USERNAME}/{FILE_FOLDER}/{filename}'  #note variables from above

    try:
        ssh, sftp = get_sftp()
      
        # open remote file and write directly from uploaded file
        with sftp.open(remote_path, 'wb') as remote_file:
            remote_file.write(uploaded_file.read())

        sftp.close()
        ssh.close()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Upload failed: {e}")
        return f"Upload failed: {e}", 500



if __name__ == '__main__':
    app.run(debug=True)
