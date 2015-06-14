import re

from arkiv import ArchiveTuple, VolumeType
from arkiv.zip.multi.match import match_zip_multi

_zip_extension_regex = re.compile('(.+)\.(zip)$', re.IGNORECASE)


def _match_archive_zip(file_name):
    match = _zip_extension_regex.match(file_name)
    if match:
        return ArchiveTuple(match.group(1), 1, VolumeType.Zip, match.group(2))


def match_zip_file(file_name):
    if file_name:
        return _match_archive_zip(file_name) or match_zip_multi(file_name)
