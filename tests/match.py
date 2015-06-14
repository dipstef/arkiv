from arkiv import match_archive, is_multi_part_file_name, archive_extension


def main():
    assert not match_archive(None)

    assert is_multi_part_file_name('test.part1.rar')
    assert 'part1.rar' == archive_extension('test.part1.rar')
    assert 'r01' == archive_extension('test.r01')
    assert 'z01' == archive_extension('test.z01')
    assert '01' == archive_extension('test.rar.01')

    assert 'part1.rar' == archive_extension('test.part1.RAR')


if __name__ == '__main__':
    main()
