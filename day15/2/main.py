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
        indexes = {}
        boxes = [[] for _ in range(256)]
        for raw in sequence:
            label = raw[:2]
            operation = raw[2]
            value = (int(raw[3]) if operation == "=" else None)
            h = apply_hash(label)
            if operation == "-":
                if not (label in indexes):
                    continue
                boxes[h].pop(indexes[label])
                indexes.pop(label)
            if operation == "=":
                if label in indexes:
                    boxes[h][indexes[label]] = (label, value)
                else:
                    boxes[h].append((label, value))
                    indexes[label] = len(boxes[h]) - 1
        for i, box in enumerate(boxes):
            for j, lens in enumerate(box):
                k = lens[1]
                print(i, j, k)
                s += (i + 1) * (j + 1) * k
        fout.write(str(s))

