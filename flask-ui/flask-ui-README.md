Currently SSH'ing into my WSL on local network. Will work core functionality here until NAS hardware stood up.
<br />

# Installation Guide

### In order to run program, please confirm or install the following:

Generate an ssh key on the device you wish to connect to. Write the path down for further use. 

Download the folder "flask-ui" and place in easy to access directory on your machine.

Ensure you have VS Code installed on your machine.

Ensure you have Conda version 25.5.1 installed on your machine.

Via command line interface (CLI), do the following:

Create a conda environment as Python version 3.10.18 and activate.

Within this environment, pip install flask, gunicorn and paramiko, and flask-wtf.

Still within this environment, change directory to the location of the downloaded "flask-ui" folder.

With VS Code, open and edit the ssh.py file to add a path for the global variables "FILE" and "USERNAME" such that they match what is on the device you wish to connect to.

Edit the variable "key_path" in the function get_sftp() to reflect the path you wrote down.

Via CLI, run the command "python ui.py" (remove quotations)

Access the link generated in the command window.

If shutting down system is desired, press Ctrl+c in the CLI window that the program is running in. All data will be saved. **NOTE**: if there is a currently logged in user when this occurs, the logged in user will *remain logged in upon next execution of the code!*

<br />

## Developer Documentation

The intent of this software is to make this a modular program that will execute on any machine with minimal changes in the code.

Each user and password must be created on the Server. This will allow the user machine to connect to the Server with the ssh function and properly display the user's folder architecture.

Variables are snake_case, constants are SCREAMING_SNAKE_CASE
