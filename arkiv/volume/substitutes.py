from collections import OrderedDict

from ..archive import VolumeType
from ..rar import substitute_rar_part
from ..split import substitute_split_file
from ..zip import substitute_zip_part


def join_archive_parts(volume, substitutes):
    parts = volume.parts
    for part_substitutes in substitutes.values():
        part_substitutes = [substitute for substitute in part_substitutes if substitute.archive == volume.archive]
        if part_substitutes:
            parts.append(part_substitutes[0])

    return sorted(parts, key=lambda p: p.number)


def archive_parts_names(parts, part_numbers):
    part_names = OrderedDict()
    part_number_dict = {part.number: part for part in parts}

    volume_part = _archive_volume_part(parts)
    if volume_part:
        for part_number in part_numbers:
            if part_number in part_number_dict:
                part_names[part_number] = part_number_dict[part_number].name
            else:
                part_names[part_number] = multi_part_name(volume_part, part_number)
    return part_names


def _archive_volume_part(archive_parts):
    if archive_parts:
        volume_part = min(archive_parts, key=lambda p: p.number)

        if volume_part.archive.type == VolumeType.RarMultiPartOld:
            secondary_parts = [part for part in archive_parts if part.number > 1]
            if secondary_parts:
                volume_part = min(archive_parts, key=lambda p: p.number)

        return volume_part


def multi_part_name(volume_part, part_number):
    if volume_part.archive.type in [VolumeType.RarMultiPart, VolumeType.RarMultiPartOld]:
        return substitute_rar_part(volume_part, part_number)
    elif volume_part.archive.type == VolumeType.Split:
        return substitute_split_file(volume_part, part_number)
    elif volume_part.archive.type == VolumeType.ZipMultiPart:
        return substitute_zip_part(volume_part, part_number)