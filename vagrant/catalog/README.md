This repository contains a fully functional webserver/app that tracks catalogs of various inventory items.  To run the webserver, you first need to install vagrant VM. Follow the instruction to install vagrant VM and instrunction to install the webserver 

Installing Vagrant VM ============================================
Install VirtualBox VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org(https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Install Vagrant Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com (https://www.vagrantup.com/downloads.html). Install the version for your operating system.

Download the VM configuration Fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm. You will end up with a new directory containing the VM files. Change to this directory in your terminal with cd. Inside, you will find another directory called vagrant. Change directory to the vagrant directory.

Start the VM From your terminal, inside the vagrant subdirectory, run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

Login into VM When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM

Installing/Running the webserver===================================
To install the webserver, simply clone the repository under vagrant directory by running following git clone command in vagrant directory 
git clone https://github.com/sungp/catalog.git catalog

cd into newly created catalog directory and run the webserver by running following command
python project.py

Open web browser (i.e. chrome) and navigate to http://locahost:8000.  If everything functioning correctly, it should display catalog web page.

