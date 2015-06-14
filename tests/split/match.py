from arkiv import VolumeType
from arkiv.split.match import match_split_file, substitute_split_file_name
from arkiv.split.letter import letter_split
from arkiv.split.digit import digit_split


def main():
    assert not match_split_file('asd.002')
    assert not match_split_file('asd.net.002')
    assert not match_split_file('a.b.c.d.e.f.g.h.net.002')
    assert not match_split_file('a.b.c.d.e.f.g.h.i.3.0')
    assert not match_split_file('a.b.c.d.e.f.g.h.i.3.03')

    assert ('test.rar', 1, VolumeType.Split, '01') == match_split_file('test.rar.01')
    assert digit_split('test.rar.01').number == match_split_file('test.rar.01').number
    assert digit_split('test.rar.01').number == match_split_file('test.rar.001').number
    assert ('test.rar', 10, VolumeType.Split, '10') == match_split_file('test.rar.10')

    assert ('test.rar', 1, VolumeType.Split, '_a') == match_split_file('test.rar._a')
    assert letter_split('test.rar._a').number == match_split_file('test.rar.__a').number
    assert letter_split('test.rar._a').number == match_split_file('test.rar.___a').number

    assert 'test.rar.02' == substitute_split_file_name('test.rar.01', 2)
    assert 'test.rar.002' == substitute_split_file_name('test.rar.001', 2)
    assert 'test.rar.02' == substitute_split_file_name('test.rar.10', 2)
    assert 'test.rar.002' == substitute_split_file_name('test.rar.100', 2)
    assert 'test.rar.00002' == substitute_split_file_name('test.rar.00100', 2)

    assert 'test.rar._b' == substitute_split_file_name('test.rar._a', 2)
    assert 'test.rar.__b' == substitute_split_file_name('test.rar.__a', 2)

    assert match_split_file('test.mp4.002.001')


if __name__ == '__main__':
    main()
