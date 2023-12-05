class SeedMap:
    def __init__(self, name):
        self.ranges = []

    def addRange(self, dest, sour, rang):
        self.ranges.append((dest, sour, rang))

    def go(self, seeds):
        new_seeds = []
        for seed in seeds:
            new_seed = seed
            for dest, sour, rang in self.ranges:
                if sour <= seed < sour + rang:
                    new_seed = dest + (seed - sour)
                    break
            new_seeds.append(new_seed)
        return new_seeds

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        data = fin.read().split("\n\n")
        seeds = map(int, data[0][len("Seeds: "):].split(" "))
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
            seeds = mapObject.go(seeds)
        s = min(seeds)
        fout.write(str(s))
