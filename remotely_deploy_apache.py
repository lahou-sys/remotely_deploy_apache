#!/usr/bin/env python3

# coding: utf-8

'''
Author: Lahoucine BEN MOULAY

License:
    MIT License
    Copyright (c) 2020 Lahoucine BEN MOULAY
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
PRIV_SSH_DIR = "/home/%s/.ssh" % (CUR_USER)
BIN_DIR= "/usr/bin"

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
				{"host": "ip address",
				"user": "userunix",
				"password": "toto",
				"port": "22"},
			"srv2":
				{"host": "hostanme",
				"user": "alice",
				"password": "12345678",
				"port": "622"}
			}

		"""
		with open("info_in.json", "r") as f:
			dict_srv = json.load(f)
			return dict_srv


def remote_cmd(command,host,user,priv_ssh,port=22):
	#Description

		"""Launching a remote command using the SSH protocol.
			command: system command to run
			host: hostname or ip adress of remote server
			user: remote system account to use
			priv_ssh: ssh private key to use
			port: ssh network port to use

		"""
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
					command = "sshpass -p %s ssh-copy-id -p %s %s@%s" % (password, port, user, host)
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
			remote_cmd('echo %s | sudo -S apt update -y' % (password),host,user,priv_ssh,port)


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
			remote_cmd('echo %s | sudo -S apt upgrade -y' % (password),host,user,priv_ssh,port)


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
			remote_cmd('echo %s | sudo -S apt install apache2 -y' % (password),host,user,priv_ssh,port)


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
    
	dict_srv = list_srv()
	nbr_srv(dict_srv)
	gen_key()
	add_fingerprint(dict_srv)
	push_key(dict_srv)
	update_remote(dict_srv)
	upgrade_remote(dict_srv)
	install_remote_apache(dict_srv)
	nbr_srv(dict_srv)
	test_http_srv(dict_srv)

# Running the script

if __name__ == "__main__":
    main()
