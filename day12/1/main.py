from functools import cmp_to_key
import numpy as np


def permutations(record, numbers, history=""):
    # remove all leading "."
    #   if we were on a streak - return 0, cant break continuity
    while len(record) != 0 and record[0] == ".":
        if numbers[0] != 0:
            return 0
        record = record[1:]
        history = history + "."
    # debug
    print(f"perm {record=}, {numbers=}, {history=}")
    # exit conditions:
    #   if no more records, exit, checking if no more numbers
    #   if no more numbers, exit, checking if all other records are not mandatory
    if len(record) == 0:
        if len(numbers) == 0 or numbers == [0]:
            print(history)
        return 1 if len(numbers) == 0 or numbers == [0] else 0
    if len(numbers) == 0 or numbers == [0]:
        if not ("#" in record):
            print(history + "." * len(record))
        return 1 if not ("#" in record) else 0
    # recursion
    #   if not on a streak
    #     if # then we begin streak
    #     if ? then either skip or begin streak
    #   if on a streak, next one is mandatory #
    if numbers[0] == 0:
        if record[0] == "#":
            return permutations(record[1:], [numbers[1]-1] + numbers[2:], history+"#")
        elif record[0] == "?":
            return permutations(record[1:], [numbers[1]-1] + numbers[2:], history+"#") + permutations(record[1:], numbers, history+".")
        else:
            raise Exception("wtf")
    else:
        return permutations(record[1:], [numbers[0]-1] + numbers[1:], history+"#")
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
            new_perm = permutations(record, [0] + numbers)
            print(f"{record=}, {numbers=}, {new_perm=}" + "\n\n\n")
            s += new_perm
        fout.write(str(s))
