def parse_subset(raw):
    objects = [s.strip() for s in raw.split(",")]
    subset = {}
    for obj in objects:
        val, color = obj.split(" ")
        subset[color] = int(val)
    return subset

class Game:
    def __init__(self, raw):
        raw = raw[len("Game "):]
        self.id = int(raw[:raw.index(":")])
        raw = raw[raw.index(":") + len(": "):]
        self.subsets = [parse_subset(s) for s in raw.split(";")]

    def max(self, name):
        return max([subset.get(name, 0) for subset in self.subsets])

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        games = []
        for line in fin:
            if line.strip() == "":
                break
            games.append(Game(line))
        s = 0
        for game in games:
            s += game.max("red") * game.max("green") * game.max("blue")
        fout.write(str(s))
