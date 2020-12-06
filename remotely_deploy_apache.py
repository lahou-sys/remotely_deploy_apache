#!/usr/bin/env python3

# coding: utf-8

'''
Author: Lahoucine BEN MOULAY

License:
    MIT License
    Copyright (c) 2020 lahou-sys
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
'''

"""
Uses the ssh-keygen, ssh-copy-id, ssh-keyscan, sshpass and ssh commands found on systems.
Mac Users will need to install ssh-copy-id before attempting to use this script.
"""


###############
# Import modules
###############

"""Test if the modules exist for import , if not stop the script.
	
"""

module_names = ["json","os","sys","subprocess","argparse","shutil","requests"]


for mod in module_names:
	try:
		__import__(mod)
	except ImportError:
		print(f"""You need {mod}!
				install it from http://pypi.python.org/pypi/{mod}
				or run pip install {mod}.""")
		raise

"""Import of modules
	
"""

import json
import os
import sys
import subprocess
import argparse
import shutil
import requests

###############
# Constants
###############

CUR_USER = os.getlogin()
HOME_USER = os.path.expanduser("~")
PRIV_SSH_DIR = HOME_USER + "/.ssh"
BIN_DIR = "/usr/bin"
WORK_DIR = os.path.dirname(sys.argv[0]) 


###############
# Fonctions
###############

def show(msg):
	#Description

		"""Local print() function.

		"""
		print(msg)


def list_srv():
	#Description

		"""Dictionary creation using the external json file
			The json file is in the same folder as this script.
			The file must have this structure for example:
			{
			"srv1":
				{"host": "ip address or hostname",
				"user": "userunix",
				"password": "toto",
				"port": "22",
				"http_interface": "*",
				"http_port": "80",
				"servername": "ip address or FQN or domain name",
				"serveradmin": "webmaster@example.com",
				"documentroot": "/var/www/site1"},
				"file_vhost": "site1.conf",
				"url_source_website": "https://github.com/xxxxxx/xxxxx.git"},
			"srv2":
				{"host": "hostanme",
				"user": "alice",
				"password": "12345678",
				"port": "622",
				"http_interface": "ip address",
				"http_port": "8080",
				"servername": "ip address or FQN or domain name",
				"serveradmin": "webmaster@example.com",
				"documentroot": "/var/www/site2",
				"file_vhost": "site2.conf",
				"url_source_website": "https://github.com/xxxxxx/xxxxx.git"}
			}

		"""
		with open("info_in.json", "r") as f:
			dict_srv = json.load(f)
			return dict_srv

def test_exist_json():
	#Description

		"""Test if the file exists in the script's working directory.

		"""
		os.chdir(WORK_DIR)
		try:
			with open("info_in.json", "r") as f:
				pass
		except FileNotFoundError:
			print("""The file "info_in.json" is not present in the script's working directory.
					Please consult the documentation...""")
			raise



def test_input_json(dict_srv):
	#Description

		"""Test the entries in the json file.

		"""
		dict_srv_template = {"host": "", \
				"user": "", \
				"password": "", \
				"port": "", \
				"http_interface": "", \
				"http_port": "", \
				"servername": "", \
				"serveradmin": "", \
				"documentroot": "", \
				"file_vhost": "", \
				"url_source_website": ""}

		for item in dict_srv.keys():
			for key in dict_srv_template.keys():
				if not key in dict_srv[item]:
					try:
						print(dict_srv[key])
						break
					except KeyError:
						print(f"""The "{key}" for server "{item}": this information is missing or incorrectly entered in the "info_in.json" file.
							Please consult the documentation...""")
						raise


def remote_cmd(command,host,user,priv_ssh,port=22):
	#Description

		"""Launching a remote command using the SSH protocol.
			command: system command to run
			host: hostname or ip adress of remote server
			user: remote system account to use
			priv_ssh: ssh private key to use
			port: ssh network port to use

		"""
		show("In progrees...")
		cmd_ssh = shutil.which('ssh')
		cmd = "%s -i %s -p %s %s@%s '%s'" % (cmd_ssh,priv_ssh,port,user,host,command)
		subprocess.call(cmd, shell=True)



def key_present():
	#Description

		"""Checks to see if there is an RSA already present. Returns a bool.

		"""
		if "id_rsa" in os.listdir(PRIV_SSH_DIR):
			return True
		else:
			return False


def gen_key():
	#Description
		"""Generate a SSH Key.

		"""
		os.chdir(PRIV_SSH_DIR)
		if key_present():
			show("A key is already present.")
		else:
		# Genarate private key
			if "ssh-keygen" in os.listdir(BIN_DIR):
				subprocess.call('ssh-keygen -t rsa -b 4096 -f ./id_rsa -N "''" ', shell=True)
			else:
				show("ssh-keygen required.")


def add_fingerprint(dict_srv):
	#Description

		"""Add the remote SSH fingerprint to the local machine.
			The variables are the list of servers to install.

		"""
		os.chdir(PRIV_SSH_DIR)
		if "ssh-keyscan" in os.listdir(BIN_DIR):
			for item in dict_srv:
				srv = dict_srv[item]
				host = dict_srv[item]["host"]
				port = dict_srv[item]["port"]
				show(f'Add the remote SSH fingerprint to the local machine : / {host}')
				command = "ssh-keyscan -p %s -H %s >> ./known_hosts" % (port, host)
				subprocess.call(command, shell=True)
		else:
			show("ssh-keyscan required.")


def push_key(dict_srv):
	#Description

		"""Push a SSH Key to a remote server.
			The variables are the list of servers to install.

		"""
		os.chdir(PRIV_SSH_DIR)
		if key_present():
			if "ssh-copy-id" in os.listdir(BIN_DIR) and "sshpass" in os.listdir(BIN_DIR):
				for item in dict_srv:
					srv = dict_srv[item]
					host = dict_srv[item]["host"]
					port = dict_srv[item]["port"]
					user = dict_srv[item]["user"]
					password = dict_srv[item]["password"]
					show(f'SSH key found. Pushing key to remote server : {host}')
					command = "sshpass -p %s ssh-copy-id -f -p %s %s@%s" % (password, port, user, host)
					subprocess.call(command, shell=True)
			else:
				show("ssh-copy-id and sshpass required.")
		else:
			show("A SSH key is required. Run script again with action set as GenKey")


def nbr_srv(srv_list):
	#Description

		"""Displays the number of servers to install.
			The variables are the list of servers to install.

		"""
		nbr_serveur = len(srv_list)
		show(10*'#')
		show(f'Number of servers to install: {nbr_serveur}')
		show(10*'#')


def update_remote(dict_srv):
	#Description

		"""Starts the Update cache of remote servers updates.
			The variables are the list of servers to install.
       
		"""
		for item in dict_srv:
			srv = dict_srv[item]
			host = dict_srv[item]["host"]
			port = dict_srv[item]["port"]
			user = dict_srv[item]["user"]
			priv_ssh = "%s/id_rsa" % (PRIV_SSH_DIR)
			password = dict_srv[item]["password"]
			show(f'Update to remote server : {host}')
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." apt-get -qq update -y' % (password),host,user,priv_ssh,port)
			show("\n")


def upgrade_remote(dict_srv):
	#Description

		"""Starts the System Update for remote servers.
			The variables are the list of servers to install.

		"""
		for item in dict_srv:
			srv = dict_srv[item]
			host = dict_srv[item]["host"]
			port = dict_srv[item]["port"]
			user = dict_srv[item]["user"]
			priv_ssh = "%s/id_rsa" % (PRIV_SSH_DIR)
			password = dict_srv[item]["password"]
			show(f'Upgrade to remote server : {host}')
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." apt-get -qq upgrade -y' % (password),host,user,priv_ssh,port)
			show("\n")


def install_remote_apache(dict_srv):
	#Description

		"""Install the Apache2 package on the remote servers.
			The variables are the list of servers to install.

		"""
		for item in dict_srv:
			srv = dict_srv[item]
			host = dict_srv[item]["host"]
			port = dict_srv[item]["port"]
			user = dict_srv[item]["user"]
			priv_ssh = "%s/id_rsa" % (PRIV_SSH_DIR)
			password = dict_srv[item]["password"]
			show(f'Install package Apache to remote server : {host}')
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." apt-get install -qq apache2 -y' % (password),host,user,priv_ssh,port)
			show("\n")


def create_vhost_documentroot(dict_srv):
	#Description

		"""Creation of the folder hosting the website files.

		"""
		for item in dict_srv:
			host = dict_srv[item]["host"]
			port = dict_srv[item]["port"]
			user = dict_srv[item]["user"]
			priv_ssh = "%s/id_rsa" % (PRIV_SSH_DIR)
			password = dict_srv[item]["password"]
			documentroot = dict_srv[item]["documentroot"]
			show(f'Create the folder hosting the website files : {host}')
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." mkdir -p %s' % (password, documentroot),host,user,priv_ssh,port)
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." chown -R www-data: %s' % (password, documentroot),host,user,priv_ssh,port)
			show("\n")


def create_remote_vhost_file(dict_srv):
	#Description

		"""creation of the remote vhost file.

		"""
		for item in dict_srv:
			host = dict_srv[item]["host"]
			port = dict_srv[item]["port"]
			user = dict_srv[item]["user"]
			priv_ssh = "%s/id_rsa" % (PRIV_SSH_DIR)
			password = dict_srv[item]["password"]
			documentroot = dict_srv[item]["documentroot"]
			http_interface = dict_srv[item]["http_interface"]
			http_port = dict_srv[item]["http_port"]
			servername = dict_srv[item]["servername"]
			serveradmin = dict_srv[item]["serveradmin"]
			file_vhost = dict_srv[item]["file_vhost"]
			dir_conf_vhost = "/etc/apache2/sites-available/"
			vhost_file_tmp = "/tmp/" + file_vhost
			print(vhost_file_tmp)
			with open(vhost_file_tmp, "w") as f:
				f.write('<VirtualHost %s:%s>\n' % (http_interface, http_port))
				f.write('\tServerName %s\n' % (servername))
				f.write('\tServerAdmin %s\n' % (serveradmin))
				f.write('\tDocumentRoot %s\n' % (documentroot))
				f.write('\n')
				f.write('\t<Directory %s>\n' % (documentroot))
				f.write('\t\tOptions -Indexes +FollowSymLinks\n')
				f.write('\t\tAllowOverride All\n')
				f.write('\t</Directory>\n')
				f.write('\n')
				f.write('\tErrorLog ${APACHE_LOG_DIR}/%s.log\n' % (servername))
				f.write('\tCustomLog ${APACHE_LOG_DIR}/%s.log combined\n' % (servername))
				f.write('</VirtualHost>')
				f.close()
			show(f'Create the remote vhost file: {host}')
			command = "scp -i %s -P %s %s %s@%s:/tmp/" % (priv_ssh, port, vhost_file_tmp, user, host)
			subprocess.call(command, shell=True)
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." mv /tmp/%s %s' % (password, file_vhost, dir_conf_vhost),host,user,priv_ssh,port)
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." chown -R root: %s/%s' % (password, dir_conf_vhost, file_vhost),host,user,priv_ssh,port)
			os.remove(vhost_file_tmp)
			show("\n")


def disable_remote_site_default(dict_srv):
	#Description

		"""Disable apache default site.

		"""
		for item in dict_srv:
			host = dict_srv[item]["host"]
			port = dict_srv[item]["port"]
			user = dict_srv[item]["user"]
			priv_ssh = "%s/id_rsa" % (PRIV_SSH_DIR)
			password = dict_srv[item]["password"]
			show(f'Disable apache default site : {host}')
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." a2dissite *default*' % (password),host,user,priv_ssh,port)
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." systemctl reload apache2' % (password),host,user,priv_ssh,port)
			show("\n")


def deploy_website_with_git(dict_srv):
	#Description

		"""Deploy the website sources on the remote server.

		"""
		for item in dict_srv:
			host = dict_srv[item]["host"]
			port = dict_srv[item]["port"]
			user = dict_srv[item]["user"]
			priv_ssh = "%s/id_rsa" % (PRIV_SSH_DIR)
			password = dict_srv[item]["password"]
			documentroot = dict_srv[item]["documentroot"]
			url_source_website = dict_srv[item]["url_source_website"]
			show(f'Deploy the website sources on the remote server : {host}')
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." apt-get -qq -y install git' % (password),host,user,priv_ssh,port)
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." rm -rf %s/*' % (password, documentroot),host,user,priv_ssh,port)
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." rm -rf %s/.* 2> /dev/null' % (password, documentroot),host,user,priv_ssh,port)
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." git clone %s %s > /dev/null' % (password, url_source_website, documentroot),host,user,priv_ssh,port)
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." chown -R www-data: %s/*' % (password, documentroot),host,user,priv_ssh,port)
			show("\n")


def enable_remote_site_(dict_srv):
	#Description

		"""Enable apache deployed site.

		"""
		for item in dict_srv:
			host = dict_srv[item]["host"]
			port = dict_srv[item]["port"]
			user = dict_srv[item]["user"]
			priv_ssh = "%s/id_rsa" % (PRIV_SSH_DIR)
			password = dict_srv[item]["password"]
			file_vhost = dict_srv[item]["file_vhost"]
			show(f'Enable apache deployed site : {host}')
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." a2ensite %s' % (password, file_vhost),host,user,priv_ssh,port)
			remote_cmd('echo -e "%s\n" | sudo -S -p "....." systemctl reload apache2' % (password),host,user,priv_ssh,port)
			show("\n")


def url_check(url):
       #Description

       """Boolean return - check to see if the site exists.
          This function takes a url as input and then it requests the site 
          head - not the full html and then it checks the response to see if 
          it's less than 400. If it is less than 400 it will return TRUE 
          else it will return False.

       """
       try:
               site_ping = requests.head(url)
               if site_ping.status_code < 400:
                   #  To view the return status code, type this   :   **print(site.ping.status_code)** 
                   return True
               else:
                   return False
       except Exception:
           return False


def test_http_srv(dict_srv):
	#Description

		"""Test if the installed web servers are online.
			The variables are the list of servers to install

		"""
		show(10*'#')
		for item in dict_srv:
			host = dict_srv[item]["host"]
			if url_check('http://%s' % (host)):
				show('The server web %s is OK' % (host))
			else:
				show('The server web %s is KO' % (host))
		show(10*'#')


def main():
	#Description
	"""Start of script.
	
	"""
	decorateur = "\n" + 80*'#'
	decorateur_min = "\n" + 40*'#'
	
	show(decorateur)
	show("TEST THE JSON FILE EXIST")
	show(decorateur)
	test_exist_json()
	show(decorateur_min)
	dict_srv = list_srv()
	test_input_json(dict_srv)
	show(decorateur_min)
	nbr_srv(dict_srv)
	show(decorateur)

	show(decorateur)
	show("GENERATE RSA KEY")
	show(decorateur)
	gen_key()
	show(decorateur)

	show(decorateur)
	show("PUSH RSA KEY")
	show(decorateur)
	add_fingerprint(dict_srv)
	show(decorateur_min)
	push_key(dict_srv)
	show(decorateur)

	show(decorateur)
	show("'UPDATE' AND 'UPGRADE' REMOTE SERVER")
	show(decorateur)
	update_remote(dict_srv)
	show(decorateur_min)
	upgrade_remote(dict_srv)
	show(decorateur)

	show(decorateur)
	show("INSTALL APACHE TO REMOTE SERVER")
	show(decorateur)
	install_remote_apache(dict_srv)
	show(decorateur)

	show(decorateur)
	show("CONFIGURATION OF APACHE TO REMOTE SERVER")
	show(decorateur)
	create_vhost_documentroot(dict_srv)
	show(decorateur_min)
	create_remote_vhost_file(dict_srv)
	show(decorateur_min)
	disable_remote_site_default(dict_srv)
	show(decorateur)

	show(decorateur)
	show("DEPLOY SOURCE WEBSITE FROM GITHUB")
	show(decorateur)
	deploy_website_with_git(dict_srv)
	show(decorateur_min)
	enable_remote_site_(dict_srv)
	show(decorateur)
	
	show(decorateur)
	show("TEST OF APACHE TO REMOTE SERVER")
	show(decorateur)
	nbr_srv(dict_srv)
	show(decorateur_min)
	test_http_srv(dict_srv)
	show(decorateur)

# Running the script

if __name__ == "__main__":
    main()
