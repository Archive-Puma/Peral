# ============================================= #
#  -------------- Future Modules -------------  #
# ============================================= #
from __future__ import print_function

# ============================================= #
#  ----------------- Modules -----------------  #
# ============================================= #
import subprocess

# ============================================= #
#  --------------- From modules --------------  #
# ============================================= #
from builtins import input
from shlex import split as shsplit
from os import getcwd as currentdir
from os import system as dangerous_execution


# ============================================= #
#  ------------------ Colors -----------------  #
# ============================================= #
class color:
    BOLD = '\033[1m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'


# ============================================= #
#  ------------- Linux Installer -------------  #
# ============================================= #
class LinuxInstaller:
    # ----------
    #  Init Function
    # ----------------
    def __init__(self, __database, __installation_folder, __info):
        self.__info = __info
        self.__syslink_flag = True
        self.__database = __database
        self.__initscript = "initperal.sh"
        self.__syslink_folder = "/usr/bin"
        self.__installation_folder = __installation_folder

# ============================================= #
#  --------- Basic Install Functions ---------  #
# ============================================= #

# ----------
#  Install Function
# ----------------

    def install(self, __repository):
        # ----------
        #  User Security Confirmation
        # ----------------
        if self.confirm_commands(__repository['name'],
                                 __repository['install'][0]['Linux']):
            # ----------
            #  Git Clone
            # ----------------
            self.github(__repository['name'], __repository['author'])
            # ----------
            #  Change owner and directory
            # ----------------
            self.configure_new_folder(__repository['name'])
            # ----------
            #  Create and reset initperal.sh if it is needed
            # ----------------
            if self.init_script_needed:
                self.configure_init_script()
            # ----------
            #  Installation Commands
            # ----------------
            print("{}{}[*] Running Setup Scripts...{}".format(
                color.BOLD, color.OKBLUE, color.ENDC))
            for cmd in __repository['install'][0]['Linux']:
                with open(self.__info.get_devnull(), "w") as FNULL:
                    cmd = self.custom_command(cmd)
                    if cmd is not None:
                        # ----------
                        #  Handle execution errors
                        # ----------------
                        try:
                            subprocess.check_output(shsplit(cmd), stderr=FNULL)
                        except subprocess.CalledProcessError:
                            print("{}[!] Error running: {}{}{}".format(
                                color.FAIL, color.WARNING, cmd, color.ENDC))
            # ----------
            #  Check for Syslink
            # ----------------
            if self.__syslink_flag:
                if self.confirm_syslink(__repository['name']):
                    # ----------
                    #  Create Syslink
                    # ----------------
                    self.create_syslink(__repository['name'],
                                        __repository['main-script'])


# ============================================= #
#  -------- Complex Install Functions --------  #
# ============================================= #

# ----------
#  Git Clone Function
# ----------------

    def github(self, __name, __author):
        # ----------
        #  Get GitHub Link
        # ----------------
        github_link = "https://github.com/{}/{}".format(__author, __name)
        # ----------
        #  Git Clone Command
        # ----------------
        repository_folder = "{}/{}".format(self.__installation_folder, __name)
        git_command = "git clone {} {}".format(github_link, repository_folder)
        # ----------
        #  Check if Repository is already installed
        # ----------------
        with open(self.__info.get_devnull(), 'w') as FNULL:
            if self.__info.is_dir(repository_folder):
                rm_old_repo_cmd = "rm -rf {}".format(repository_folder)
                # ----------
                #  Handle Errors
                # ----------------
                try:
                    print("{}{}[*] Removing old installations...{}".format(
                        color.BOLD, color.OKBLUE, color.ENDC))
                    subprocess.check_output(
                        shsplit(rm_old_repo_cmd), stderr=FNULL)
                except subprocess.CalledProcessError:
                    print("{}{}[*] Failed to remove old repositories{}".format(
                        color.BOLD, color.FAIL, color.ENDC))
        # ----------
        #  Handle Errors
        # ----------------
            try:
                print("{}{}[*] Clonning GitHub repository...{}".format(
                    color.BOLD, color.OKBLUE, color.ENDC))
                subprocess.check_output(shsplit(git_command), stderr=FNULL)
            except subprocess.CalledProcessError:
                raise ImportError("Failed to clone GitHub repository!")

    # ----------
    #  User Security Confirmation
    # ----------------
    def confirm_commands(self, __name, __commands):
        self.init_script_needed = False

        print("")
        print("{}{}[*] SETUP COMMANDS:".format(color.BOLD, color.OKBLUE))
        print("-------------------------{}{}".format(color.ENDC,
                                                     color.WARNING))
        # ----------
        #  Read Setup Commands
        # ----------------
        for cmd in __commands:
            # ----------
            #  Check INIT commands
            # ----------------
            if not self.init_script_needed and "INIT " == cmd[:5]:
                self.init_script_needed = True
            print(cmd)
        print("{}{}---------------------------------------{}".format(
            color.BOLD, color.OKBLUE, color.FAIL))
        # ----------
        # Get User Option
        # ----------------
        option = input(
            "[?] Are you sure to install {} executing this commands? [Y/n] {}".
            format(__name, color.ENDC)).lower()
        # ----------
        #  Return User Input
        # ----------------
        return option == 'y' or option == ''

    # ----------
    #  Format custom commands
    # ----------------
    def custom_command(self, __cmd):
        # ----------
        #  Replace Custom TAGS
        # ----------------
        if "<PWD>" in __cmd:
            __cmd = __cmd.replace("<PWD>", currentdir())
        if "<HOME>" in __cmd:
            __cmd = __cmd.replace("<HOME>", self.__info.get_homedir())
        # ----------
        #  Don't create syslinks
        # ----------------
        if __cmd[:9] == "NOSYSLINK":
            self.__syslink_flag = False
            __cmd = None
        # ----------
        #  Configure the initial script
        # ----------------
        elif __cmd[:5] == "INIT ":
            with open("initperal.sh", "a") as init_script:
                init_script.write("{}\n".format(__cmd[5:]))
        # ----------
        #  Check for an input value
        # ----------------
        elif __cmd[:6] == "INPUT ":
            self.BUFFER = input("{}{}[-] {}{}".format(
                color.BOLD, color.OKGREEN, __cmd[6:], color.ENDC))
            __cmd = None
        # ----------
        #  Use the input value in a command
        # ----------------
        elif __cmd[:7] == "OUTPUT ":
            __cmd = __cmd[7:].replace("<OUTPUT>", self.BUFFER)
        # ----------
        #  echos and wget
        # ----------------
        elif "echo" in __cmd or "wget" in __cmd:
            '''
             !!!!!!!!!!!!!!!!!!!!
             !! DANGEROUS CODE !!
             !!!!!!!!!!!!!!!!!!!!
            '''
            dangerous_execution(__cmd)
            __cmd = None

        # ----------
        #  Return command
        # ----------------
        return __cmd

    # ----------
    #  Change owner and directory
    # ---------------
    def configure_new_folder(self, __name):
        # ----------
        #  User Security Confirmation
        # ----------------
        full_path = "{}/{}".format(self.__installation_folder, __name)
        cmd = "chown -R {} {}".format(self.__info.get_username(), full_path)
        # ----------
        #  Handle exceptions
        # ----------------
        try:
            with open(self.__info.get_devnull(), "w") as FNULL:
                subprocess.check_output(
                    shsplit(cmd), stderr=FNULL, shell=False)
        except subprocess.CalledProcessError:
            print("{}[!] Error changing {} owner{}".format(
                color.FAIL, full_path, color.ENDC))
        # ----------
        #  Change directory
        # ----------------
        self.__info.set_workdir(full_path)

    # ----------
    #  Configure Initial Script - owner and mods
    # ---------------
    def configure_init_script(self):
        # ----------
        #  Set commands
        # ---------------
        chm = "chmod +x {}".format(self.__initscript)
        chw = "chown {} {}".format(self.__info.get_username(),
                                   self.__initscript)
        # ----------
        #  Touch the file
        # ---------------
        open(self.__initscript, "w").close()
        # ----------
        #  Handle exceptions
        # ---------------
        try:
            with open(self.__info.get_devnull(), "w") as FNULL:
                print("{}{}[*] Touching {} script...{}".format(
                    color.BOLD, color.OKBLUE, self.__initscript, color.ENDC))
                # ----------
                #  Executing commands
                # ---------------
                subprocess.check_output(shsplit(chm), stderr=FNULL)
                subprocess.check_output(shsplit(chw), stderr=FNULL)
        except subprocess.CalledProcessError:
            print("{}{}[!] Cannot touch {} script{}".format(
                color.BOLD, color.FAIL, self.__initscript, color.ENDC))

    # ----------
    #  Confirm Syslink
    # ---------------
    def confirm_syslink(self, __name):
        __name = __name.lower()
        # ----------
        #  Get User Option
        # ----------------
        option = input("{}{}[?] {} {}{}{}{}{}? [Y/n]: {}".format(
            color.BOLD, color.WARNING,
            "Would you like to create a syslink named", color.UNDERLINE,
            __name, color.ENDC, color.BOLD, color.WARNING,
            color.ENDC)).lower()
        # ----------
        #  Return option
        # ---------------
        return option == 'y' or option == ''

    # ----------
    #  Syslink Function
    # ---------------
    def create_syslink(self, __name, __script):
        # ----------
        #  Get Main Script Path
        # ---------------
        repository_script = "{}/{}/{}".format(self.__installation_folder,
                                              __name, __script)
        __name = __name.lower()
        # ----------
        #  Syslink Command
        # ---------------
        cmd = "ln -s {} {}/{}".format(repository_script, self.__syslink_folder,
                                      __name)
        # ----------
        #  Handle exception
        # ---------------
        try:
            print("{}{}[*] Creating a syslink...{}".format(
                color.BOLD, color.OKBLUE, color.ENDC))
            # ----------
            #  Create Syslink
            # ---------------
            with open(self.__info.get_devnull(), "w") as FNULL:
                subprocess.check_output(shsplit(cmd), stderr=FNULL)
        except subprocess.CalledProcessError:
            print("{}{}[!] Cannot create a syslink{}".format(
                color.BOLD, color.FAIL, color.ENDC))
