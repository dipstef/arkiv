import os
from arkiv import ArchiveFileName, VolumeType
from arkiv.zip.match import match_zip_file
from arkiv.zip.multi import ZipMultiPart
from arkiv.zip.multi.match import substitute_zip_part_file_name


class ArchiveZip(ArchiveFileName):
    def __init__(self, file_name):
        super(ArchiveZip, self).__init__(file_name, VolumeType.Zip)


def is_zip_file(file_name):
    return bool(zip_file(file_name))


def zip_file(file_name):
    file_zip = match_zip_file(file_name)
    if file_zip:
        return ArchiveZip(file_name) if file_zip.type == VolumeType.Zip else ZipMultiPart(file_name, *file_zip[:2])


def zip_path(path):
    file_zip = zip_file(os.path.basename(path))
    if file_zip:
        file_zip.path = path
    return file_zip


def substitute_zip_part(part, substitute):
    return substitute_zip_part_file_name(part.name, substitute)
