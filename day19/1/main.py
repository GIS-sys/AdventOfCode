from collections import deque

class Condition:
    def __init__(self, line):
        if not (":" in line):
            self.simple = True
            self.name = line
            return
        self.simple = False
        self.cond, self.name = line.split(":")

    def applicable(self, part):
        if self.simple:
            return True
        cond = self.cond
        cond = cond.replace("x", str(part.x))
        cond = cond.replace("m", str(part.m))
        cond = cond.replace("a", str(part.a))
        cond = cond.replace("s", str(part.s))
        return eval(cond)

class Workflow:
    def __init__(self, line):
        self.name = line[:line.index("{")]
        line = line[line.index("{") + 1:line.index("}")]
        self.conditions = [Condition(line) for line in line.split(",")]

    def go(self, part):
        for cond in self.conditions:
            if cond.applicable(part):
                return cond.name
        raise Exception("Workflow.go - unknown part for conditions")

class Part:
    def __init__(self, line):
        line = line.replace("{", "{'").replace("=", "':").replace(",", ",'")
        parsed = eval(line)
        self.x, self.m, self.a, self.s = map(int, (parsed["x"], parsed["m"], parsed["a"], parsed["s"]))

class Step:
    def __init__(self, part, name):
        self.part = part
        self.name = name

    def go(self, workflows):
        self.name = workflows[self.name].go(self.part)

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        workflows = {}
        steps = []
        mod = 0
        for line in fin:
            line = line.strip()
            if line == "":
                mod += 1
                if mod == 2:
                    break
                continue
            if mod == 0:
                w = Workflow(line)
                workflows[w.name] = w
            else:
                steps.append(Step(Part(line), "in"))
        for step in steps:
            while not (step.name in "AR"):
                step.go(workflows)
            if step.name == "A":
                s += step.part.x + step.part.m + step.part.a + step.part.s
        fout.write(str(s))

