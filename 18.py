"""
Advent of Code 2023
Day 18: Lavaduct Lagoon
Part 1

Daniel Herding
"""

import re

R_WALL = re.compile("(?<!%)#+(?!%)")

with open("18.txt") as f:
    input = f.read()
WIDTH = 650

trenches = []
for line in input.split("\n"):
    dir, distance, color = line.split(" ")
    trenches.append((dir, int(distance), color))

landscape = [["." for x in range(WIDTH)] for y in range(WIDTH)]
currentX = WIDTH // 2
currentY = WIDTH // 2

for i, (dir, distance, _) in enumerate(trenches):
    if dir == "R":
        isBend = trenches[i - 1][0] != trenches[i + 1][0]
        for x in range(currentX, currentX + distance):
            landscape[currentY][x] = "%" if isBend else "#"
        currentX = currentX + distance
    elif dir == "D":
        for y in range(currentY, currentY + distance):
            landscape[y][currentX] = "#"
        currentY = currentY + distance
    elif dir == "L":
        isBend = trenches[i - 1][0] != trenches[i + 1][0]
        for x in range(currentX, currentX - distance - 1, -1):
            landscape[currentY][x] = "%" if isBend else "#"
        currentX = currentX - distance    
    elif dir == "U":
        for y in range(currentY, currentY - distance - 1, -1):
            landscape[y][currentX] = "#"
        currentY = currentY - distance

for row in landscape:
    for x, c in enumerate(row):
        rowStr = "".join(row)
        if c == "." and len(R_WALL.findall(rowStr[:x])) % 2 == 1 and "#" in rowStr[x:]:
            row[x] = "*"
    
# for row in landscape:
    # for c in row:
        # print(c, end="")
    # print()

part1Result = 0
for row in landscape:
    for c in row:
        if c in ("#", "%", "*"):
            part1Result += 1

print(f"Part 1 result: {part1Result}")
