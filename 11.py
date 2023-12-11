"""
Advent of Code 2023
Day 11: Cosmic Expansion

Daniel Herding
"""

with open("11.txt") as f:
    input = f.read()

lines = input.split("\n")

expandedRows = []
for r, line in enumerate(lines):
    if all(x == "." for x in line):
        expandedRows.append(r)

expandedCols = []
for c in range(len(lines[0])):
    if all(l[c] == "." for l in lines):
        expandedCols.append(c)

# for line in lines:
    # print(line)
    
stars = []
pairs = []

for r, line in enumerate(lines):
    for c, x in enumerate(line):
        if x == "#":
            star = (c, r)
            for otherStar in stars:
                pairs.append((otherStar, star))
            stars.append(star)

def distance(expansion: int) -> int:
    dists = 0
    for s1, s2  in pairs:
        distX = abs(s1[0] - s2[0])
        for i in expandedCols:
            if min(s1[0], s2[0]) < i < max(s1[0], s2[0]):
                distX += expansion
        distY = abs(s1[1] - s2[1])
        for i in expandedRows:
            if min(s1[1], s2[1]) < i < max(s1[1], s2[1]):
                distY += expansion
        #print(otherStar, star, distX + distY)
        dists += distX + distY
    return dists
    
print(f"Part 1: {distance(1)}")
print(f"Part 2: {distance(1000000 - 1)}")

