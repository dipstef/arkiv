import os
from ..archive import ArchiveFileName, MultiPartFile
from .match import match_rar, multi_part_with_number
from .old.match import *
from .old import RarMultiPartOld


class ArchiveRar(ArchiveFileName):
    def __init__(self, file_name):
        super(ArchiveRar, self).__init__(file_name, VolumeType.Rar)


class RarMultiPart(MultiPartFile):
    def __init__(self, file_name, archive_name, number):
        super(RarMultiPart, self).__init__(file_name, archive_name, VolumeType.RarMultiPart, number)


def match_rar_archive(file_name):
    rar = match_rar(file_name)
    if rar:
        return _multi_part(file_name, rar) or ArchiveRar(file_name)


def _multi_part(name, rar):
    if rar.type == VolumeType.RarMultiPart:
        return RarMultiPart(name, *rar[:2])
    elif rar.type == VolumeType.RarMultiPartOld:
        return RarMultiPartOld(name, *rar[:2])


_rar_extension_regex = re.compile(r'(rar|r\d{2,})$')


def is_rar_extension(extension):
    return _rar_extension_regex.match(extension)


def rar_file(file_name):
    return match_rar_archive(file_name)


def rar_path(path):
    rar = rar_file(os.path.basename(path))
    if rar:
        rar.path = path
    return rar


def is_rar_file(file_name):
    return bool(match_rar_archive(file_name))


def substitute_rar_part(part, missing_part):
    if part.archive.type == VolumeType.RarMultiPart:
        return multi_part_with_number(part.name, missing_part)
    elif part.archive.type == VolumeType.RarMultiPartOld:
        return substitute_old_rar_multi_part(part.archive.name, part.number, substitute=missing_part)
