from .rar import rar_file
from .zip import zip_file
from .split import split_file
from .zip7 import zip7_file


def parse_archive_name(name):
    if name:
        return rar_file(name) or zip_file(name) or split_file(name) or zip7_file(name)
