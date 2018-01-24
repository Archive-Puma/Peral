#! /usr/bi/env python
# -*- coding: utf-8 -*-

# ----------
#  Future modules
# ----------------
from __future__ import print_function

# ----------
#  Modules
# ----------------
import os
import json
import shlex
import platform
import subprocess

# ----------
#  From modules
# ----------------
from sys import argv
from builtins import input


# ----------
#  Terminal colors
# ----------------
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# ----------
#  Main functions
# ----------------
class Core:
    # ----------
    #  Initialization
    # ----------------
    def __init__(self):
        pass

    # ----------
    #  Repository Installation
    # ----------------
    def install(self, __db, __query, __os):
        found = False
        # ----------
        #  Search in the Database
        # ----------------
        for repository in __db['repos']:
            if not found and __query.lower() == repository['name'].lower():
                found = True
                # ----------
                #  Check permissions
                # ----------------
                if os.geteuid() == 0:
                    # ----------
                    #  Get Github link
                    # ----------------
                    gitlink = "https://github.com/{}/{}".format(
                        repository['author'], repository['name'])
                    gitclone_f = [
                        "git", "clone", gitlink, "/opt/{}".format(
                            repository['name'], ">", "/dev/null")
                    ]
                    # ----------
                    #  Print Setup Commands
                    # ----------------
                    print(color.BOLD + color.OKBLUE + "\n[*] SETUP COMMANDS:")
                    print("----------------------------------------------" +
                          color.ENDC)
                    print(color.WARNING + "git clone {}".format(gitlink) +
                          color.ENDC)
                    for cmd in repository['install'][0][__os]:
                        print(color.WARNING + cmd + color.ENDC)
                    print(
                        color.BOLD + color.OKBLUE +
                        "-----------------------------------------------------"
                        + color.ENDC)
                    # ----------
                    #  Confirm Setup Commands
                    # ----------------
                    confirm_install = input(
                        color.FAIL + color.BOLD +
                        "\n[!] Are you sure to install {}".format(
                            repository['name']) +
                        " executing this commands? [Y/n]: " + color.ENDC)
                    # ----------
                    #  Installation process
                    # ----------------
                    if confirm_install.lower() == 'y' or confirm_install == '':
                        # ----------
                        #  Open /dev/null
                        # ----------------
                        with open(os.devnull, 'w') as FNULL:
                            # ----------
                            #  Clone Github Repository
                            # ----------------
                            print("{}{}\n[*] Cloning repository into /opt/{}{}"
                                  .format(color.BOLD, color.OKBLUE,
                                          repository['name'], color.ENDC))
                            subprocess.call(
                                gitclone_f,
                                stdout=FNULL,
                                stderr=FNULL,
                                shell=False)
                            # ----------
                            #  Get real user name
                            # ----------------
                            real_user = str()
                            if 'SUDO_USER' in os.environ:
                                real_user = os.environ['SUDO_USER']
                            else:
                                real_user = os.environ['USER']
                            # ----------
                            #  Change folder owner
                            # ----------------
                            print("{}{}[*] Changing program owner{}".format(
                                color.BOLD, color.OKBLUE, color.ENDC))
                            chownR = "chown -R {} \"/opt/{}\"".format(
                                real_user, str(repository['name']))
                            subprocess.call(shlex.split(chownR))
                            os.chdir("/opt/{}".format(str(repository['name'])))
                            # ----------
                            #  Running post-download commands
                            # ----------------
                            print("{}{}[*] Running Setup Scripts...{}".format(
                                color.BOLD, color.OKBLUE, color.ENDC))
                            VARIABLE = int()
                            for cmd in repository['install'][0][__os]:
                                try:
                                    lcmd = shlex.split(cmd)
                                    # ----------
                                    #  Custom Command: INPUT
                                    # ----------------
                                    if cmd[:6] == "INPUT ":
                                        VARIABLE = input(
                                            "{}{}[-] {}{}".format(
                                                color.BOLD, color.OKGREEN,
                                                cmd[6:], color.ENDC))
                                    # ----------
                                    #  Custom Command: OUTPUT
                                    # ----------------
                                    elif cmd[:7] == "OUTPUT ":
                                        cmd = cmd[7:].replace(
                                            "<OUTPUT>", VARIABLE)
                                        lcmd = shlex.split(cmd)
                                        subprocess.call(
                                            lcmd, stdout=FNULL, shell=False)
                                    # ----------
                                    #  shell Command: echo
                                    # ----------------
                                    elif "echo" in cmd:
                                        '''
                                     !!!!!!!!!!!!!!!!!!!!
                                     !! DANGEROUS CODE !!
                                     !!!!!!!!!!!!!!!!!!!!
                                        '''
                                        os.system(cmd)
                                    # ----------
                                    #  Execute other commands
                                    # ----------------
                                    else:
                                        subprocess.call(
                                            lcmd,
                                            stdout=FNULL,
                                            stderr=FNULL,
                                            shell=False)
                                except Exception as e:
                                    print(e)
                            # ----------
                            #  Create a Syslink
                            # ----------------
                            if __os == "Linux":
                                # ----------
                                #  Ask to the user
                                # ----------------
                                syslink_comfirmation = input(
                                    "{}{}[?] Would you like to create ".format(
                                        color.BOLD, color.WARNING) +
                                    "a syslink named {}{}{}{}{}? [Y/n]: {}".
                                    format(color.UNDERLINE, repository['name']
                                           .lower(), color.ENDC, color.WARNING,
                                           color.BOLD, color.ENDC))
                                # ----------
                                #  Try to link the program
                                # ----------------
                                if syslink_comfirmation.lower == 'Y' or syslink_comfirmation == '':
                                    lk = "sudo ln -s {}/{} /usr/bin/{}".format(
                                        os.getcwd(), repository['main-script'],
                                        str(repository['name']).lower())
                                    llk = shlex.split(lk)
                                    try:
                                        subprocess.check_call(
                                            llk, stderr=FNULL, shell=False)
                                    # ----------
                                    #  Catch the exception
                                    # ----------------
                                    except subprocess.CalledProcessError:
                                        print("{}{}[!] Error: ".format(
                                            color.BOLD, color.FAIL) +
                                              "Please, delete or rename " +
                                              "/usr/bin/{}".format(
                                                  repository['name'].lower()))
                        # ----------
                        #  Installation confirmation
                        # ----------------
                        print("{}{}[*] {} has been successfully installed{}\n".
                              format(color.BOLD, color.HEADER,
                                     repository['name'], color.ENDC))
                # ----------
                #  Unprivileged error
                # ----------------
                else:
                    print("{}[!] You must be root!{}".format(
                        color.FAIL, color.ENDC))
        # ----------
        #  Repository not found
        # ----------------
        if not found:
            print("{}[!] Repository {} not found in the db. Try {} search {}".
                  format(color.FAIL, __query, argv[0], __query))

    # ----------
    #  Repository Uninstallation
    # ----------------
    def uninstall(self, __db, __query, __os):
        found = False
        for repository in __db['repos']:
            if not found and __query.lower() == repository['name'].lower():
                found = True
                # ----------
                #  Check permissions
                # ----------------
                if os.geteuid() == 0:
                    # ----------
                    #  Confirm Remove Commands
                    # ----------------
                    confirm_uninstall = input(
                        color.FAIL + color.BOLD +
                        "[!] Are you sure to uninstall {}? [y/N]: {}".format(
                            repository['name'], color.ENDC))
                    if confirm_uninstall.lower() == 'y':
                        # ----------
                        #  Linux desinstaller
                        # ----------------
                        if __os == "Linux":
                            # ----------
                            #  Common Commands
                            # ----------------
                            remove_lk = "rm -f /usr/bin/{}".format(
                                repository['name'].lower())
                            remove_repo = "rm -rf /opt/{}".format(
                                repository['name'])
                            lremove_lk = shlex.split(remove_lk)
                            lremove_repo = shlex.split(remove_repo)
                            # ----------
                            #  Desinstallation Process
                            # ----------------
                            print("{}{}[*] Removing syslinks...{}".format(
                                color.BOLD, color.WARNING, color.ENDC))
                            subprocess.call(lremove_lk, shell=False)
                            print("{}{}[*] Removing repository...{}".format(
                                color.BOLD, color.WARNING, color.ENDC))
                            subprocess.call(lremove_repo, shell=False)
                        # ----------
                        #  Desinstallation confirmation
                        # ----------------
                        print("{}{}[*] {} ".format(color.BOLD, color.HEADER,
                                                   repository['name']) +
                              "has been successfully uninstalled{}".format(
                                  color.ENDC))
                # ----------
                #  Unprivileged error
                # ----------------
                else:
                    print("{}[!] You must be root!{}".format(
                        color.FAIL, color.ENDC))
        # ----------
        #  Repository not found
        # ----------------
        if not found:
            print("{}[!] Repository {} not found in the db.{}".format(
                color.FAIL, __query, color.ENDC))

    # ----------
    #  Repository Cache
    # ----------------
    def search(self, __db, __query):
        # ----------
        #  Search in the Database
        # ----------------
        for repository in __db['repos']:
            if __query.lower() in repository['name'].lower():
                self.show(repository)

    # ----------
    #  Repository Print
    # ----------------
    def show(self, __repo):
        print("Name: {}".format(__repo['name']))
        print("Author: {}".format(__repo['author']))
        print("Description: {}".format(__repo['description']))
        print("Link: https://github.com/{}/{}".format(__repo['author'],
                                                      __repo['name']))


# ----------
#  User & OS information
# ----------------
class Info:
    # ----------
    #  Variables
    # ----------------
    __os__ = str()

    # ----------
    #  Initialization
    # ----------------
    def __init__(self):
        self.__os__ = platform.system()


# ----------
#  JSON functions
# ----------------
class Reader:
    # ----------
    #  Variables
    # ----------------
    __db = dict()
    __file = str()

    # ----------
    #  Initialization
    # ----------------
    def __init__(self, __file):
        self.__file = __file
        with open(__file, 'r') as open_json:
            self.__db = json.load(open_json)

    # ----------
    #  Misc. functions
    # ----------------

    def getjson(self):
        return self.__db
