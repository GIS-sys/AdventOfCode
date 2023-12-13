from functools import cmp_to_key
import numpy as np


DEBUG = False

class Reflection:
    def __init__(self, hor, ver):
        self.error = False
        if hor != -1:
            self.is_hor = True
            self.val = hor
        elif ver != -1:
            self.is_hor = False
            self.val = ver
        else:
            self.error = True

    def isError(self):
        return self.error

    def isHor(self):
        return self.is_hor

    def isVer(self):
        return not self.isHor()

    def getVal(self):
        return self.val

    def getScore(self):
        return self.val if not self.isHor() else self.val * 100

    def __eq__(self, other):
        return not self.isError() and not other.isError() and self.isHor() == other.isHor() and self.getVal() == other.getVal()

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

    def findReflection(self):
        reflection = Reflection(self.findReflectionHor(), self.findReflectionVer())
        if reflection.isError():
            print(self.lines)
            DEBUG = True
            self.findReflectionHor()
            self.findReflectionVer()
            exit(1)
        return reflection

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
            reflection = pat.findReflection()
            s += reflection.getScore()
        fout.write(str(s))
