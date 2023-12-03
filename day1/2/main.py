def to_digit(text):
    if text[0] in "0123456789":
        return True, int(text[0])
    digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for i, digit in enumerate(digits):
        if text.startswith(digit):
            return True, i
    return False, None

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        for line in fin:
            for i in range(len(line)):
                is_digit, val = to_digit(line[i:])
                if is_digit:
                    s += val * 10
                    break
            for i in range(len(line))[::-1]:
                is_digit, val = to_digit(line[i:])
                if is_digit:
                    s += val
                    break
        fout.write(str(s))
