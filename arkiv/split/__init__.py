import os
from arkiv import MultiPartFile, VolumeType
from arkiv.split.match import match_split_file, substitute_split_file_name


class SplitFile(MultiPartFile):
    def __init__(self, file_name, archive_name, archive_number):
        super(SplitFile, self).__init__(file_name, archive_name, VolumeType.Split, archive_number)
        self.file = archive_name


def split_file(file_name):
    file_split = match_split_file(file_name)
    if file_split:
        archive, archive_number = file_split[:2]
        if archive_number:
            return SplitFile(file_name, archive, archive_number)


def split_file_path(path):
    file_split = split_file(os.path.basename(path))
    if file_split:
        file_split.path = path
    return file_split


def substitute_split_file(part, missing_part):
    return substitute_split_file_name(part.name, missing_part)
