from arkiv import split_file, substitute_split_file
from arkiv.split.match import match_split_file


def main():
    assert not match_split_file('softarchive.net_Working.with.NHibernate.3.0')
    assert not match_split_file('softarchive.net_Working.with.NHibernate.3.03')

    assert 'test.rar.02' == substitute_split_file(split_file('test.rar.01'), 2)
    assert 'test.rar.002' == substitute_split_file(split_file('test.rar.001'), 2)
    assert 'test.rar.02' == substitute_split_file(split_file('test.rar.10'), 2)
    assert 'test.rar.002' == substitute_split_file(split_file('test.rar.100'), 2)
    assert 'test.rar.00002' == substitute_split_file(split_file('test.rar.00100'), 2)
    assert 'test.rar._b' == substitute_split_file(split_file('test.rar._a'), 2)
    assert 'test.rar.__b' == substitute_split_file(split_file('test.rar.__a'), 2)


if __name__ == '__main__':
    main()
