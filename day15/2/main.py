from functools import cmp_to_key
import numpy as np


def apply_hash(raw):
    current_value = 0
    for c in raw:
        asc = ord(c)
        current_value += asc
        current_value *= 17
        current_value %= 256
    return current_value

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        sequence = ""
        for line in fin:
            line = line.strip()
            if line == "":
                break
            sequence += line
        sequence = line.split(",")
        boxes = [[] for _ in range(256)]
        for raw in sequence:
            if raw[-1] == "-":
                label = raw[:-1]
                operation = "-"
                value = None
            else:
                label = raw[:-2]
                operation = "="
                value = int(raw[-1])
            # print(label, operation, value)
            h = apply_hash(label)
            if operation == "-":
                i = None
                for i in range(len(boxes[h])):
                    if boxes[h][i][0] == label:
                        boxes[h].pop(i)
                        break
            if operation == "=":
                i = 0
                for i in range(len(boxes[h])):
                    if boxes[h][i][0] == label:
                        boxes[h][i] = (label, value)
                        i = None
                        break
                if not (i is None):
                    boxes[h].append((label, value))
            # print(boxes)
        for i, box in enumerate(boxes):
            for j, lens in enumerate(box):
                k = lens[1]
                # print(i, j, k)
                s += (i + 1) * (j + 1) * k
        fout.write(str(s))

