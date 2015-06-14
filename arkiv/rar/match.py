import math

import re

from arkiv import ArchiveTuple, VolumeType
from .old.match import old_multi_part_rar
from .one_part import match_rar_archive



_new_format_rar_regex = re.compile(r'(.+)\.(part(?P<zeros>0*)(\d+)\.rar)$', re.IGNORECASE)


def match_rar(file_name):
    if file_name:
        return _multi_part_rar(file_name) or old_multi_part_rar(file_name) or match_rar_archive(file_name)


def _multi_part_rar(file_name):
    match = _new_format_rar_regex.match(file_name)
    if match:
        return ArchiveTuple(match.group(1), int(match.group(4)), VolumeType.RarMultiPart, match.group(2))


def multi_part_with_number(file_name, substitute):
    archive_match = _multi_part_rar(file_name)
    if archive_match:
        existing_zeros = _new_format_rar_regex.match(file_name).group('zeros')
        part_zeros = int(math.log(archive_match[1], 10))
        zeros = '0' * (part_zeros + len(existing_zeros))

        substitute = _new_format_rar_regex.sub(r'\g<1>.part%s%d.rar' % (zeros, substitute), file_name)
        return substitute
