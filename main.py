#! /usr/bi/env python
# -*- coding: utf-8 -*-

# requirements.txt : future

# ============================================= #
#  --------------- Header Info ---------------  #
# ============================================= #

__author__ = "Kike Puma"
__copyright__ = "Copyright 2018, CosasDePuma"
__credits__ = ["KikePuma", "CosasDePuma"]
__license__ = "MIT"
__version__ = "0.1c"
__maintainer__ = "KikePuma"
__email__ = "kikefontanlorenzo@gmail.com"
__status__ = "In development"

# ============================================= #
#  ----------------- Modules -----------------  #
# ============================================= #

import argparse

from core import Core
from core import Info
from core import Reader
from core import Security

# ============================================= #
#  --------------- Arguments -----------------  #
# ============================================= #

parser = argparse.ArgumentParser(version=__version__)
subparser = parser.add_subparsers(dest="cmd")

for cmd in ["install", "search", "uninstall"]:
    subsubparser = subparser.add_parser(cmd)
    subsubparser.add_argument('repository', type=str)
    if "install" in cmd:
        subsubparser.add_argument(
            '-q',
            '--quiet',
            '--silent',
            help="Do not print info messages",
            action="store_true")
        subsubparser.add_argument(
            '-y', '--yes', help="Accept all dialogs", action="store_true")

args = parser.parse_args()

# ============================================= #
#  ------------------ Main -------------------  #
# ============================================= #

if __name__ == "__main__":
    core = Core()
    info = Info()
    security = Security(info.getpath())
    reader = Reader("{}".format(info.getpath()))

    if security.is_secure():
        if args.cmd == "install":
            core.install(reader.getjson(), args.repository, info.getos(), args)
        elif args.cmd == "search":
            core.search(reader.getjson(), args.repository)
        elif args.cmd == "uninstall":
            core.uninstall(reader.getjson(), args.repository,
                           info.getos(), args)
    else:
        security.not_secure()

# ============================================= #
#  ------------------ ToDo's -----------------  #
# ============================================= #

# Author search
# Handle errors during installation
# Stylish search
