<img src="https://cdn.rawgit.com/CosasDePuma/Peral/63ff9393/img/Peral.png" align="right" width="300">

# Peral
[![Python Version](https://img.shields.io/badge/python-2.x\/3.x-yellow.svg?style=flat)](https://www.python.org/downloads) ![Made with Love](https://img.shields.io/badge/made%20with-<3-red.svg?style=flat) [![License](https://img.shields.io/github/license/CosasDePuma/Peral.svg)](https://github.com/CosasDePuma/Peral/blob/master/LICENSE)

:vhs: Clone me!
----
Clone or download the Github project
```bash
git clone https://github.com/cosasdepuma/peral.git Peral
```

:memo: Installation
----
Enter to the Peral directory

```sh
cd Peral
```

Create a launch script
```sh
echo "#! /bin/bash" > initperal.sh
echo "pushd $PWD > /dev/null" >> initperal.sh
echo "python ./main.py $@" >> initperal.sh
echo "popd > /dev/null" >> initperal.sh
```

Link the program to `peral` shortcut

```sh
ln -s $PWD/initperal.sh /usr/bin/peral
```

:see_no_evil: Run the program!
----
Run the python script and display help:
```sh
peral --help
```

To find a repository:
```sh
peral search repository
```

You can also find a repository using part of its name:
```sh
peral search partialname
```

To install a repository:
```sh
peral install repository
```

You can see a list with the available installation commands by typing:
```sh
peral install --help
```

The same process is required to uninstall repositories:
```sh
peral uninstall repository
```

Issues
----
If **peral** does not work, try replacing
```sh
python ./main.py $@
```
with
```sh
python2 ./main.py $@
```

###### Currently, Peral only works correctly in Linux Operating Systems based on Debian.

 

Please contact with [Kike Puma](https://linkedin.com/in/kikepuma) if you need more information.
