import re
from arkiv import ArchiveTuple, VolumeType

_rar_regex = re.compile('(.+)\.(rar)$', re.IGNORECASE)


def match_rar_archive(file_name):
    match = _rar_regex.match(file_name)
    if match:
        return ArchiveTuple(match.group(1), 1, VolumeType.Rar, match.group(2))
