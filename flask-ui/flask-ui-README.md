Currently SSH'ing into my WSL on local network. Will work core functionality here until NAS hardware stood up.
<br />
<br />



In order to run program, please confirm or install the following:

Generate an ssh key on the device you wish to connect to. Write the path down for further use. 

Download the folder "flask-ui" and place in easy to access directory on your machine.

Ensure you have VS Code installed on your machine.

Ensure you have Conda version 25.5.1 installed on your machine.

Create a conda environment as Python version 3.10.18 and activate.

Within this environment, pip install flask, gunicorn and paramiko.

Still within this environment, change directory to the location of the downloaded "flask-ui" folder.

Open and edit the ssh.py file to add a path for the global variables "FILE" and "USERNAME" such that they match what is on the device you wish to connect to.

Edit the variable "key_path" in the function get_sftp() to reflect the path you wrote down.

Run the command "python ui.py" (remove quotations)

Access the link generated in the command window.

