# Network Accessible Storage System
CS3300 Semester Project - Fall 2025

Authors: Collin Backus, Sean Gunnis

This software system is a tool intended to be used by those who are data privacy-aware. It provides a system level implementation of a a network accessible storage device and allows access to a large data storage device via same network access. While at face value, this may seem similar to various cloud server service provided by big name companies, there are some key distinctions: the user retains all ownership of the data storage device without having to rent cloud storage and retains control of the software itself. Additionally, there is no risk of a third party organization abusing their private and/or sensitive data. This was done by utilizing free and open-source software. 

Free and open-source: Ubuntu, Conda, Python pacakages

Free: VS Code

## Requirements
Due to the nature of the system as whole, it is up to the end-user to supply their own server hardware and access machines. There are no baseline specifications to run this software, however, it is reccomended that the server hardware be SSD storage devices and include a minimum 8 GB of RAM, and the access machines should be robust enough to execute moderate intensity programs. 


## Installation Guide

### On server machine

*Insert Linux server requirements here*

### On access machine(s)

Download the folder "flask-ui" and place in easy to access directory on your machine.

Ensure you have VS Code installed on your machine.

Ensure you have Conda version 25.5.1 installed on your machine.

Via command line interface (CLI), do the following:

Create a conda environment as Python version 3.10.18 and activate.

Within this environment, pip install flask, gunicorn and paramiko, and flask-wtf.

Still within this environment, change directory to the location of the downloaded "flask-ui" folder.

With VS Code, open and edit the ~ssh.py~ utils.py file to add a path for the global variables IP_ADDRESS to reflect the IP address of the server machine,  ~"FILE_FOLDER" and "USER_FOLDER"~ *update for final release* .

Via CLI, run the command "python ui.py" (remove quotations)

Access the link generated in the command window.

Log in using username and password created on the server. 

If shutting down system is desired, press Ctrl+c in the CLI window that the program is running in. All data will be saved. **NOTE**: if there is user logged in when this occurs, the logged in user will *remain logged in upon next execution of the code!*

<br />

## Developer Documentation

The intent of this software is to make this a modular program that will execute on any machine with minimal changes in the code.

Each user and password must be created on the server. This will allow the user machine to connect to the server with the ssh function and properly display the user's folder architecture.

Variables are snake_case, constants are SCREAMING_SNAKE_CASE

