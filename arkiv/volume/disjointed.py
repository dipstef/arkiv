from collected.dict.default import OrderedDefaultDict
from collected.sequence import no_duplicates

from arkiv import ArchiveMultiPart, MultiParts, part_numbers, valid_parts, common_valid_parts
from arkiv.volume.similarity import same_parts, same_parts_diff


def _disjointed_volumes(volume, archive_volumes):
    common_parts_volumes = set()

    processed = []

    def check_disjointed(check):
        processed.append(check)
        for other in archive_volumes(check):
            if other not in processed:
                if not _disjointed(volume, other):
                    common_parts_volumes.add(other)
                check_disjointed(other)
            if other in common_parts_volumes:
                common_parts_volumes.add(check)

    check_disjointed(volume)
    return [v for v in processed if v != volume and v not in common_parts_volumes]


def find_disjointed_parts_volumes(volume, archive_id_volumes, volume_eq=same_parts_diff):
    parts_online = valid_parts(volume)

    if volume.is_multi_part and parts_online:
        disjointed = _disjointed_volumes(volume, archive_id_volumes)

        if disjointed:
            return find_common_parts(volume, disjointed, volume_eq)
    return []


def _disjointed(v1, v2):
    return valid_parts(v2) and (_parts_disjointed(v1, v2) or not common_valid_parts(v1, v2))


def _parts_disjointed(volume1, volume2):
    parts1 = set(part_numbers(volume1))
    parts2 = set(part_numbers(volume2))
    return parts1.isdisjoint(parts2) if parts1 and parts2 else False


def find_common_parts(volume, volumes, volume_eq=same_parts_diff):
    parts_online = OnlineDisjointedParts(volume, volumes)

    disjointed = []
    if parts_online.volume_online_parts:
        if parts_online.volume_has_first_parts():
            disjointed = _find_disjointed_with_existing_first_parts(volume, parts_online, volume_eq=volume_eq)
        elif parts_online.exists_containing_last_part():
            disjointed = _find_disjointed_with_existing_last_part(volume, parts_online, volume_eq=volume_eq)
        else:
            disjointed = _find_comparing_min_parts(volume, parts_online, volume_eq=volume_eq)

    return sorted(disjointed, key=lambda v: volumes.index(v))


def _find_disjointed_with_existing_first_parts(volume, parts_online, volume_eq):
    if parts_online.volume_has_max_part():
        disjointed = [other for other in parts_online.volumes if volume_eq(volume, other)]
    else:
        disjointed = [other for other in parts_online.having_first_parts if volume_eq(volume, other)]
        same_online = _select_online_parts(disjointed)
        if parts_online.max_part not in same_online:
            disjointed += _add_remaining_last_parts(volume, parts_online.having_only_last_part, volume_eq)
    return disjointed


def _find_disjointed_with_existing_last_part(volume, parts_online, volume_eq):
    if parts_online.volume_has_max_part():
        return [other for other in parts_online.having_last_part if volume_eq(volume, other)]
    else:
        last_part_volumes = parts_online.having_last_part
        for last_part_volume in last_part_volumes:
            archive_vol = _multi_parts_archive(last_part_volume, volume.archive)
            disjointed = [v for v in last_part_volumes if v != last_part_volume and volume_eq(archive_vol, v)]
            if disjointed:
                return [last_part_volume] + disjointed
    return []


def _find_comparing_min_parts(volume, parts_online, volume_eq):
    for min_part_vol in parts_online.having_first_parts:
        archive_vol = _multi_parts_archive(min_part_vol, volume.archive)
        disjointed = [v for v in parts_online.having_first_parts if v != min_part_vol and volume_eq(archive_vol, v)]
        if disjointed:
            return [min_part_vol] + disjointed
    return []


def _add_remaining_last_parts(volume, last_parts, volume_eq):
    same = []
    for last_part_volume in last_parts:
        archive_volume = _multi_parts_archive(last_part_volume, volume.archive)
        if volume_eq(archive_volume, last_part_volume):
            same.append(last_part_volume)
    return same


def _multi_parts_archive(volume, archive):
    multi_parts = MultiParts(archive)
    for part in volume.parts:
        multi_part = ArchiveMultiPart(part.name, archive, part.number)
        multi_part.size = part.size
        multi_parts[part.number] = multi_part
    return multi_parts


def _select_online_parts(disjointed):
    parts_online = OrderedDefaultDict(list)
    for other in disjointed:
        for part in other.parts:
            if part.size:
                parts_online[part.number].append(other)
    return parts_online


class OnlineDisjointedParts(OrderedDefaultDict):
    def __init__(self, volume, volumes):
        super(OnlineDisjointedParts, self).__init__(list)
        self.max_part = max([part.number for v in [volume] + volumes for part in v.parts])
        self.volume_online_parts = valid_parts(volume)

        for v in volumes:
            for part in v.parts:
                if part.size:
                    self[part.number].append(v)

    def volume_has_first_parts(self):
        return min(self.volume_online_parts) < self.max_part

    def volume_has_max_part(self):
        return self.max_part in self.volume_online_parts

    @property
    def volumes(self):
        return no_duplicates([v for vols in self.values() for v in vols])

    @property
    def having_first_parts(self):
        return no_duplicates([v for p, vols in self.iteritems() if p < self.max_part for v in vols])

    @property
    def having_last_part(self):
        return no_duplicates([v for v in self[self.max_part]]) if self.max_part in self else []

    @property
    def having_only_last_part(self):
        return [v for v in self.having_last_part if v not in self.having_first_parts]

    def exists_containing_last_part(self):
        return self.max_part in self


def _iterate_online_parts_less_than(number):
    def iterate_parts(archive_parts):
        return (part for part in archive_parts if part.number < number if part.size)

    return iterate_parts


def _all_same(archive_parts, eq_part, part_eq=same_parts):
    archive_parts = list(archive_parts)
    return all((part_eq(part, eq_part) for part in part_numbers)) if archive_parts else False
