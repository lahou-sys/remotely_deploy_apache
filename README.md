# REMOTELY DEPLOY APACHE (RDA)

REMOTELY DEPLOY APACHE AND DEPLOY WEBSITES FROM GITHUB AUTOMATICALLY TO REMOTE SERVERS

[![GitHub](https://img.shields.io/github/license/lahou-sys/remotely_deploy_apache)](LICENSE) ![GitHub contributors](https://img.shields.io/github/contributors/lahou-sys/remotely_deploy_apache)

# Table of Contents <a name="Table_of_Contents"></a>
* [Introduction](#INTRODUCTION)
    * [The project's objectives](#objectives)
* [Features](#FEATURES)
* [Requirements](#REQUIREMENTS)
    * [For the station which launches the script](#For_the_station)
        * [Package system used](#Package_system_used)
        * [Python Package used by the RDA script](#Python_Package)
        * [JSON input file](#JSON_input_file)
        * [Understanding JSON File Entries](#Understanding_JSON_File_Entries)
        * [Example of "info_in.json" file](#Example_of_info_in_json)
    * [For servers to install](#For_servers)
        *  [Using SUDO](#SUDO)
            *  [How to install SUDO](#How_to_install)
            *  [How to Add User to Sudoers](#How_to_Add)
        *  [Install openssh-client](#Install_openssh-client)
  * [How to use the RDA script](#How_to_use)
      * [Download the GitHub project](#Download_the_GitHub)
      * [Running the script RDA](#Running_the_script)
  * [Development](#Development)
  * [Todolist](#Todolist)
  * [License](#License)
  * [Contributor Covenant](#Contributor_Covenant)
  * [Contact](#Contact)




## INTRODUCTION <a name="INTRODUCTION"></a>



RDA est script Python qui automatise l'insatllation d'un serveur WEB distant sous Linux.

  - RDA currently works with Linux distributions from the Debian family.
  - RDA does the necessary system updates on the remote server.
  - RDA installs the Apache2 and Git packages on the remote server.
  - Information on the remote server (s) is given in a Json file.


### The project's objectives <a name="objectives"></a>

The main objective is to facilitate the work of system administrators in their daily tasks.
This RDA scripts will save time and reduce human errors in the deployment of one or more web servers within an IT infrastructure.
It can be improved or adapted for other administrative tasks than those it currently offers.


[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

## FEATURES <a name="FEATURES"></a>

  - Installs the Apaches and Git packages on the remote server.
  - Communication with remote servers is secure (SSH protocol).
  - Use of SUDO for launching remote commands.
  - Automatically create VHOST on the remote server.
  - Activation of the website on the remote server.
  - Deployment of the website from Github sources.
  - Test of the web service at the end of the installation for each remote server.

[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 


## REQUIREMENTS <a name="REQUIREMENTS"></a>
  - Recommended version of Python is v3.7 or newer.
  - The recommended version of the operating system: GNU / Linux with kernel 4.19.0 (tested without problem with Debian 10).
  - Installing the system packages listed above on the server running the RDA script.
  - Remote servers must be connected to a network and with internet access.
  - A system account with SUDO rights and authorizing SSH remote connections (the procedure for SUDO rights is below).
  - Have all the information for the Json input file  (explained below).

[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

### For the station which launches the script <a name="For_the_station"></a>

#### Package system used: <a name="Package_system_used"></a>
 
  - openssh-server and openssh-client
    - ssh-keygen
    - ssh-copy-id
    - ssh-keyscan
```ssh
$ sudo apt install openssh-server openssh-client
```
  - sshpass
```ssh
$ sudo apt install sshpass
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents)

####  Python Package used by the RDA script  <a name="Python_Package"></a>

Here are the Python modules used by the RDA script:

  - json
  - os
  - sys
  - subprocess
  - argparse
  - shutil
  - requests

  To install a module if it is not present on your system, here is the command to use:

```ssh
$ sudo python3 -m pip3 install SomePackage
```


[<div align="center">[Table of Contents]</div>](#Table_of_Contents)

#### JSON input file <a name="JSON_input_file"></a>

The input file must be in JSON format and named 'info_in.json'.
All fields for a server must be filled in, otherwise the script will stop with an error telling you which field is missing.


Here is the syntax of the JSON file:

```json
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
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

#### Understanding JSON File Entries: <a name="Understanding_JSON_File_Entries"></a>

| Variable | COMMENT |
| ------ | ------ |
| "srv1" | Tag of the server to install, it must be unique in the file. |
| "host" | IP address or hostname of the server to install. |
| "user" | Remote system account to use for installation. |
|"password" | Password of the remote "user" system account to be used for installation. |
| "port" | Remote SSH port to use, 22 by default. |
| "http_interface" | Interface on which the remote web server listens. |
| "http_port" | Network port on which the web server listens. |
| "servername" | This is the unique name that the virtual host is for, in this case the virtual host configuration block is for the www.example.com website. |
| "serveradmin" | This is an email address that is provided in error messages, allowing users to contact the web master of the web server. |
| "documentroot" | The document root is the directory where the content exists that Apache should serve when we visit the domain name, in this case going to www.example.com will direct us to files within the /var/www/example1 directory on the web server.  |
| "file_vhost"" | The name of the virtual host configuration file. It will be added to the remote server folder: /etc/httpd/conf.d/. Syntax: xxxxxx.conf |
| "url_source_website" | Github URL of the website source files to deploy. |


[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

#### Example of "info_in.json" file <a name="Example_of_info_in_json"></a>

Example for a server:

```json
{
      "serveur01":
        {"host": "10.0.2.4",
        "user": "admin",
        "password": "PassHall$",
        "port": "22",
        "http_interface": "10.0.2.4",
        "http_port": "80",
        "servername": "mywebsite.com",
        "serveradmin": "webmaster@mywebsite.com",
        "documentroot": "/var/www/mywebsite"},
        "file_vhost": "mywebsite.conf",
        "url_source_website": "https://github.com/sample/sample.git"}
}
```

Example for three servers:

```json
{
      "serveur01":
          {"host": "10.0.2.4",
          "user": "admin",
          "password": "PassHall$",
          "port": "22",
          "http_interface": "10.0.2.4",
          "http_port": "80",
          "servername": "mywebsite01.com",
          "serveradmin": "webmaster@mywebsite01.com",
          "documentroot": "/var/www/mywebsite01"},
          "file_vhost": "mywebsite02.conf",
          "url_source_website": "https://github.com/sample1/sample.git"},
        "serveur02":
          {"host": "10.0.2.5",
          "user": "admin",
          "password": "PassHall$",
          "port": "622",
          "http_interface": "127.0.0.1",
          "http_port": "80",
          "servername": "mywebsite02.com",
          "serveradmin": "webmaster@mywebsite02.com",
          "documentroot": "/var/www/mywebsite02"},
          "file_vhost": "mywebsite02.conf",
          "url_source_website": "https://github.com/sample2/sample.git"},
        "serveur03":
          {"host": "10.0.2.6",
          "user": "admin",
          "password": "PassHall$",
          "port": "6722",
          "http_interface": "*",
          "http_port": "80",
          "servername": "mywebsite03.com",
          "serveradmin": "webmaster@mywebsite03.com",
          "documentroot": "/var/www/mywebsite03"},
          "file_vhost": "mywebsite03.conf",
          "url_source_website": "https://github.com/sample3/sample.git"}
}
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

## For servers to install <a name="For_servers"></a>

### Using SUDO <a name="SUDO"></a>

#### How to install SUDO <a name="How_to_install"></a>

The command sudo allows you running programs with the security privileges of another user (commonly root).
SUDO is used by the RDA script to execute remote commands.

```ssh
$ sudo apt install sudo
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents)

####  How to Add User to Sudoers <a name="How_to_Add"></a>

To add the user to the group run the command below as root or another sudo user.
Make sure to change "username" to the name of the user you want to use with the RDA script.


```ssh
# usermod -aG sudo username
```


[<div align="center">[Table of Contents]</div>](#Table_of_Contents) 

### Install openssh-client  <a name="Install_openssh-client"></a>

In general, the openssh-client package is installed on the servers, it is important that it is installed on the servers to be installed so that the script can do the remote installation.
If not, install it with the following command.

```ssh
$ sudo apt install openssh-client
```



[<div align="center">[Table of Contents]</div>](#Table_of_Contents)

## How to use the RDA script <a name="How_to_use"></a>

### Download the GitHub project <a name="Download_the_GitHub"></a>

You have several methods to copy the project to your administration computer.

  - Download the ZIP archive directly with "wget"

 ```ssh
$ cd YourWorkDirectory
$ wget "https://github.com/lahou-sys/remotely_deploy_apache/archive/main.zip"
$ unzip main.zip
```   
  - Download the ZIP archive directly with "curl"

```ssh
$ cd YourWorkDirectory
$ curl -LO "https://github.com/lahou-sys/remotely_deploy_apache/archive/main.zip"
$ unzip main.zip
```
Output of the command "unzip":
```ssh
Archive:  main.zip
0a8331b2a3d897fd258e56b15490d9ce3a32ee5a
   creating: remotely_deploy_apache-main/
  inflating: remotely_deploy_apache-main/LICENSE  
  inflating: remotely_deploy_apache-main/README.md  
  inflating: remotely_deploy_apache-main/info_in.json  
  inflating: remotely_deploy_apache-main/remotely_deploy_apache.py
```
  - Clone the project on your local computer

Install the "git" package if it is not installed:

```ssh
$ sudo apt install git
```

Clone the project:

```ssh
$ cd YourWorkDirectory
$ git clone https://github.com/lahou-sys/remotely_deploy_apache.git
```

Output of the command "git":
```ssh
Clonage dans 'remotely_deploy_apache'...
remote: Enumerating objects: 32, done.
remote: Counting objects: 100% (32/32), done.
remote: Compressing objects: 100% (26/26), done.
remote: Total 32 (delta 17), reused 13 (delta 6), pack-reused 0
Dépaquetage des objets: 100% (32/32), fait.
```

[<div align="center">[Table of Contents]</div>](#Table_of_Contents)


### Running the script RDA <a name="Running_the_script"></a>

Running the RDA script is standalone, it just needs the "info_in.json" file to be fully completed and to be in the same RDA script folder.
The following "shebang" is entered for the RDA script, if it is different on your computer, please adapt it before running the script:

```ssh
#!/usr/bin/env python3
```

  - Launch of the RDA script

```ssh
$ cd YourWorkDirectory/remotely_deploy_apache
$ ./remotely_deploy_apache.py
```



The RDA script performs several tasks in a well-defined order.

  - It tests for the presence of the Python packages necessary for the RDA script
  - It tests the file "info_in.json"
  - It generates a pair of RSA SSH keys once
  - It installs the public key on the remote server(s)
  - System update of the remote server(s)
  - Install the Apache package on the remote server(s)
  - Adding and configuring a Vhost on the remote server(s)
  - Deploying the sources of a website from a Github repository on the remote server(s)
  - Test if the web server(s) are online


Example of the end of the RDA script output. We can see the number of servers processed and the status of the web service per server.


```ssh
...

################################################################################
TEST OF APACHE TO REMOTE SERVER

################################################################################
##########
Number of servers to install: 2
##########

########################################
##########
The server web 10.0.2.9 is OK
The server web 10.0.2.11 is OK
##########
```
Enjoy it !

[<div align="center">[Table of Contents]</div>](#Table_of_Contents)


## Development <a name="Development"></a>

Want to contribute? Great!

First, please consider contributing to RDA.
It's people like you who make RDA such a great tool.

Please consult the following [CONTRIBUTING.md](CONTRIBUTING.md) file to understand the procedure.

Also read the ["Contributor Covenant"](code_of_conduct.md) to complete the content of the CONTRIBUTING.md file.



[<div align="center">[Table of Contents]</div>](#Table_of_Contents)


## Todolist <a name="Todolist"></a>

 - Add the HTTPS option
 - Make the script compatible with other Linux distributions
 - Add the PHP option
 - Allow the script to take arguments as input

[<div align="center">[Table of Contents]</div>](#Table_of_Contents)

## License <a name="License"></a>
----

[MIT](LICENSE) 

## Contributor Covenant <a name="Contributor_Covenant"></a>

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](code_of_conduct.md) 

**Free Software, Hell Yeah!**

[<div align="center">[Table of Contents]</div>](#Table_of_Contents)

## Contact <a name="Contact"></a>

Mail : lbenmoulay@gmail.com