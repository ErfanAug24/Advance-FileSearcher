import sys


def convert_datetime(timestamp):
    pass


def get_default_path(platform):
    if platform == "win32":
        return "C://"
    return "/home"


def check_platform():
    return sys.platform
