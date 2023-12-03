class Number:
    def __init__(self, val, right, top):
        self.val = val
        self.length = len(str(self.val))
        self.x = right - self.length
        self.y = top

    def adjacent_cells(self):
        return ([(i, self.y-1) for i in range(self.x-1, self.x + self.length + 1)] +
                [(self.x + self.length, self.y)] +
                [(i, self.y+1) for i in range(self.x + self.length, self.x - 2, -1)] +
                [(self.x-1, self.y)])

class Board:
    def __init__(self, raw):
        self.board = []
        self.numbers = []
        for i, line in enumerate(raw.split("\n")):
            if line.strip() == "":
                continue
            self.board.append(line)
            line += "."
            cur_number = 0
            for j, c in enumerate(line):
                if c in "1234567890":
                    cur_number = cur_number * 10 + int(c)
                else:
                    if cur_number != 0:
                        self.numbers.append(Number(cur_number, j, i))
                    cur_number = 0

    def get(self, pos):
        x, y = pos
        if y >= len(self.board) or y < 0:
            return "."
        line = self.board[y]
        if x >= len(line) or x < 0:
            return "."
        return line[x]

    def gears(self):
        gears = []
        for i, line in enumerate(self.board):
            for j, c in enumerate(line):
                if c == "*":
                    gears.append((j, i))
        return gears

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        board = Board(fin.read())
        gears = board.gears()
        gear_numbers = {}
        for gear in gears:
            x, y = gear
            if not x in gear_numbers:
                gear_numbers[x] = {}
            if not y in gear_numbers[x]:
                gear_numbers[x][y] = {}
            gear_numbers[x][y] = (0, 1)
        for number in board.numbers:
            cells = number.adjacent_cells()
            for cell in cells:
                if board.get(cell) == "*":
                    x, y = cell
                    gear_amount, gear_score = gear_numbers[x][y]
                    gear_numbers[x][y] = (gear_amount+1, gear_score*number.val)
        for x in gear_numbers.values():
            for y in x.values():
                if y[0] == 2:
                    s += y[1]
        fout.write(str(s))
