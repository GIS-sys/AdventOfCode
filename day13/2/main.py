from functools import cmp_to_key
import numpy as np


DEBUG = False

def reverseCharInLine(line, ind):
    return line[:ind] + ("." if line[ind] == "#" else "#") + line[ind+1:]

class Reflection:
    def __init__(self, hor, ver, ignore_ref):
        if not (ignore_ref is None):
            possible = [Reflection({single_hor}, {}, None) for single_hor in hor] + [Reflection({}, {single_ver}, None) for single_ver in ver]
            for new_ref in possible:
                if not(new_ref == ignore_ref):
                    self.error = new_ref.error
                    self.is_hor = new_ref.is_hor
                    self.val = new_ref.val
                    return
            self.error = True
            return
        hor = -1 if not hor else next(iter(hor))
        ver = -1 if not ver else next(iter(ver))
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
        return res

    def findReflection(self, check_error=True, ignore_ref=None):
        reflection = Reflection(self.findReflectionHor(), self.findReflectionVer(), ignore_ref)
        if check_error and reflection.isError():
            self.DEBUG_END()
        return reflection

    def findReflectionWithSmudge(self):
        original_ref = self.findReflection()
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i])):
                self.lines[i] = reverseCharInLine(self.lines[i], j)
                new_ref = self.findReflection(check_error=False, ignore_ref=original_ref)
                self.lines[i] = reverseCharInLine(self.lines[i], j)
                if new_ref == original_ref or new_ref.isError():
                    continue
                return new_ref
        self.DEBUG_END()

    def DEBUG_END(self):
        global DEBUG
        print(self.lines)
        DEBUG = True
        self.findReflectionHor()
        self.findReflectionVer()
        exit(1)

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
            reflection = pat.findReflectionWithSmudge()
            s += reflection.getScore()
        fout.write(str(s))
