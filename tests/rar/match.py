from arkiv import VolumeType, substitute_old_rar_multi_part, old_multi_part_number, match_rar, old_multi_part_rar
from arkiv.rar.match import _multi_part_rar, multi_part_with_number


def main():
    assert old_multi_part_rar('test.r01') == ('test', 3, VolumeType.RarMultiPartOld, 'r01')
    assert _multi_part_rar('test.part1.rar') == ('test', 1, VolumeType.RarMultiPart, 'part1.rar')
    assert _multi_part_rar('test.part1.rar').number == _multi_part_rar('test.part01.rar').number
    assert _multi_part_rar('test.part1.rar').number == _multi_part_rar('test.part001.rar').number
    assert _multi_part_rar('test.part10.rar') == ('test', 10, VolumeType.RarMultiPart, 'part10.rar')
    assert _multi_part_rar('test.part10.rar').number == _multi_part_rar('test.part010.rar').number
    assert _multi_part_rar('test.part010.rar').number == _multi_part_rar('test.part0010.rar').number

    assert 'test.part2.rar' == multi_part_with_number('test.part1.rar', 2)
    assert 'test.part02.rar' == multi_part_with_number('test.part01.rar', 2)
    assert 'test.part0002.rar' == multi_part_with_number('test.part0001.rar', 2)
    assert 'test.part02.rar' == multi_part_with_number('test.part10.rar', 2)
    assert 'test.part002.rar' == multi_part_with_number('test.part100.rar', 2)

    assert 'test.r00' == substitute_old_rar_multi_part('test', 2, 2)
    assert 'test.r01' == substitute_old_rar_multi_part('test', 2, 3)
    assert 'test.rar' == substitute_old_rar_multi_part('test', 2, 1)
    assert 'test.r01' == substitute_old_rar_multi_part('test', 1, 3)
    assert 'test.r00' == substitute_old_rar_multi_part('test', 12, 2)
    assert 'test.r000' == substitute_old_rar_multi_part('test', 102, 2)
    assert 'test.r001' == substitute_old_rar_multi_part('test', 102, 3)

    assert 'test.r00' == old_multi_part_number('test.rar', 2)
    assert 'test.r00' == old_multi_part_number('test.r00', 2)
    assert 'test.r01' == old_multi_part_number('test.r00', 3)
    assert 'test.rar' == old_multi_part_number('test.r00', 1)
    assert 'test.r01' == old_multi_part_number('test.rar', 3)
    assert 'test.r00' == old_multi_part_number('test.r10', 2)
    assert 'test.r000' == old_multi_part_number('test.r100', 2)
    assert 'test.r001' == old_multi_part_number('test.r100', 3)

    assert match_rar('test.RAR') == ('test', 1, VolumeType.Rar, 'RAR')
    assert match_rar('TEST.RAR') == ('TEST', 1, VolumeType.Rar, 'RAR')
    assert match_rar('test.part1.RAR') == ('test', 1, VolumeType.RarMultiPart, 'part1.RAR')
    assert match_rar('TEST.PART1.RAR') == ('TEST', 1, VolumeType.RarMultiPart, 'PART1.RAR')


if __name__ == '__main__':
    main()
