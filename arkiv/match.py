from arkiv import is_multi_part_volume_type

from arkiv.rar.match import match_rar
from arkiv.split.match import match_split_file

from arkiv.zip import match_zip_file
from arkiv.zip7 import match_zip7_file


def match_archive(name):
    return match_rar(name) or match_split_file(name) or match_zip_file(name) or match_zip7_file(name)


def is_archive_file_name(file_name):
    return bool(match_archive(file_name))


def is_multi_part_file_name(file_name):
    archive = match_archive(file_name)
    return bool(archive) and is_multi_part_volume_type(archive.type)


def archive_extension(name):
    match = match_archive(name)
    if match:
        return match.extension.lower()