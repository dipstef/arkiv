from arkiv import MultiPartFile, VolumeType


class ZipMultiPart(MultiPartFile):
    def __init__(self, file_name, archive_name, number):
        super(ZipMultiPart, self).__init__(file_name, archive_name, VolumeType.ZipMultiPart, number)
