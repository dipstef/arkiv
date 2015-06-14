import math
import re
from arkiv import ArchiveTuple, VolumeType
from ..one_part import match_rar_archive

_old_format_rar_regex = re.compile(r'(.+)\.(r(\d{2,}))$', re.IGNORECASE)


def old_multi_part_rar(file_name):
    match = _old_format_rar_regex.match(file_name)
    if match:
        return ArchiveTuple(match.group(1), int(match.group(3)) + 2, VolumeType.RarMultiPartOld, match.group(2))


def substitute_old_rar_multi_part(archive_name, number, substitute):
    if substitute == 1:
        return archive_name + '.rar'
    else:
        starting_zeros = '0' * (int(math.log(number, 10)) or 1)
        return archive_name + '.r%s%d' % (starting_zeros, substitute - 2)


def old_multi_part_number(file_name, number):
    archive_match = old_multi_part_rar(file_name) or match_rar_archive(file_name)
    if archive_match:
        return substitute_old_rar_multi_part(archive_match[0], archive_match[1], substitute=number)
