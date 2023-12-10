from functools import cmp_to_key

class Hand:
    def __init__(self, line):
        self.raw, bid = line.split(" ")
        self.bid = int(bid)

    def type(self):
        vals = {}
        for letter in self.raw:
            vals[letter] = vals.get(letter, 0) + 1
        amounts = sorted(list(vals.values()))
        if amounts[-1] == 5:
            return -1
        if amounts[-1] == 4:
            return -2
        if amounts[-1] == 3 and amounts[-2] == 2:
            return -3
        if amounts[-1] == 3:
            return -4
        if amounts[-1] == 2 and amounts[-2] == 2:
            return -5
        if amounts[-1] == 2:
            return -6
        return -7

    def abs(self):
        cards = "23456789TJQKA"
        score = 0
        for letter in self.raw:
            score = score * 100 + cards.index(letter)
        return score

    MAX_ABS = 10**30

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        hands = []
        for line in fin:
            if line.strip() == "":
                continue
            hands.append(Hand(line))
        hands.sort(key=lambda x: x.abs() + x.type() * Hand.MAX_ABS)
        for i, hand in enumerate(hands):
            # print(hand.bid, hand.abs(), hand.type(), hand.raw)
            s += hand.bid * (i + 1)
        fout.write(str(s))
