import math

with open("output.txt", "w") as fout:
    with open("input.txt", "r") as fin:
        s = 1
        times = [int(fin.readline()[len("Time:"):].replace(" ", ""))]
        dists = [int(fin.readline()[len("Distance:"):].replace(" ", ""))]
        for t, d in zip(times, dists):
            # x * (t - x) > d
            # x^2 - tx + d < 0
            # D=t^2-4d
            # x = (+-sqr(D)+t)/2
            D = math.sqrt(t*t-4*d)
            x1 = math.ceil((t - D) / 2)
            x2 = math.floor((t + D) / 2)
            s *= (x2 - x1 + 1)
        fout.write(str(s))
