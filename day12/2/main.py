from functools import cmp_to_key
import numpy as np

DEBUG = False

def withHistory(history, condition):
    if DEBUG and condition:
        print(history)
    return 1 if condition else 0

def withUsed(cur, val):
    global USED
    USED[cur] = val
    return val

USED = dict()

# record:  . empty, # mandatory, ? joker
# numbers: [x, ...], x: >0 streak, =0 just ended streak, -1 any
def permutations(record, numbers, history=""):
    cur = (tuple(record), tuple(numbers))
    if cur in USED:
        return USED[cur]
    # if we were just on a streak - check that end or next is free
    if len(numbers) > 0 and numbers[0] == 0:
        if len(record) == 0:
            return withUsed(cur, withHistory(history, numbers == [0]))
        if record[0] == "#":
            return withUsed(cur, 0)
        record = record[1:]
        history += "."
        numbers[0] = -1
    # remove all leading "."
    #   if we are on a streak - return 0, cant break continuity
    while len(record) != 0 and record[0] == ".":
        if numbers[0] != -1:
            return withUsed(cur, 0)
        record = record[1:]
        history = history + "."
    # debug
    if DEBUG:
        print(f"perm {record=}, {numbers=}, {history=}")
    # exit conditions:
    #   if no more records, exit, checking if no more numbers
    #   if no more numbers, exit, checking if all other records are not mandatory
    if len(record) == 0:
        return withUsed(cur, withHistory(history, len(numbers) == 0 or numbers == [-1]))
    if len(numbers) == 0 or numbers == [-1]:
        return withUsed(cur, withHistory(history, not ("#" in record)))
    # recursion
    #   if not on a streak
    #     if # then we begin streak
    #     if ? then either skip or begin streak
    #   if on a streak, next one is mandatory #
    if numbers[0] == -1:
        if record[0] == "#":
            return withUsed(cur, permutations(record[1:], [numbers[1]-1] + numbers[2:], history+"#"))
        elif record[0] == "?":
            return withUsed(cur, permutations(record[1:], [numbers[1]-1] + numbers[2:], history+"#") + permutations(record[1:], numbers, history+"."))
        else:
            raise Exception("wtf")
    else:
        return withUsed(cur, permutations(record[1:], [numbers[0]-1] + numbers[1:], history+"#"))
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
            record = '?'.join([record for _ in range(5)])
            numbers = numbers * 5
            USED = dict()
            new_perm = permutations(record, [-1] + numbers)
            if DEBUG:
                print(f"{record=}, {numbers=}, {new_perm=}" + "\n\n\n")
            s += new_perm
        fout.write(str(s))
