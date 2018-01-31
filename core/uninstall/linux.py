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
#  ------------ Linux Uninstaller ------------  #
# ============================================= #
class LinuxUninstaller:
    # ----------
    #  Init Function
    # ----------------
    def __init__(self, __database, __installation_folder, __info):
        self.__info = __info
        self.__database = __database
        self.__syslink_folder = "/usr/bin"
        self.__installation_folder = __installation_folder

    # ============================================= #
    #  --------- Basic Install Functions ---------  #
    # ============================================= #

    # ----------
    #  Uninstall Function
    # ----------------
    def uninstall(self, __repository):
        # ----------
        #  User Security Confirmation
        # ----------------
        if self.confirm_uninstall(__repository['name']):
            self.remove_scripts(__repository['uninstall'][0]['Linux'])
            self.remove_repository(__repository['name'])


# ============================================= #
#  ------- Complex Uninstall Functions -------  #
# ============================================= #

# ----------
#  User confirmation
# ----------------

    def confirm_uninstall(self, __name):
        # ----------
        #  Return option
        # ---------------
        return input(
            "{}{}[?] Would you like to uninstall {} repository? [y/N]: {}".
            format(color.BOLD, color.FAIL, __name, color.ENDC)).lower() == 'y'

    # ----------
    #  Remove Script Function
    # ---------------
    def remove_scripts(self, __scripts):
        print("{}{}[*] Running uninstaller scripts...{}".format(
            color.BOLD, color.OKBLUE, color.ENDC))
        for cmd in __scripts:
            try:
                subprocess.check_output(shsplit(cmd))
            except subprocess.CalledProcessError:
                print("{}[!] Error running: {}{}{}".format(
                    color.FAIL, color.WARNING, cmd, color.ENDC))

    # ----------
    #  Remove Function
    # ---------------
    def remove_repository(self, __name):
        # ----------
        #  Get locations
        # ---------------
        syslink_location = "{}/{}".format(self.__syslink_folder,
                                          __name.lower())
        repository_location = "{}/{}".format(self.__installation_folder,
                                             __name)
        # ----------
        #  Get commands
        # ---------------
        rm_syslink = "rm -f {}".format(syslink_location)
        rm_repo = "rm -rf {}".format(repository_location)
        # ----------
        #  Remove Syslink
        # ---------------
        try:
            print("{}{}[*] Removing syslink...{}".format(
                color.BOLD, color.OKBLUE, color.ENDC))
            subprocess.check_output(shsplit(rm_syslink))
        except subprocess.CalledProcessError:
            print("{}{}[*] Cannot remove {} syslink{}".format(
                color.BOLD, color.FAIL, syslink_location, color.ENDC))
        # ----------
        #  Remove Repository
        # ---------------
        try:
            print("{}{}[*] Removing repository...{}".format(
                color.BOLD, color.OKBLUE, color.ENDC))
            subprocess.check_output(shsplit(rm_repo))
        except subprocess.CalledProcessError:
            print("{}{}[*] Cannot remove {} repository{}".format(
                color.BOLD, color.FAIL, repository_location, color.ENDC))
