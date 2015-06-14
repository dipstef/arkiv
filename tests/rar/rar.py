from arkiv.rar import match_rar_archive, is_rar_file, substitute_rar_part, RarMultiPartOld


def main():
    assert match_rar_archive('asd.part1.rar')
    assert is_rar_file('Learn Python.rar')

    assert 'test.part2.rar' == substitute_rar_part(match_rar_archive('test.part1.rar'), 2)
    assert 'test.part02.rar' == substitute_rar_part(match_rar_archive('test.part01.rar'), 2)
    assert 'test.part02.rar' == substitute_rar_part(match_rar_archive('test.part10.rar'), 2)
    assert 'test.part002.rar' == substitute_rar_part(match_rar_archive('test.part100.rar'), 2)

    assert 'test.r00' == substitute_rar_part(match_rar_archive('test.r00'), 2)
    assert 'test.r01' == substitute_rar_part(match_rar_archive('test.r00'), 3)
    assert 'test.rar' == substitute_rar_part(match_rar_archive('test.r00'), 1)
    assert 'test.r01' == substitute_rar_part(RarMultiPartOld('test.rar', 'test', 1), 3)
    assert 'test.r00' == substitute_rar_part(match_rar_archive('test.r10'), 2)
    assert 'test.r000' == substitute_rar_part(match_rar_archive('test.r100'), 2)
    assert 'test.r001' == substitute_rar_part(match_rar_archive('test.r100'), 3)


if __name__ == '__main__':
    main()
