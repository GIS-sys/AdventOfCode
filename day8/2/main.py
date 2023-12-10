from functools import cmp_to_key

class Map:
    def __init__(self):
        self.nodes = {}

    def add(self, line):
        data = line.split(" ")
        nodeFrom = data[0]
        nodeLeft = data[2][1:-1]
        nodeRight = data[3][:-2]
        self.nodes[nodeFrom] = (nodeLeft, nodeRight)

    def allStart(self):
        return [node for node in self.nodes if node[-1] == "A"]

    def start(self, nodeFrom):
        self.currentNode = nodeFrom

    def current(self):
        return self.currentNode

    def next(self, instruction):
        self.currentNode = self.nodes[self.currentNode][0 if instruction == "L" else 1]

def nokN(arr):
    if len(arr) == 1:
        return arr[0]
    if len(arr) > 2:
        return nokN([nokN(arr[:2])] + arr[2:])
    a, b = arr
    while a != 0:
        a, b = b%a, a
    return arr[0] * arr[1] // b

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        m = Map()
        for step, line in enumerate(fin):
            if step == 0:
                instructions = line[:-1]
                continue
            if line.strip() == "":
                continue
            m.add(line)
        i = 0
        startNodes = m.allStart()
        loops = []
        for startNode in startNodes:
            loops.append(0)
            m.start(startNode)
            while m.current()[-1] != "Z":
                m.next(instructions[i])
                i = (i + 1) % len(instructions)
                loops[-1] += 1
        s = nokN(loops)
        fout.write(str(s))
