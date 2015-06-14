from arkiv import MultiPartFile
from .match import *


class RarMultiPartOld(MultiPartFile):
    def __init__(self, file_name, archive_name, number):
        super(RarMultiPartOld, self).__init__(file_name, archive_name, VolumeType.RarMultiPartOld, number)
