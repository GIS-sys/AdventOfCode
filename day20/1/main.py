from collections import deque

class Pulse:
    def __init__(self, kind, fr, to):
        self.kind, self.fr, self.to = kind, fr, to

class Machine:
    def __init__(self):
        self.modules = {}
        self.broadcaster = None

    def add_module(self, line):
        module = Module(line)
        self.modules[module.name] = module
        if module.kind == "broadcaster":
            self.broadcaster = module.name

    def build(self):
        for module in self.modules.values():
            for child_name in module.children_names:
                if child_name in self.modules:
                    self.modules[child_name].add_parent(module)
        for module in self.modules.values():
            module.build()

    def pulse(self, kind):
        total_pulses = [0, 0]
        total_pulses[kind] = 1
        bfs = deque()
        bfs.append(Pulse(kind, None, self.broadcaster))
        while bfs:
            pulse = bfs.popleft()
            if not (pulse.to in self.modules):
                continue
            new_pulses = self.modules[pulse.to].pulse(pulse)
            for pulse in new_pulses:
                bfs.append(pulse)
                total_pulses[pulse.kind] += 1
        return total_pulses

class Module:
    def __init__(self, line):
        self.parents = []
        kindname, children = line.split(" -> ")
        self.children_names = children.split(", ")
        if line.startswith("broadcaster"):
            self.name = "broadcaster"
            self.kind = "broadcaster"
            return
        if kindname[0] == "%":
            self.kind = "%"
            self.name = kindname[1:]
        elif kindname[0] == "&":
            self.kind = "&"
            self.name = kindname[1:]
        else:
            self.kind = ""
            self.name = kindname

    def add_parent(self, parent_module):
        self.parents.append(parent_module)

    def build(self):
        if self.kind == "%":
            self.state = 0
        elif self.kind == "&":
            self.parents_pulses = {parent.name: 0 for parent in self.parents}

    def pulse(self, pulse):
        new_pulses = []
        if self.kind == "%":
            if pulse.kind == 1:
                return []
            self.state = 1 - self.state
            for child_name in self.children_names:
                new_pulses.append(Pulse(self.state, self.name, child_name))
        elif self.kind == "&":
            self.parents_pulses[pulse.fr] = pulse.kind
            state = 0
            for k in self.parents_pulses:
                if self.parents_pulses[k] == 0:
                    state = 1
                    break
            for child_name in self.children_names:
                new_pulses.append(Pulse(state, self.name, child_name))
        elif self.kind == "broadcaster":
            for child_name in self.children_names:
                new_pulses.append(Pulse(pulse.kind, self.name, child_name))
        else:
            raise Exception("idk how to process this pulse")
        return new_pulses

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        machine = Machine()
        for line in fin:
            line = line.strip()
            if line == "":
               break
            machine.add_module(line)
        machine.build()
        total_pulses = [0, 0]
        for _ in range(1000):
            a, b = machine.pulse(0)
            total_pulses = [total_pulses[0] + a, total_pulses[1] + b]
        s = total_pulses[0] * total_pulses[1]
        fout.write(str(s))

