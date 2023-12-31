with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        for line in fin:
            if line.strip() == "":
                continue
            line = line[line.index(":")+2:]
            winning, my = line.split("|")
            winning = winning.strip().split(" ")
            my = my.strip().split(" ")
            winning = [x.strip() for x in winning if x.strip() != ""]
            my = [x.strip() for x in my if x.strip() != ""]
            cur = 0
            for x in winning:
                if x in my:
                    if cur == 0:
                        cur = 1
                    else:
                        cur *= 2
            s += cur
        fout.write(str(s))
