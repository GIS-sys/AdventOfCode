def totalLength(arrOfPairs):
    s = 0
    for x, y in arrOfPairs:
        s += y - x + 1
    return s

class SeedMap:
    def __init__(self, name):
        self.ranges = []

    def addRange(self, dest, sour, rang):
        self.ranges.append((sour, dest, rang))

    def goRanges(self, seed_ranges):
        self.ranges.sort()
        new_seed_ranges = []
        for ls, rs in seed_ranges:
            new_seed_ranges_inloop = []
            for sour, dest, rang in self.ranges:
                lrange, rrange = sour, sour + rang - 1
                bias = dest - lrange
                # if [ls, rs] and [lrange, rrange] intersect
                if rs > lrange and rrange > ls:
                    if lrange <= ls and rrange >= rs:
                        new_seed_ranges_inloop.append([ls+bias, rs+bias])
                        ls, rs = 0, -1
                    elif lrange <= ls and rrange < rs:
                        new_seed_ranges_inloop.append([ls+bias, rrange+bias])
                        ls, rs = rrange+1, rs
                    elif lrange > ls and rrange < rs:
                        new_seed_ranges_inloop.append([ls, lrange-1])
                        new_seed_ranges_inloop.append([lrange+bias, rrange+bias])
                        ls, rs = rrange+1, rs
                    elif lrange > ls and rrange >= rs:
                        new_seed_ranges_inloop.append([ls, lrange-1])
                        new_seed_ranges_inloop.append([lrange+bias, rs+bias])
                        ls, rs = 0, -1
                    else:
                        print(ls, rs, lrange, rrange)
                        raise Exception("Unexpected intersection pattern")
                if ls > rs:
                    break
            if ls <= rs:
                new_seed_ranges_inloop.append([ls, rs])
            new_seed_ranges += new_seed_ranges_inloop
        # print(seed_ranges, new_seed_ranges)
        assert totalLength(seed_ranges) == totalLength(new_seed_ranges)
        return new_seed_ranges

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        data = fin.read().split("\n\n")
        raw_seeds = list(map(int, data[0][len("Seeds: "):].split(" ")))
        seed_ranges = []
        for i in range(0, len(raw_seeds), 2):
            seed_ranges += [[raw_seeds[i], raw_seeds[i] + raw_seeds[i+1]]]
        maps = []
        for mapData in data[1:]:
            mapData = mapData.split("\n")
            maps.append(SeedMap(mapData[0]))
            for line in mapData[1:]:
                if line.strip() == "":
                    break
                dest, sour, rang = map(int, line.split(" "))
                maps[-1].addRange(dest, sour, rang)
        for mapObject in maps:
            seed_ranges = mapObject.goRanges(seed_ranges)
        s = min([seed_range[0] for seed_range in seed_ranges])
        fout.write(str(s))
