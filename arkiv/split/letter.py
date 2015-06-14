import math
import re
from arkiv import ArchiveTuple, VolumeType


def letter_split(file_name):
    match = _letter_split_regex.match(file_name)
    if match:
        return ArchiveTuple(match.group(1), ord(match.group(4)) % 96, VolumeType.Split, match.group(2))


_letter_split_regex = re.compile('(.+)\.((?P<dashes>_+)(\w))$', re.IGNORECASE)


def substitute_letter_split_file(file_name, part, substitute):
    letter_split = _letter_split_regex.match(file_name)

    existing_dashes = letter_split.group('dashes') or ''
    part_dashes = int(math.log(part, 10))
    dashes = '_' * (part_dashes + len(existing_dashes))

    letter = str(unichr(96 + substitute))
    return _letter_split_regex.sub(r'\g<1>.%s%s' % (dashes, letter), file_name)
