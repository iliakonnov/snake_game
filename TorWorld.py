# -*- coding:utf8 -*-


class TorWorld:
    def __init__(self, x, y=None):  # Set world size
        self.changes = {}
        if y is None:
            self._ReadFromFile(x)
        else:
            self.width = x
            self.height = y
            self.table = [[None] * self.width for j in range(self.height)]

    def _ReadFromFile(self, fileName):
        legend = {'+': 3, '*': 4, '-': None}
        lvl_file = open(fileName)
        lines = lvl_file.readlines()
        self.height = len(lines)
        self.width = len(lines[0].rstrip('\n'))

        self.table = [[None] * self.width for j in range(self.height)]
        print(lines[0])
        print(self.width)

        for i in range(self.height):
            for j in range(self.width):
                symbol = lines[i][j]
                code = legend[symbol]
                self.table[i][j] = code
                self.changes[(i, j)] = code

    def GetCell(self, x, y):  # Get ID in cell
        (x, y) = self._Normalize(x, y)
        return self.table[y][x]

    def PutCell(self, x, y, ID):  # Set ID in cell
        (x, y) = self._Normalize(x, y)
        self.changes[(x, y)] = ID
        self.table[y][x] = ID

    def IsEmpty(self, x, y):
        return self.GetCell(x, y) is None

    def Clear(self, x, y):
        self.PutCell(x, y, None)

    def GetDiff(self):
        result = self.changes
        self.changes = {}
        return result

    def _Normalize(self, x, y):
        x = self._NormalizeSeg(x, self.width)
        y = self._NormalizeSeg(y, self.height)
        return(x, y)

    def _NormalizeSeg(self, pos, size):
        while pos >= size:
            pos = pos - size

        while pos < 0:
            pos = pos + size

        return pos

if __name__ == "__main__":
    T = TorWorld(7, 8)
    assert T.GetCell(3, 4) is None, "TEST 1 ERROR"

    T.PutCell(2, 3, 3)
    assert T.GetCell(2, 3) == 3, "TEST 2 ERROR"

    T.PutCell(10, 17, 4)
    assert T.GetCell(10, 17) == 4, "TEST 3 ERROR"
    assert T.GetCell(3, 1) == 4, "TEST 4 ERROR"

    T.PutCell(-10, -17, 4)
    assert T.GetCell(-10, -17) == 4, "TEST 5 ERROR"
    assert T.GetCell(4, 7) == 4, "TEST 6 ERROR"

    T.PutCell(23, 34, 17)
    assert not T.IsEmpty(23, 34), "ERROR TEST 7"

    T.Clear(23, 34)
    assert T.IsEmpty(23, 34), "ERROR TEST 8"

    print("SUCCESS!")
