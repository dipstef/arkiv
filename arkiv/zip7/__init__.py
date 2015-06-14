import re
from arkiv import ArchiveFileName, VolumeType, ArchiveTuple

_7z_regex = re.compile('(.+)\.(7z)$', re.IGNORECASE)


class File7z(ArchiveFileName):
    def __init__(self, file_name):
        super(File7z, self).__init__(file_name, VolumeType.Zip7)


def is_zip7_file(file_name):
    if file_name:
        return bool(_7z_regex.match(file_name))


def match_zip7_file(file_name):
    if file_name:
        match = _7z_regex.match(file_name)
        if match:
            return ArchiveTuple(match.group(1), 1, VolumeType.Zip7, match.group(2))


def zip7_file(file_name):
    if is_zip7_file(file_name):
        return File7z(file_name)
