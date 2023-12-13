from functools import cmp_to_key
import numpy as np


FACTOR = 1000000

def countNumbersInBetween(arr, left, right):
    count = 0
    for x in arr:
        if left < x and x < right:
            count += 1
    return count

class Field:
    def __init__(self, rows):
        self.rows = rows
        self.precalcEmptys()
        print(self.emptyCol, self.emptyRow)

    def precalcEmptys(self):
        self.emptyCol = []
        for y in range(len(self.rows[0])):
            occupied = False
            for x in range(len(self.rows)):
                if self.rows[x][y] == "#":
                    occupied = True
                    break
            if not occupied:
                self.emptyCol.append(y)
        self.emptyRow = []
        for x in range(len(self.rows)):
            occupied = False
            for y in range(len(self.rows[0])):
                if self.rows[x][y] == "#":
                    occupied = True
                    break
            if not occupied:
                self.emptyRow.append(x)

    def galaxies(self):
        for x in range(len(self.rows)):
            for y in range(len(self.rows[x])):
                if self.rows[x][y] == "#":
                    yield (x,y)

    def shortestPath(self, a, b):
        # TODO
        s = 0
        s += countNumbersInBetween(self.emptyRow, min(a[0], b[0]), max(a[0], b[0]))
        s += countNumbersInBetween(self.emptyCol, min(a[1], b[1]), max(a[1], b[1]))
        print(f"{s=}")
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + s * (FACTOR-1)
        #return abs(a[0] - b[0]) + abs(a[1] - b[1]) + 1

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        field = Field([x for x in map(str.strip, fin.read().split("\n")) if x != ""])
        #print(field.emptyCol, field.emptyRow, "col row")
        for a in field.galaxies():
            for b in field.galaxies():
                if a != b:
                    shPath = field.shortestPath(a, b)
                    print(a, b, shPath)
                    s += shPath
        fout.write(str(s // 2))
