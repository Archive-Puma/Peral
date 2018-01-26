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
import hashlib
import platform
import subprocess

# ----------
#  From modules
# ----------------
from sys import argv
from builtins import input

# ----------
#  Variables
# ----------------
db_name = "octopus_db.json"


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
    def install(self, __db, __query, __os, __args):
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
                    tools_folder = str()
                    # ----------
                    #  Peral Tools Installation Folder
                    # ----------------
                    if __os == "Linux":
                        tools_folder = "/opt/peral_tools/"
                    # ----------
                    #  Get Github link
                    # ----------------
                    gitlink = "https://github.com/{}/{}".format(
                        repository['author'], repository['name'])
                    gitclone_f = [
                        "git", "clone", gitlink, "{}{}".format(
                            tools_folder, repository['name'], ">", "/dev/null")
                    ]
                    # ----------
                    #  Print Setup Commands
                    # ----------------
                    if not __args.quiet:
                        has_init_command = False
                        print(color.BOLD + color.OKBLUE +
                              "\n[*] SETUP COMMANDS:")
                        print("----------------------------------------------"
                              + color.ENDC)
                        print(color.WARNING + "git clone {}".format(gitlink) +
                              color.ENDC)
                        for cmd in repository['install'][0][__os]:
                            if "INIT " == cmd[:5]:
                                has_init_command = True
                            print(color.WARNING + cmd + color.ENDC)
                        print(
                            color.BOLD + color.OKBLUE +
                            "-----------------------------------------------------"
                            + color.ENDC)
                    # ----------
                    #  Confirm Setup Commands
                    # ----------------
                    confirm_install = ''
                    if not __args.yes:
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
                            if not __args.quiet:
                                print(
                                    "{}{}\n[*] Cloning repository into {}{}{}"
                                    .format(color.BOLD, color.OKBLUE,
                                            tools_folder, repository['name'],
                                            color.ENDC))
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
                            if not __args.quiet:
                                print(
                                    "{}{}[*] Changing program owner{}".format(
                                        color.BOLD, color.OKBLUE, color.ENDC))
                            chownR = "chown -R {} \"{}{}\"".format(
                                real_user, tools_folder, repository['name'])
                            subprocess.call(shlex.split(chownR))
                            os.chdir("{}{}".format(tools_folder,
                                                   repository['name']))
                            # ----------
                            #  Clear & Create Init Scripts
                            # ----------------
                            if has_init_command:
                                try:
                                    subprocess.check_output(
                                        ["[", "-f", "initperal.sh", "]"])
                                    print("El directorio si que existe")
                                    subprocess.check_output(
                                        ["rm", "-f", "initperal.sh"])
                                except subprocess.CalledProcessError:
                                    pass
                                subprocess.call(["touch", "initperal.sh"])
                                subprocess.call(
                                    ["chown", real_user, "initperal.sh"])
                                subprocess.call(
                                    ["chmod", "+x", "initperal.sh"])
                            # ----------
                            #  Running post-download commands
                            # ----------------
                            if not __args.quiet:
                                print("{}{}[*] Running Setup Scripts...{}".
                                      format(color.BOLD, color.OKBLUE,
                                             color.ENDC))
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
                                    #  Custom Command: INIT
                                    # ----------------
                                    elif cmd[:5] == "INIT ":
                                        with open("initperal.sh",
                                                  "a") as script:
                                            cmd = cmd.replace(
                                                "<PWD>", os.getcwd())
                                            script.write(
                                                "{}\n".format(cmd[5:]))
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
                                syslink_comfirmation = ''
                                if not __args.yes:
                                    syslink_comfirmation = input(
                                        "{}{}[?] Would you like to create ".
                                        format(color.BOLD, color.WARNING) +
                                        "a syslink named {}{}{}{}{}? [Y/n]: {}".
                                        format(
                                            color.UNDERLINE, repository['name']
                                            .lower(), color.ENDC, color.
                                            WARNING, color.BOLD, color.ENDC))
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
                                        if not __args.quiet:
                                            print(
                                                "{}{}[!] Error: Please, delete".
                                                format(color.BOLD, color.FAIL)
                                                + " or rename " +
                                                "/usr/bin/{}".format(
                                                    repository['name'].lower())
                                            )
                        # ----------
                        #  Installation confirmation
                        # ----------------
                        if not __args.quiet:
                            print(
                                "{}{}[*] {} has been successfully installed{}\n".
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
    def uninstall(self, __db, __query, __os, __args):
        found = False
        for repository in __db['repos']:
            if not found and __query.lower() == repository['name'].lower():
                found = True
                # ----------
                #  Check permissions
                # ----------------
                if os.geteuid() == 0:
                    # ----------
                    #  Peral Tools Installation Folder
                    # ----------------
                    if __os == "Linux":
                        tools_folder = "/opt/peral_tools/"
                    # ----------
                    #  Confirm Remove Commands
                    # ----------------
                    if __args.yes:
                        confirm_uninstall = 'y'
                    else:
                        confirm_uninstall = input(
                            color.FAIL + color.BOLD +
                            "[!] Are you sure to uninstall {}? [y/N]: {}".
                            format(repository['name'], color.ENDC))
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
                            remove_repo = "rm -rf {}{}".format(
                                tools_folder, repository['name'])
                            lremove_lk = shlex.split(remove_lk)
                            lremove_repo = shlex.split(remove_repo)
                            # ----------
                            #  Desinstallation Process
                            # ----------------
                            if not __args.quiet:
                                print("{}{}[*] Removing syslinks...{}".format(
                                    color.BOLD, color.WARNING, color.ENDC))
                                subprocess.call(lremove_lk, shell=False)
                                print(
                                    "{}{}[*] Removing repository...{}".format(
                                        color.BOLD, color.WARNING, color.ENDC))
                                subprocess.call(lremove_repo, shell=False)
                        # ----------
                        #  Desinstallation confirmation
                        # ----------------
                        if not __args.quiet:
                            print("{}{}[*] {} has been successfully".format(
                                color.BOLD, color.HEADER, repository['name']) +
                                  " uninstalled{}".format(color.ENDC))
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
    __os = str()
    __realpath = str()

    # ----------
    #  Initialization
    # ----------------
    def __init__(self):
        self.__os = platform.system()
        self.__realpath = os.path.dirname(os.path.realpath(__file__))

    # ----------
    #  System Information
    # ----------------
    def getos(self):
        return self.__os

    def getpath(self):
        return self.__realpath


# ----------
#  Security Core
# ----------------
class Security:
    security_enabled = False

    # ----------
    #  Initialization
    # ----------------
    def __init__(self, __path):
        try:
            # ----------
            #  Read MD5 file
            # ----------------
            hashmd5 = str()
            with open("{}/md5.sum".format(__path)) as md5sum:
                # ----------
                #  Calculate MD5 DB Sum
                # ----------------
                with open("{}/{}".format(__path, db_name)) as db:
                    hashmd5 = hashlib.md5(
                        db.read().encode('utf-8')).hexdigest()
                # ----------
                #  Compare both and check if it is secure
                # ----------------
                if md5sum.read().strip() == hashmd5.strip():
                    self.security_enabled = True
        # ----------
        #  Handle errors
        # ----------------
        except IOError:
            pass

    # ----------
    #  Return security flag
    # ----------------
    def is_secure(self):
        return self.security_enabled

    # ----------
    #  Security Error Message
    # ----------------
    def not_secure(self):
        print("{}{}[!] Database has been modified!".format(
            color.BOLD, color.FAIL, color.ENDC))


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
        self.__file = "{}/{}".format(__file, db_name)
        with open(self.__file, 'r') as open_json:
            self.__db = json.load(open_json)

    # ----------
    #  Misc. functions
    # ----------------
    def getjson(self):
        return self.__db
