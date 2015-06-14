class VolumeType(object):
    Rar = 'rar'
    RarMultiPart = "rar_multi"
    RarMultiPartOld = "rar_multi_old"
    Split = 'split'
    Zip = 'zip'
    ZipMultiPart = 'zip_multi'
    Zip7 = '7z'

    multi_part = [RarMultiPart, RarMultiPartOld, Split, ZipMultiPart]
    single_part = [Rar, Zip, Zip7]


def is_multi_part_volume_type(volume_type):
    return volume_type in VolumeType.multi_part
