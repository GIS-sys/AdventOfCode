from collections import deque

MIN, MAX = 1, 4000

class Condition:
    def __init__(self, line):
        if not (":" in line):
            self.simple = True
            self.name = line
            return
        self.simple = False
        self.cond, self.name = line.split(":")
        i = -1
        if "<" in self.cond:
            i = self.cond.index("<")
        else:
            i = self.cond.index(">")
        self.cond_arg = self.cond[:i]
        self.cond_sgn = self.cond[i]
        self.cond_val = int(self.cond[i+1:])

    def split(self, step):
        if self.simple:
            return Step(step.part.copy(), self.name), Step(None, "R")
        step_a = Step(None, self.name)
        step_b = Step(None, "")
        if self.cond_sgn == "<":
            argval = getattr(step.part, self.cond_arg)
            inter = self.cond_val
            step_a.part = step.part.copy(**{self.cond_arg: [argval[0], inter-1]})
            step_b.part = step.part.copy(**{self.cond_arg: [inter, argval[1]]})
        else:
            argval = getattr(step.part, self.cond_arg)
            inter = min(max(self.cond_val, argval[0]), argval[1])
            step_b.part = step.part.copy(**{self.cond_arg: [argval[0], inter]})
            step_a.part = step.part.copy(**{self.cond_arg: [inter+1, argval[1]]})
        return step_a, step_b

class Workflow:
    def __init__(self, line):
        self.name = line[:line.index("{")]
        line = line[line.index("{") + 1:line.index("}")]
        self.conditions = [Condition(line) for line in line.split(",")]

    def go(self, step):
        new_steps = [step]
        for cond in self.conditions:
            a, b = cond.split(new_steps[-1])
            new_steps.pop()
            new_steps.append(a)
            new_steps.append(b)
        return new_steps

class Part:
    def __init__(self, x, m, a, s):
        self.x, self.m, self.a, self.s = x, m, a, s

    def amount(self):
        return max(0, self.x[1] - self.x[0] + 1) * max(0, self.m[1] - self.m[0] + 1) * max(0, self.a[1] - self.a[0] + 1) * max(0, self.s[1] - self.s[0] + 1)

    def copy(self, x=None, m=None, a=None, s=None):
        return Part(
            (self.x if x is None else x),
            (self.m if m is None else m),
            (self.a if a is None else a),
            (self.s if s is None else s)
        )

    def __repr__(self):
        return f"(x={self.x},m={self.m},a={self.a},s={self.s})"

class Step:
    def __init__(self, part, name):
        self.part = part
        self.name = name

    def __repr__(self):
        return self.name + ":" + str(self.part)

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        workflows = {}
        for line in fin:
            line = line.strip()
            if line == "":
                break
            w = Workflow(line)
            workflows[w.name] = w
        bfs = deque()
        bfs.append(Step(Part([MIN, MAX], [MIN, MAX], [MIN, MAX], [MIN, MAX]), "in"))
        while bfs:
            #step = bfs.popleft() # TODO reuse this
            step = bfs.pop()
            print(len(bfs))
            print(step)
            if step.name in "AR":
                if step.name == "A":
                    s += step.part.amount()
                continue
            if step.part.amount == 0:
                continue
            workflow = workflows[step.name]
            new_steps = workflow.go(step)
            for new_step in new_steps[::-1]: # TODO remove -1
                bfs.append(new_step)
        fout.write(str(s))

