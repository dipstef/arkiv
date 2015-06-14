from collections import OrderedDict

from .type import OnePartArchive, MultiParts
from ..archive import is_archive, is_multi_part_archive


class ArchiveGroups(OrderedDict):
    def __init__(self, single_volume=OnePartArchive, multi_parts=MultiParts, archive_group_by=lambda a: a.archive):
        super(ArchiveGroups, self).__init__()
        self._archive_id = archive_group_by
        self._single_volume = single_volume
        self._multi_parts = multi_parts

    def group_archives(self, archives):
        for archive in archives:
            self.add_archive(archive)

    def add_archive(self, archive):
        if is_archive(archive):
            self._add_archive(self._archive_id(archive), archive)

    def _add_archive(self, archive_id, archive):
        if is_multi_part_archive(archive):
            archive_volumes = self._multi_part_volume(archive_id)
            archive_volumes[archive.number] = archive
        else:
            volume = self.get(archive_id)
            if volume:
                volume.extract_file = archive
            else:
                self[archive_id] = self._single_volume(archive)

    def get_archive_volume(self, archive):
        return self.get(self._archive_id(archive))

    def _multi_part_volume(self, archive_id):
        try:
            volume_group = self[archive_id]
        except KeyError:
            volume_group = self._multi_parts(archive_id)
            self[archive_id] = volume_group
        return volume_group

    @property
    def volumes(self):
        return self.values()


def archive_part(archive):
    if is_multi_part_archive(archive):
        return archive.number
    elif is_archive(archive):
        return 1
