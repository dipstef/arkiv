from arkiv import VolumeType
from arkiv.zip.match import match_zip_file
from arkiv.zip.multi.match import match_zip_multi, substitute_zip_part_file_name


def main():
    assert ('test', 1, VolumeType.ZipMultiPart, 'z00') == match_zip_multi('test.z00')
    assert ('test', 2, VolumeType.ZipMultiPart, 'z01') == match_zip_multi('test.z01')

    assert 'test.z00' == substitute_zip_part_file_name('test.z00', 1)
    assert 'test.z01' == substitute_zip_part_file_name('test.z00', 2)
    assert 'test.z01' == substitute_zip_part_file_name('test.z10', 2)

    assert 'test.z00002' == substitute_zip_part_file_name('test.z00001', 3)
    assert 'test.z00001' == substitute_zip_part_file_name('test.z10000', 2)

    assert ('test.part1.rar', 1, VolumeType.Zip, 'zip') == match_zip_file('test.part1.rar.zip')


if __name__ == '__main__':
    main()
