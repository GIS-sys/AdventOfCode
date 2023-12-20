from functools import cmp_to_key
import numpy as np


def empty_arr(size, default):
    if len(size) == 1:
        return [default for _ in range(size[0])]
    return [empty_arr(size[1:], default) for _ in range(size[0])]

class Field:
    def __init__(self, lines):
        self.lines = [list(map(int, line)) for line in lines]

#    def get_or_default(self, x, y):
#        if y >= 0 and y < len(self.cells) and x >= 0 and x < len(self.cells[y]):
#            return self.cells[y][x]
#        return Cell(".")

#    def get_neighbours(self, x, y):
#        # left, top, right, bottom
#        neighbours = []
#        if x == 0 and y == 0:
#            neighbours.append(Cell("."))
#            neighbours[-1].lights[0] = True
#        else:
#            neighbours.append(self.get_or_default(x-1, y))
#        neighbours.append(self.get_or_default(x, y-1))
#        neighbours.append(self.get_or_default(x+1, y))
#        neighbours.append(self.get_or_default(x, y+1))
#        return neighbours

    def bfs3(self):
        MAX_DISTANCE = 1_000_000_000
        # x, y, how_many_steps_already, which_direction (right, down, left, up)
        distances = empty_arr((len(self.lines), len(self.lines[0]), 4, 4), MAX_DISTANCE)
        distances[0][0][3] = [self.lines[0][0] for _ in range(4)]
        parents = empty_arr((len(self.lines), len(self.lines[0]), 4, 4), None)
        queue = [(0, 0, 3, d) for d in range(4)]
        while len(queue) > 0:
            x, y, z, d = queue[0]
            queue = queue[1:]
            # fill possible next with next cells
            possible_next = []
            if d == 0:
                possible_next.append((x+1, y, z-1, d))
                possible_next.append((x, y+1, 2, 1))
                possible_next.append((x, y-1, 2, 3))
            if d == 1:
                possible_next.append((x, y+1, z-1, d))
                possible_next.append((x+1, y, 2, 0))
                possible_next.append((x-1, y, 2, 2))
            if d == 2:
                possible_next.append((x-1, y, z-1, d))
                possible_next.append((x, y+1, 2, 1))
                possible_next.append((x, y-1, 2, 3))
            if d == 3:
                possible_next.append((x, y-1, z-1, d))
                possible_next.append((x+1, y, 2, 0))
                possible_next.append((x-1, y, 2, 2))
            # for each possible next decide if we want to go in it
            for nx, ny, nz, nd in possible_next:
                if nz < 0 or ny < 0 or ny >= len(self.lines) or nx < 0 or nx >= len(self.lines[0]):
                    continue
                if distances[nx][ny][nz][nd] > self.lines[ny][nx] + distances[x][y][z][d]:
                    distances[nx][ny][nz][nd] = self.lines[ny][nx] + distances[x][y][z][d]
                    parents[nx][ny][nz][nd] = (x, y, z, d)
                    queue.append((nx, ny, nz, nd))
        min_z, min_d = 0, 0
        for z in range(4):
            for d in range(4):
                if distances[-1][-1][z][d] < distances[-1][-1][min_z][min_d]:
                    min_z, min_d = z, d
        path = []
        cur = (len(self.lines[0])-1, len(self.lines)-1, min_z, min_d)
        while cur != None:
            path.append(cur[:2])
            cur = parents[cur[0]][cur[1]][cur[2]][cur[3]]
        path = path[::-1]
        print(path)
        self.print_with_path(path)
        #a = [[min([min([distances[y][x][z][d] for d in range(4)]) for z in range(4)]) for y in range(len(distances))] for x in range(len(distances[0]))]
        #print("\n".join(map(lambda x: " ".join(map(str, x)), a)))
        #while (i := input()):
        #    exec(i)
        return path

    def path_length(self, path):
        res = 0
        for x, y in path:
            res += self.lines[y][x]
        return res

    def print_with_path(self, path):
        self.copy = [[c for c in line] for line in self.lines]
        for x, y in path:
            self.copy[y][x] = "."
        for line in self.copy:
            print("".join(map(str, line)))
        print("")

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        lines = []
        for line in fin:
            line = line.strip()
            if line == "":
                break
            lines.append(line)
        field = Field(lines)
        path = field.bfs3()
        s = field.path_length(path[1:])
        fout.write(str(s))

