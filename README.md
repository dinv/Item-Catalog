# Catalog

## Setup
1) Install Vagrant and VirtualBox

2) Launch the Vagrant VM (vagrant up)

3) Log in to the VM (vagrant ssh)

4) Change directory to /vagrant (cd /vagrant)

5) Run database setup files (python database_setup.py && python populate_database.py)

5) Run the application within the VM (python project.py)

6) Access the application by visiting http://localhost:8000 locally

### Note
The vagrant file has a line that has been specially modified for OSx compatibility
https://github.com/chef/bento/issues/661

