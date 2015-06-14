from collections import namedtuple
import os

from unicoder import encoded, to_unicode
from .type import is_multi_part_volume_type, VolumeType


ArchiveID = namedtuple('ArchiveID', ('name', 'type'))

ArchiveTuple = namedtuple('ArchiveTuple', ('archive', 'number', 'type', 'extension'))


class PartOfArchive(object):

    def __init__(self, archive):
        self.archive = archive


class FileArchive(PartOfArchive):
    def __init__(self, file_name, archive):
        super(FileArchive, self).__init__(archive)
        self.name = file_name


class ArchiveMultiPart(PartOfArchive):
    def __init__(self, file_name, archive, number):
        super(ArchiveMultiPart, self).__init__(archive)
        self.name = file_name
        self.number = number


class FileNameArchive(FileArchive):

    def __init__(self, file_name, archive_name, archive_type):
        super(FileNameArchive, self).__init__(file_name, ArchiveID(archive_name, archive_type))

    def __str__(self):
        return encoded(unicode(self))

    def __unicode__(self):
        return unicode(self.name)


class ArchiveFileName(FileNameArchive):

    def __init__(self, file_name, archive_type):
        super(ArchiveFileName, self).__init__(file_name, os.path.splitext(file_name)[0], archive_type)


class MultiPartFile(ArchiveMultiPart):

    def __init__(self, file_name, archive_name, archive_type, number):
        super(MultiPartFile, self).__init__(file_name, ArchiveID(archive_name, archive_type), number)

    def __str__(self):
        return encoded(unicode(self))

    def __unicode__(self):
        return u'%s, Multi Volume, volume: %s' % (to_unicode(self.name), self.number)


def is_archive(archive_obj):
    return isinstance(archive_obj, PartOfArchive)


def is_multi_part_archive(archive_obj):
    return is_archive(archive_obj) and is_multi_part_volume_type(archive_obj.archive.type)


def is_multi_part_with_extract(archive):
    return is_multi_part_archive(archive) and archive_multi_extract_part(archive)


def is_multi_part_extract(archive):
    return is_multi_part_archive(archive) and archive.number == 1


def is_split_archive(archive):
    return is_archive(archive) and archive.archive.type == VolumeType.Split


def archive_multi_extract_part(archive):
    return archive if is_multi_part_extract(archive) else archive.volume.extract_file


def is_archive_secondary_part(archive):
    return is_multi_part_archive(archive) and archive.number > 1


def is_archive_extract(archive):
    return is_archive(archive) and (is_multi_part_extract(archive) or not is_multi_part_archive(archive))


def main():
    print ArchiveFileName('test.zip', VolumeType.Rar)

if __name__ == '__main__':
    main()