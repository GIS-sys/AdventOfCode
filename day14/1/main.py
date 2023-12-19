from functools import cmp_to_key
import numpy as np


def assign_to_string(raw, index, char):
    return raw[:index] + char + raw[index+1:]

class Dish:
    def __init__(self, lines):
        self.dish = lines

    def tilt_column(self, column):
        last_free = 0
        for row in range(len(self.dish)):
            if self.dish[row][column] == "O":
                if row == last_free:
                    last_free += 1
                else:
                    self.dish[last_free] = assign_to_string(self.dish[last_free], column, self.dish[row][column])
                    self.dish[row] = assign_to_string(self.dish[row], column, ".")
                    last_free += 1
                    while last_free < len(self.dish) and self.dish[last_free][column] == "#":
                        last_free += 1
            elif self.dish[row][column] == "#":
                last_free = row + 1

    def tilt(self):
        for column in range(len(self.dish[0])):
            self.tilt_column(column)

    def rotate(self):
        new_lines = []
        for x in range(len(self.dish[0])):
            new_line = ""
            for y in range(len(self.dish)-1, -1, -1):
                new_line += self.dish[y][x]
            new_lines.append(new_line)
        self.dish = new_lines

    def cycle(self):
        for _ in range(4):
            #print(self)
            self.tilt()
            #print(self)
            self.rotate()

    def weight(self):
        total = 0
        for anti_height, row in enumerate(self.dish):
            height = len(self.dish) - anti_height
            for c in row:
                if c == "O":
                    total += height
        return total

    def __repr__(self):
        return "\n".join(self.dish) + "\n"

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        lines = []
        for line in fin:
            line = line.strip()
            if line == "":
                break
            lines.append(line)
        dish = Dish(lines)
        dish.tilt()
        s = dish.weight()
        fout.write(str(s))

