from functools import cmp_to_key
import numpy as np


def _get_connected(c):
    if c == "|":
        return ((1,0), (-1,0))
    elif c == "-":
        return ((0,1), (0,-1))
    elif c == "L":
        return ((-1,0), (0,1))
    elif c == "J":
        return ((-1,0), (0,-1))
    elif c == "7":
        return ((1,0), (0,-1))
    elif c == "F":
        return ((1,0), (0,1))
    elif c == ".":
        return []
    elif c == "S":
        return []

def get_connected(c, base):
    return [np.array(x)+base for x in _get_connected(c)]

def contains(arr, pos):
    for x in arr:
        if np.sum((x - pos)**2) == 0:
            return True
    return False

def get_not_equal(arr, el):
    for x in arr:
        if np.sum((x - el)**2) != 0:
            return x

class Field:
    def __init__(self, rows):
        self.rows = rows

    def get_loop(self):
        S = np.array((-1, -1))
        for x, r in enumerate(self.rows):
            for y, c in enumerate(r):
                if c == 'S':
                    S = np.array((x, y))
        x, y = S[0], S[1]
        path = [S]
        if x > 0 and contains(get_connected(self.rows[x-1][y], np.array((x-1,y))), S):
            path.append(np.array((x-1,y)))
            #path.append(get_not_equal(get_connected(self.rows[x-1][y], np.array((x-1,y))), S))
        elif x < len(self.rows)-1 and contains(get_connected(self.rows[x+1][y], np.array((x+1,y))), S):
            path.append(np.array((x+1,y)))
            #path.append(get_not_equal(get_connected(self.rows[x+1][y], np.array((x+1,y))), S))
        elif y > 0 and contains(get_connected(self.rows[x][y-1], np.array((x,y-1))), S):
            path.append(np.array((x,y-1)))
            #path.append(get_not_equal(get_connected(self.rows[x][y-1], np.array((x,y-1))), S))
        elif y < len(self.rows[0])-1 and contains(get_connected(self.rows[x][y+1], np.array((x,y+1))), S):
            path.append(np.array((x,y+1)))
            #path.append(get_not_equal(get_connected(self.rows[x][y+1], np.array((x,y+1))), S))
        while not (path[-1] is None):
            #print(path)
            a, b = path[-2], path[-1]
            path.append(get_not_equal(get_connected(self.rows[b[0]][b[1]], b), a))
        return path

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        field = Field([x for x in map(str.strip, fin.read().split("\n")) if x != ""])
        s = (len(field.get_loop())-2) // 2
        fout.write(str(s))
