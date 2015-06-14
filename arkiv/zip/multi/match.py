import math
import re
from arkiv import ArchiveTuple, VolumeType

_zip_multi_regex = re.compile('(.+)\.(z(?P<zeros>0*)(\d+))$', re.IGNORECASE)


def match_zip_multi(file_name):
    match = _zip_multi_regex.match(file_name)
    if match:
        return ArchiveTuple(match.group(1), int(match.group(4)) + 1, VolumeType.ZipMultiPart, match.group(2))


def substitute_zip_part_file_name(file_name, substitute):
    zip_part_match = match_zip_multi(file_name)

    if zip_part_match:
        existing_zeros = _zip_multi_regex.match(file_name).group('zeros')
        part_zeros = int(math.log(zip_part_match[1], 10))
        zeros = '0' * (part_zeros + len(existing_zeros))

        substitute = _zip_multi_regex.sub(r'\g<1>.z%s%d' % (zeros, substitute - 1), file_name)
        return substitute
