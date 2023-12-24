from collections import deque

class Segment:
    def __init__(self, fr, to, color):
        self.fr = fr
        self.to = to
        self.color = color

    def x(self):
        return self.to[0] - self.fr[0]

    def y(self):
        return self.to[1] - self.fr[1]

class Line:
    def __init__(self):
        self.segments = []
        self.lastPoint = [0, 0]

    def move(self, delta, color):
        self.newPoint = [self.lastPoint[0] + delta[0], self.lastPoint[1] + delta[1]]
        self.segments.append(Segment(self.lastPoint, self.newPoint, color))
        self.lastPoint = self.newPoint

    def area(self):
        s = 0
        for segment in self.segments:
            s += (segment.fr[0] - segment.to[0]) * (segment.fr[1] + segment.to[1]) / 2
        return s

    def additionalArea(self):
        corners = 0
        lines = 0
        for segment1, segment2 in zip(self.segments, self.segments[1:] + [self.segments[0]]):
            lines += abs(segment1.x() + segment1.y())
            if segment1.x() * segment2.x() + segment1.y() * segment2.y() == 0:
                corners += 1
        return lines / 2 + 1 #(corners - 2) / 4

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 0
        line = Line()
        for row in fin:
            row = row.strip()
            if row == "":
                break
            direction, distance, color = row.split(" ")
            distance = int(distance)
            if direction == "R":
                line.move([distance, 0], color)
            if direction == "D":
                line.move([0, distance], color)
            if direction == "L":
                line.move([-distance, 0], color)
            if direction == "U":
                line.move([0, -distance], color)
        s = line.area() + line.additionalArea()
        fout.write(str(s))

