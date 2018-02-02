# ============================================= #
#  -------------- Future Modules -------------  #
# ============================================= #
from __future__ import print_function


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
class Searcher:
    # ----------
    #  Init Function
    # ----------------
    def __init__(self, __info, __args, __database):
        self.__info = __info
        self.__args = __args
        self.__database = __database

    def search(self, __pieceofname):
        print("")
        print("{}{}|----------------------------------------------".format(
            color.BOLD, color.OKBLUE))
        for repository in self.__database['repos']:
            if __pieceofname in repository['name']:
                print("{}|{} Name: {}{}".format(color.OKBLUE, color.OKGREEN,
                                                color.WARNING,
                                                repository['name']))
                print("{}|{} Author: {}{}".format(color.OKBLUE, color.OKGREEN,
                                                  color.WARNING,
                                                  repository['author']))
                print("{}|{} Description: {}{}".format(
                    color.OKBLUE, color.OKGREEN, color.WARNING,
                    repository['description']))
                print("{}|{} Version: {}{}".format(color.OKBLUE, color.OKGREEN,
                                                   color.WARNING,
                                                   repository['version']))
                print("{}|{} Commit tested: {}{}".format(
                    color.OKBLUE, color.OKGREEN, color.WARNING,
                    repository['commit']))
                print("{}{}|----------------------------------------------{}"
                      .format(color.OKBLUE, color.BOLD, color.OKBLUE,
                              color.ENDC))
        print("")
