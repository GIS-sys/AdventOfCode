def is_digit(c):
    return c in "0123456789"

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        for line in fin:
            for c in line:
                if is_digit(c):
                    s += int(c) * 10
                    break
            for c in line[::-1]:
                if is_digit(c):
                    s += int(c)
                    break
        fout.write(str(s))
