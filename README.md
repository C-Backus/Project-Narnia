# Network Accessible Storage System
CS3300 Semester Project - Fall 2025

Authors: Collin Backus, Sean Gunnis

This software system is a tool intended to be used by those who are data privacy-aware. It provides a system level implementation of a a network accessible storage device and allows access to a large data storage device via same network access. While at face value, this may seem similar to various cloud server service provided by big name companies, there are some key distinctions: the user retains all ownership of the data storage device without having to rent cloud storage and retains control of the software itself. Additionally, there is no risk of a third party organization abusing their private and/or sensitive data. This was done by utilizing free and open-source software. 

Free and open-source: Ubuntu, Conda, Python pacakages

Free: VS Code

## Requirements
Due to the nature of the system as whole, it is up to the end-user to supply their own server hardware and access machines. There are no baseline specifications to run this software, however, it is reccomended that the server hardware be SSD storage devices and include a minimum 8 GB of RAM, and the access machines should be robust enough to execute moderate intensity programs. 

## Code Convention

This software system gives the means to access a Linux Ubuntu server machine through another machine running a Python Script. This Python script leverages the Flask framework to work off of a web-UI for user functionality and then connects to the server machine via SSH/SFTP protocols to execute whatever functionality the user is requesting.

The basic structure of the front end code in Python is to login and capture username and password during initial login, then every function will check if the user is logged in (in session), upon success, the function will execute the desired functionality as indicated by the user’s interaction with the html page. Executing the desired functionality is done by opening an SSH/SFTP connection with the server machine, running whatever command is needed, then closing the SSH/SFTP connection.

## Included Files

ui.py: Main Python executable script. Contains all user-functionality functions, depends on utils.py and forms.py

utils.py: Contains the get_sftp function and get_files_and_folders function. get_sftp establishes the SSH/SFTP connection to the server machine using the username and password passed to it from ui.py on initial user login. get_files_and_folders returns all files and folders in the current directory the user is in and returns them in separate lists to be displayed on the logged-in user’s page.

forms.py: Contains the single LoginForm class. This is filled with data from the login.html file as a user logs in on the web-UI. Then this data is accessed by the login function in ui.py to be sent to get_sftp.

base.html: Contains general formatting of the web-UI as seen by users.

index.html: Contains all user functionality of the web-UI. Depends on base.html.

login.html: This is the login page that is first shown upon initial running of program. Will also show after a user logs out. Depends on base.html.

## Known Issues and Undeveloped/Underdeveloped Features
•	The delete_item function only deletes empty directories currently. 
    
Need to write a function that deletes all items within directory and checks for more items to delete until directory is empty, then deletes directory itself. This might be best suited to a recursive function. Currently, users must delete everything within a folder before deleting the empty folder itself.

•	User creation can only be done on the server machine.
    
It would be very useful to be able to create users automatically from the access machine. This involves accessing the root user of the server machine to do so, which, from a security perspective, is less than ideal.

•	SSH connections are authenticated via username and password instead of SSH Pair keys. 

Yes, username and password authentication is technically less secure than SSH key authentication. This is not a problem in terms of scope of this system as a home network device. Additionally, the idea of using SSH key authentication for multiple users means storing those SSH keys somewhere in a dictionary or dictionary-like data structure. This was not feasible in our development timeline.

•	Secondary Layer of encryption on data transfer

Ubuntu 24.04 LTS already comes with standard encryption that can be enabled through the UFW (Uncomplicated Firewall). In the future, we would like to add another layer of encryption to the data transfer itself instead of just the data on the server. 

•	Front end Admin

A front end admin at higher level on the server so the other users can be remotely accessed by the admin user. 

•	Accessibility options

Allowing the user to change the color of the website and color/size of the text via the UI instead of opening code files would be ideal. This is currently unsupported.  


## Installation Guide

### On server machine

Download Ubuntu 24.04 LTS from Ubuntu’s official site onto a USB driver from any computer. https://ubuntu.com/download/desktop

Download Rufus onto your computer (Not the USB) In order to make a bootable drive for Ubuntu. https://rufus.ie/en/

Make sure you plug in your USB to your computer and launch Rufus. 

In Rufus select your USB drive then click select. This will open the file selector and click on your Ubuntu installation. At the bottom of the window click OK on all dialog boxes and wait for Rufus to complete. This can take around 5 minutes for the USB to be bootable. 

Restart your computer with USB plugged in and boot to the USB 

When onto the USB from the boot menu, click the UEFI boot if possible. 

There will be some accessibility options to go through based on your preferences. 

The next option you’ll see is Install Ubuntu or Try Ubuntu. Click Install Ubuntu. This screen only appears if you directly installed Ubuntu.

The next screen will be showing Interactive Installation and Automated Installation. Click Interactive Installation then click next.  

Next will be Default Selection or Extended Selections. Click Extended Selections. 

Next screen will be priority software will be recommended. Click all the boxes then click next

The next screen will be how do you want to install Ubuntu. There should be three options. Install Ubuntu alongside them, Erase disk and install Ubuntu, and Manual installation. Choose the option that best works for you.

The next screen will have you create a user and a few other accessibility options.

The final screen will be a breakdown of all the options you chose before on how you are installing Ubuntu. Click next and wait for the installer to finish

Reboot and you should be able to access the desktop.

From your Ubuntu desktop find the application for the Terminal. This is where we will be working from now on.

We are going to install openssh-server package. In the terminal type:

    sudo apt update

    sudo apt install openssh-server -y

Next we are going to create a SFTP directory to store the user data:

    sudo mkdir /sftpDataHome

    sudo chmod 701 /sftpDataHome

Next you are going to create a user and a group for our SFTP users. Type:

    sudo groupadd sftpGroup

The next will create a user and add them to the group. This can be done multiple times for more users.

    sudo useradd -g sftpGroup -d /sftpDataHome/username/DataDirectory -s /urs/sbin/nologin username

change the user’s password

    sudo passwd username

Create directory and home for the user:

    sudo mkdir -p /sftpDataHome/username/DataDirectory

    sudo chown -R root:sftpGroup /sftpDataHome/username

    sudo chown -R username:sftpGroup /sftpDataHome/username/DataDirectory

Modify the ssh config file to set up you sftp group

    Sudo nano /etc/ssh/sshd_config

Comment out:

    subsystem sftp /usr/lib/openssh/sftp-server

add the following to the bottom of the file:

    subsystem sftp internal-sftp

    Match Group sftpGroup

    ChrootDirectory /sftpDataHome/%u

    kbdInteractiveAuthentication yes

    PasswordAuthentication yes

    X11Forwarding no

    AllowTcpForwarding no

    AllowAgentForwarding no

    PermitTunnel no

    FoceCommand internal-sftp -d /DataDirectory

    press Ctrl+O then ENTER to save, then Ctrl+x to exit

Go to the Ubuntu Read Me for non-requirement set up

### Repeated User Creation and Deletion on Server Administrator

Repeated code in order

    sudo useradd -g sftpGroup -d /sftpDataHome/username/DataDirectory -s /usr/bin/nologin

    sudo passwd username

    sudo mkdir -p /sftpDataHome/username/DataDirectory

    sudo chown -R root:sftpGroup /sftpDataHome/username

    sudo chown -R username:sftpGroup/sftpDataHome/username/DataDirectory

### Delete a user

Keep information

    sudo deluser username

Delete user and data directory

    sudo deluser --remove-home username

Delete user and all their files

    sudo deluser --remove-all-files username

### On access machine(s)

Download the folder "flask-ui" and place in easy to access directory on your machine.

Ensure you have VS Code installed on your machine.

Ensure you have Conda version 25.5.1 installed on your machine.

Via command line interface (CLI), do the following:

Create a conda environment as Python version 3.10.18 and activate.

Within this environment, pip install flask, paramiko, and flask-wtf.

Still within this environment, change directory the downloaded "flask-ui" folder.

With VS Code, open and edit the utils.py file to add a path for the global variables IP_ADDRESS to reflect the IP address of the server machine. If necessary, change the port variable in get_sftp() to the port the server machine is using.

In ui.py, edit app.config['SECRET_KEY'] to be a secure string of your choice, edit DOWNLOAD_FOLDER to be the absolute file path that is desired for files to download to from the server. 

Via CLI, run the command 

    python ui.py

Access the link generated in the command window.

Log in using username and password created on the server. 

If shutting down system is desired, press Ctrl+c in the CLI window that the program is running in. All user data will be saved. **NOTE**: if there is user logged in when this occurs, the logged in user will *remain logged in upon next execution of the code!*

<br />

## Developer Documentation

The intent of this software is to make this a modular program that will execute on any machine with minimal changes in the code.

Each user and password must be created on the server. This will allow the access machine(s) to connect to the server with the ssh function and properly display the logging in user's folder architecture.

