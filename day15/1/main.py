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
        for raw in sequence:
            s += apply_hash(raw)
        fout.write(str(s))

