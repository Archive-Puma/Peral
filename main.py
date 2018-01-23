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
__version__ = "0.1a"
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

# ============================================= #
#  --------------- Arguments -----------------  #
# ============================================= #

parser = argparse.ArgumentParser(version=__version__)
subparser = parser.add_subparsers(dest="cmd")

for cmd in ["install", "search", "uninstall"]:
    subsubparser = subparser.add_parser(cmd)
    subsubparser.add_argument('repository', type=str)

args = parser.parse_args()


# ============================================= #
#  ------------------ Main -------------------  #
# ============================================= #

if __name__ == "__main__":
    core = Core()
    info = Info()
    reader = Reader('toilet.json')

    if args.cmd == "install":
        core.install(reader.getjson(), args.repository, info.__os__)
    elif args.cmd == "search":
        core.search(reader.getjson(), args.repository)
    elif args.cmd == "uninstall":
        core.uninstall(reader.getjson(), args.repository, info.__os__)

# ============================================= #
#  ------------------ ToDo's -----------------  #
# ============================================= #

# Fix sudo without -H if pip is installed
# Handle errors during installation
# MD5 checksum
# Stylish search
# Global usage (not only current workdir) Check JSON file
# change installarion folder to /opt/{repositoryname}
