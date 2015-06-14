from collections import OrderedDict
from .group import ArchiveGroups
from .type import OnePartArchive, MultiParts
from .parts import has_all_parts
from .substitutes import join_archive_parts, archive_parts_names


class ArchiveGroupsCompletion(ArchiveGroups):
    def __init__(self, single_volume=OnePartArchive, multi_parts=MultiParts, archive_group_by=lambda a: a.archive):
        super(ArchiveGroupsCompletion, self).__init__(single_volume, multi_parts, archive_group_by)

    @property
    def incomplete_volumes(self):
        return [vol for vol in self.volumes if not has_all_parts(vol)]

    @property
    def complete_volumes(self):
        return [vol for vol in self.volumes if has_all_parts(vol)]

    def duplicates(self, volume):
        return []

    def substitutes_for_part(self, volume, part_number):
        parts = []
        for same_volume_group in self.duplicates(volume):
            if part_number in same_volume_group:
                parts.append(same_volume_group[part_number])
        return parts

    def missing_parts_substitutes(self, volume):
        return self.parts_substitutes(volume, volume.missing_parts)

    def missing_parts_names(self, volume):
        parts = join_archive_parts(volume, self.missing_parts_substitutes(volume))
        return archive_parts_names(parts, volume.missing_parts)

    def parts_substitutes(self, volume, parts):
        substitutes = OrderedDict()
        for missing_part in parts:
            volume_substitutes = self.substitutes_for_part(volume, missing_part)
            if volume_substitutes:
                substitutes[missing_part] = volume_substitutes
        return substitutes
