#! /usr/bin/env python
# -*- coding: utf-8 -*-

from core.information import Info
from core.jsonreader import ReadJSON
from core.install.linux import LinuxInstaller


# ============================================= #
#  -------------- Release Info ---------------  #
# ============================================= #
class release:
    __author__ = "Kike Puma"
    __copyright__ = "Copyright 2018, CosasDePuma"
    __credits__ = ["KikePuma", "CosasDePuma"]
    __license__ = "MIT"
    __version__ = "1.0a"
    __maintainer__ = "KikePuma"
    __email__ = "kikefontanlorenzo@gmail.com"
    __status__ = "In development"


# ============================================= #
#  ------------------ Colors -----------------  #
# ============================================= #
class color:
    BOLD = '\033[1m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# ============================================= #
#  --------------- Arguments -----------------  #
# ============================================= #
class args:
    repo = "Cr3dOv3r"


# ============================================= #
#  ------------------ Main -------------------  #
# ============================================= #
class Main:
    database_name = "octopus_db.json"

    def __init__(self):
        self.info = Info()
        self.database_path = self.info.get_filepath(self.database_name)
        self.reader = ReadJSON(self.database_path)
        self.database = self.reader.read()
        if not self.database:
            raise IOError('Database not found')

    def configure(self):
        if self.info.get_os() == "Linux":
            self.distro = self.info.get_distro()
            self.installation_path = "/opt/peral_tools"
            self.installer = LinuxInstaller(self.database,
                                            self.installation_path, self.info)

            repository = self.installer.search(args.repo)
            self.installer.install(repository)


if __name__ == '__main__':
    try:
        main = Main()
        main.configure()
    except (IOError, SystemError, ImportError) as custom_exception:
        print("{}{}[!] {}{}".format(color.BOLD, color.FAIL,
                                    custom_exception[0], color.ENDC))
