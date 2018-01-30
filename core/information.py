import os
import platform


class Info:
    def __init__(self):
        pass

    def is_dir(self, __dir):
        return os.path.isdir(__dir)

    def is_file_in_cwd(self, __file):
        return os.path.isfile(os.path.join(os.getcwd(), __file))

    def is_privileged(self):
        return os.geteuid() == 0

    def set_workdir(self, __path):
        os.chdir(__path)

    def get_devnull(self):
        return os.devnull

    def get_homedir(self):
        return os.path.expanduser('~')

    def get_username(self):
        real_user = str()
        if self.get_os() == "Linux":
            if 'SUDO_USER' in os.environ:
                real_user = os.environ['SUDO_USER']
            else:
                real_user = os.environ['USER']
        return real_user

    def get_os(self):
        return platform.system()

    def get_distro(self):
        return platform.dist()[0].replace('\"', '')

    def get_filepath(self, __file):
        return os.path.join(os.path.dirname(os.path.realpath(__file)), __file)
