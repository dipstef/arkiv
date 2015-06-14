from collections import OrderedDict

from arkiv import is_multi_part_archive


def has_part(volume, part_number):
    return bool(get_part(volume, part_number))


def get_part(volume, part_number):
    if volume.is_multi_part:
        return volume.get(part_number)
    else:
        assert part_number == 1
        return volume.extract_file


def part_numbers(volume):
    return volume.part_numbers if is_multi_part_archive(volume) else [1]


def secondary_parts_dict(volume):
    return OrderedDict([(archive.number, archive) for archive in volume.parts if archive.number > 1])


def parts_range(volume):
    parts_numbers = part_numbers(volume)
    # same split files having named wrongly with high indexes results in create huge range and saturating memory
    if max(parts_numbers) < 1024:
        return map(lambda i: i + 1, range(max(parts_numbers)))
    else:
        return parts_numbers


def common_parts(volume1, *volumes):
    parts_common = set(part_numbers(volume1)).intersection(*((set(part_numbers(volume2)) for volume2 in volumes)))
    parts_common = [tuple((get_part(volume, part) for volume in [volume1] + list(volumes))) for part in parts_common]
    return parts_common


def select_containing_parts(volume, parts_select):
    containing = set(part_numbers(volume)).intersection(parts_select)
    return OrderedDict([(part_containing, get_part(volume, part_containing)) for part_containing in containing])


def has_all_parts(volume):
    return not is_multi_part_archive(volume) or volume.is_complete


def valid_parts(volume):
    return [part.number for part in volume.parts if part.size]


def common_valid_parts(volume1, volume2):
    return set(valid_parts(volume1)).intersection(set(valid_parts(volume2)))
