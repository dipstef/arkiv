import math
import re
from ..archive import ArchiveTuple, VolumeType

_digit_split_regex = re.compile('(.+)\.((?P<zeros>0+)(\d+)|[1-9]\d*)$', re.IGNORECASE)


def digit_split(file_name):
    match = _digit_split_regex.match(file_name)
    if match:
        return ArchiveTuple(match.group(1), int(match.group(2)), VolumeType.Split, match.group(2))


def substitute_digit_split_file(file_name, part, missing_part):
    digit_split = _digit_split_regex.match(file_name)

    existing_zeros = digit_split.group('zeros') or ''
    part_zeros = int(math.log(part, 10))
    zeros = '0' * (part_zeros + len(existing_zeros))

    substituted = _digit_split_regex.sub(r'\g<1>.%s%d' % (zeros, missing_part), file_name)
    return substituted
