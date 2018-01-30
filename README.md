webteam-training
=============

Project code example for webteam-training for paly robotics

In order to run the code first install vagrant 
Installing Vagrant VM ============================================
* Install VirtualBox: VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org(https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

* Install Vagrant: Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com (https://www.vagrantup.com/downloads.html). Install the version for your operating system.

* Start Vagrant: Once vagrant installation is done, cd into vagrant directory (webteam/vagrant), run the command vagrant up. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

* Login to Vagrant: When vagrant up is finished running, you will get your shell prompt back. At this point, you can run vagrant ssh to log in to your newly installed Linux VM

Installing/Running the webserver===================================

* webserver.py

This webserver is created to demonstrate how simple webserver can be created using python. 

To run the server, from vagrant (after vagrant ssh), cd into /vagrant.  run webserver.py by running 'python webserver.py' command form the prompt.  Open your browser and type in http://localhost:8080/hello

* webserver-flask.py
This webserver is created to demonstrate basic functionality of flask

To run the server, from vagrant (after vagrant ssh), cd into /vagrant.  run webserver-flask.py by running 'python webserver-flask.py' command from the prompt.  Open your browser and type in http://localhost:8080

* webserver-flask-db.py
This webserver is created to demonstrate basic functionality of flask and how it can be used in conjuction with db (sqllite)

First setup the db by running "python database_setup.py"  and "python initpost.py". Running both command should create grouppost.db with some sample data.

To run the server, from vagrant (after vagrant ssh), cd into /vagrant.  run webserver-flask-db.py by running 'python webserver-flask-db.py' command from the prompt.  Open your browser and type in http://localhost:8080.  The page should display some sample post message


