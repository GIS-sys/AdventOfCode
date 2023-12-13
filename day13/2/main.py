from functools import cmp_to_key
import numpy as np


DEBUG = False

class Pattern:
    def __init__(self, lines):
        self.lines = lines

    @staticmethod
    def findReflectionVerLine(line):
        reflections = []
        for i in range(1, len(line)):
            a = line[:i][::-1]
            b = line[i:]
            if a.startswith(b) or b.startswith(a):
                reflections.append(i)
        return reflections

    def findReflectionHor(self):
        mirrored = []
        for i in range(len(self.lines[0])):
            mirrored.append(''.join([line[i] for line in self.lines]))
        return Pattern(mirrored).findReflectionVer()

    def findReflectionVer(self):
        reflections = []
        for line in self.lines:
            reflections.append(Pattern.findReflectionVerLine(line))
        if DEBUG:
            print(f"{reflections=}")
        res = set(reflections[0])
        for ref in reflections:
            res = res.intersection(set(ref))
        if DEBUG:
            print(res)
        if len(res) == 0:
            return -1
        return next(iter(res))

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        lines = []
        patterns = []
        for line in fin:
            line = line.strip()
            if line == "":
                patterns.append(Pattern(lines))
                lines = []
                continue
            lines.append(line)
        for pat in patterns:
            hor = pat.findReflectionHor()
            ver = pat.findReflectionVer()
            if hor != -1:
                s += 100 * hor
            elif ver != -1:
                s += ver
            else:
                print(pat.lines)
                DEBUG = True
                pat.findReflectionHor()
                pat.findReflectionVer()
                exit(1)
        fout.write(str(s))
