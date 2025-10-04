import os
import paramiko
import stat
from flask import Flask, render_template, request, send_file, redirect, url_for, Response
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
    subpath = request.args.get("path", "")  #relative to my_files

    try:
        folders, files = get_file_list_from_folder(subfolder=subpath)
    except Exception as e:
        print(f"Failed to list directory: {e}")
        return f"Failed to list directory: {e}", 500

    # Compute parent folder path
    if subpath == "" or subpath == FILE_FOLDER:
        parent_path = None  # we are at root, no parent
    else:
        # Remove last component of the path
        parent_path = "/".join(subpath.rstrip("/").split("/")[:-1])

    return render_template(
        "index.html",
        folders=folders,
        files=files,
        subpath=subpath,
        parent_path=parent_path
    )



#download file
@app.route('/download')
def download_file():
    filename = request.args.get('filename')
    subpath = request.args.get('path', '')  # folder user is in

    if not filename:
        return "No file specified", 400

    remote_path = f"/home/{USERNAME}/my_files/{subpath}/{filename}".replace("//", "/")


    try:
        ssh, sftp = get_sftp()

        # Open file from remote and stream its contents directly
        with sftp.open(remote_path, 'rb') as remote_file:
            file_data = remote_file.read()

        sftp.close()
        ssh.close()

        # Return file as download without saving locally
        return Response(
            file_data,
            mimetype='application/octet-stream',
            headers={
                'Content-Disposition': f'attachment;filename={filename}'
            }
        )

    except Exception as e:
        print(f"Download failed: {e}")
        return f"Download failed: {e}", 500
    

#upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    current_path = request.form.get('current_path', '').strip()  #make sure this matches HTML hidden input in upload file!

    if uploaded_file.filename == '':
        return redirect(url_for('index'))

    filename = uploaded_file.filename
    remote_path = f'/home/{USERNAME}/{FILE_FOLDER}/{current_path}/{filename}'.replace('//', '/')  #note variables from above

    try:
        ssh, sftp = get_sftp()
      
        # open remote file and write directly from uploaded file
        with sftp.open(remote_path, 'wb') as remote_file:
            remote_file.write(uploaded_file.read())

        sftp.close()
        ssh.close()
        return redirect(url_for('index', path=current_path))
    except Exception as e:
        print(f"Upload failed: {e}")
        return f"Upload failed: {e}", 500


#create folder
@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form.get('folder_name')
    current_path = request.form.get('current_path', '')  #make sure this matches HTML hidden input in create a new folder!

    if not folder_name:
        return "No folder name specified", 400

    # Construct correct full path: /home/USERNAME/FILE_FOLDER[/subpath]/folder_name
    remote_path = f"/home/{USERNAME}/{FILE_FOLDER}/{current_path}/{folder_name}".replace('//', '/')

    try:
        ssh, sftp = get_sftp()
        sftp.mkdir(remote_path)
        ssh.close()
        sftp.close()
        print(f"Created folder: {remote_path}")
    except Exception as e:
        print(f"Failed to create folder: {e}")
        return f"Failed to create folder: {e}", 500

    # Redirect back to the *current* directory
    return redirect(url_for('index', path=current_path))


if __name__ == '__main__':
    app.run(debug=True)
