with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        copies = {0: 1}
        s = 0
        for i, line in enumerate(fin):
            #print(i, copies, s)
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
                    cur += 1
            for j in range(1, cur+1):
                copies[i + j] = copies.get(i + j, 1) + copies.get(i, 1)
            s += cur * copies.get(i, 1)
        s += i + 1
        fout.write(str(s))
