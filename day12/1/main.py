from functools import cmp_to_key
import numpy as np


def permutations(record, numbers, history=""):
    while len(numbers) != 0 and numbers[0] == 0:
        numbers = numbers[1:]
        if len(record) != 0:
            if record[0] == "#":
                return 0
            record = record[1:]
            history = history + "."
    while len(record) != 0 and record[0] == ".":
        record = record[1:]
        history = history + "."
    print(f"perm {record=}, {numbers=}")
    if len(record) == 0:
        if len(numbers) == 0:
            print(history)
        return 0 if len(numbers) != 0 else 1
    if len(numbers) == 0:
        if not ("#" in record):
            print(history + "." * len(record))
        return 0 if ("#" in record) else 1
    if record[0] == "#":
        return permutations(record[1:], [numbers[0]-1] + numbers[1:], history+"#")
    if record[0] == "?":
        return permutations(record[1:], [numbers[0]-1] + numbers[1:], history+"#") + permutations(record[1:], numbers, history+".")
    raise Exception("wtf")

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        for line in fin:
            line = line.strip()
            if line == "":
                continue
            record, numbers = line.split(" ")
            numbers = list(map(int, numbers.split(",")))
            new_perm = permutations(record, numbers)
            print(f"{record=}, {numbers=}, {new_perm=}" + "\n\n\n")
            s += new_perm
        fout.write(str(s))
