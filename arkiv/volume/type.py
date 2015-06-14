from collections import OrderedDict
from UserDict import DictMixin
from arkiv import PartOfArchive


class OnePartArchive(PartOfArchive):
    def __init__(self, extract_file):
        super(OnePartArchive, self).__init__(extract_file.archive)
        self.is_multi_part = False
        self.extract_file = extract_file

    @property
    def extract_file(self):
        return self._extract_file

    @extract_file.setter
    def extract_file(self, extract_file):
        self._extract_file = extract_file
        self.archive = extract_file.archive
        extract_file.volume = self
        extract_file.number = 1

    @property
    def parts(self):
        return [self.extract_file]

    @property
    def part_numbers(self):
        return 1

    @property
    def size(self):
        return sum((part.size for part in self.parts))

    def __getattr__(self, item):
        return getattr(self.extract_file, item)

    def __len__(self):
        return int(bool(self.extract_file))

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.extract_file.__dict__.iteritems() if not key == 'volume']

        return 'Extract File: %s(%s)' % (self.__class__.__name__, ', '.join(L))


class MultiParts(PartOfArchive, DictMixin):
    def __init__(self, archive, parts=None):
        super(MultiParts, self).__init__(archive)
        self.archive = archive
        self.is_multi_part = True
        self._parts = OrderedDict()
        parts = parts or []
        for part in sorted(parts, key=lambda p: p.number):
            self[part.number] = part

    @property
    def size(self):
        size = 0
        for volume in self.parts:
            size += volume.size
        return size

    @property
    def extract_file(self):
        return self[1] if 1 in self else None

    @property
    def part_numbers(self):
        return sorted(self.keys())

    @property
    def parts(self):
        return [archive_part for part, archive_part in sorted(self.iteritems(), key=lambda t: t[0])]

    def keys(self):
        return self._parts.keys()

    def values(self):
        return self._parts.values()

    def iteritems(self):
        return self._parts.iteritems()

    def __setitem__(self, part_number, archive):
        self._parts[part_number] = archive
        archive.volume = self

    def __getitem__(self, part_number):
        return self._parts[part_number]

    def __delitem__(self, part_number):
        del self._parts[part_number]

    def __len__(self):
        return len(self._parts)

    def __repr__(self):
        return repr(self._parts)
