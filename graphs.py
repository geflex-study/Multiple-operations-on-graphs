"""
Здесь я, на всякий случай, напишу, что я Димитрий Гефлих
"""
from itertools import zip_longest
import operator as op
import re


sp = re.compile(r'\s+')


class Matrix:
    def __init__(self, data=None):
        self.data = data or []

    def __str__(self):
        result = []
        for line in self.data:
            result.append(' '.join(str(v) for v in line))
        return '\n'.join(result)

    def _map(self, other, operator):
        new = Matrix()
        for ln1, ln2 in zip_longest(self.data, other.data):
            if ln1 is None: ln1 = []
            if ln2 is None: ln2 = []
            ln = []
            for v1, v2 in zip_longest(ln1, ln2):
                if v1 is None: v1 = 0
                if v2 is None: v2 = 0
                ln.append(int(operator(v1, v2)))
            new.data.append(ln)
        return new

    def __or__(self, other):
        return self._map(other, op.or_)

    def __and__(self, other):
        return self._map(other, op.and_)

    def __sub__(self, other):
        return self._map(other, lambda x, y: x and not y)

    @classmethod
    def from_str(cls, s):
        s = s.strip()
        new = cls()
        for line in s.splitlines():
            line = [int(v) for v in re.split(sp, line)]
            new.data.append(line)
        return new

    @classmethod
    def from_dict(cls, d):
        nums = set()
        for n, v in d.items():
            nums.add(n)
            nums.update(v)
        size = max(nums) + 1
        new = cls()
        for n in range(size):
            ln = [0 for _ in range(size)]
            for pair in d.get(n, []):
                ln[pair] = 1
            new.data.append(ln)
        return new

    @classmethod
    def from_bntu(cls, s):
        s = re.sub(sp, '', s)
        d = {}
        for edge in s.split(';'):
            if edge:
                n = int(edge[0]) - 1
                paired = edge.split('(')[-1][:-1].split(',')
                d[n] = [int(v)-1 for v in paired]
        return cls.from_dict(d)

    def to_editor(self):
        res = [str(i) for i in range(len(self.data))]
        for edge_num, line in enumerate(self.data):
            for paired_num, v in enumerate(line):
                if v:
                    res.append(f'{edge_num} {paired_num}')
        return '\n'.join(res)


graph25 = Matrix.from_bntu('1 ( 2,3,4,5,6) ; 2( 1,4) ; 3 (4,5 ) ; 4( 1,2,6); 5( 1,3) ; 6(1,4)')
graph26 = Matrix.from_bntu('1 ( 2,3) ; 2( 1,4) ; 3 (1,4,5 ) ; 4( 3,5,6); 5( 3,4) ; 6(3,5)')
graph27 = Matrix.from_bntu('1 ( 2,3,6) ; 2(3,5) ; 3 ( 4,5,6) ; 4(3,5,6,8); 5(2,3,4,7,8) ; 6(3,4,8) ;7(5,8); 8(4,5,6,7)')
graph28 = Matrix.from_bntu('1 ( 2,3,6) ; 2(1,4,5) ; 3 ( 1,4,6) ; 4(2,3,5,6); 5(2,4) ; 6(3,4) ;7(4,5,6)')


def print_matrix(matrix):
    print(matrix, '\n')
    print(matrix.to_editor(), '\n')
