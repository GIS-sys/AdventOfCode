from functools import cmp_to_key
import numpy as np


with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        for line in fin:
            line = line.strip()
            if line == "":
                continue
            levels = []
            levels.append(np.array(list(map(int, line.split()))))
            while np.sum(levels[-1]*levels[-1]) != 0:
                levels.append(levels[-1][1:] - levels[-1][:-1])
            for i, level in enumerate(levels):
                s += level[0] * (1 - 2 * (i % 2))
        fout.write(str(s))
