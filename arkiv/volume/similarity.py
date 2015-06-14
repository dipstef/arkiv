def find_same_volumes(volume, volumes):
    _find_same_volumes = _volume_results(volumes)

    return _find_same_volumes(volume)


def _volume_results(volume_iterator):
    processed = set()

    def _find_same_volumes(volume):
        processed.add(volume)

        same_volumes = []

        for same_volume in volume_iterator(volume):
            if same_volume not in processed:
                same_volumes.append(same_volume)
                same_volumes += _find_same_volumes(same_volume)

        return same_volumes

    return _find_same_volumes


def same_parts(p1, p2):
    return p1.volume.archive.name == p2.volume.archive.name and p1.size == p2.size


def same_size_parts_diff(v1, v2):
    return same_parts_diff(v1, v2, part_eq=_same_size_parts)


def _same_size_parts(p1, p2):
    return p1.archive.name != p2.archive.name and (p1.size and p2.size and p1.size == p2.size)


def same_parts_diff(volume1, volume2, part_eq=same_parts):
    max_part = max(volume1.parts + volume2.parts, key=lambda p: p.number)

    parts1 = sorted([p1 for p1 in volume1.parts if p1.size], key=lambda p: p.number)
    parts2 = sorted([p2 for p2 in volume2.parts if p2.size], key=lambda p: p.number)

    if parts1 and parts2:
        min1, min2, max1, max2 = parts1[0], parts2[0], parts1[-1], parts2[-1]
        max1 = max1 if max1.number == max_part.number else None
        max2 = max2 if max2.number == max_part.number else None

        parts1 = [p1 for p1 in parts1 if p1.number < max_part.number and p1.size]
        parts2 = [p2 for p2 in parts2 if p2.number < max_part.number and p2.size]

        if max1 and max2:
            if part_eq(max1, max2):
                if not (parts1 and parts2):
                    return True
            else:
                return False

        if parts1 and parts2:
            equal_parts = _all_parts_equal_to(parts1, min2, part_eq) and _all_parts_equal_to(parts2, min1, part_eq)
            return equal_parts

    return False


def _all_parts_equal_to(parts, part, part_eq=same_parts):
    return bool(parts) and all((part_eq(p, part) for p in parts))
