from collections import defaultdict
from itertools import groupby
import re
from arkiv.archive import is_multi_part_extract


def normalize_archive_names(archives):
    extract_files = filter(is_multi_part_extract, archives)
    for extract_file in extract_files:
        volume = extract_file.volume
        archive_groups = _group_archives(volume)
        if len(archive_groups) > 1:
            _rename_to_most_common_archive(archive_groups, volume)


def _group_archives(volume):
    archive_groups = defaultdict(list)
    for archive, archive_group in groupby(volume.values(), key=lambda a: a.archive):
        archive_groups[archive].extend(archive_group)
    return archive_groups


def _rename_to_most_common_archive(archive_groups, volume):
    max_archive, max_archives = max(archive_groups.items(), key=lambda i: len(i[1]))
    for part in volume.values():
        if part.archive != max_archive:
            part.name = re.sub(part.archive.name, max_archive.name, part.name)
            part.archive = max_archive
