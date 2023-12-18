"""
Advent of Code 2023
Day 18: Lavaduct Lagoon
Part 2

Daniel Herding
"""

import re
from shapely import Polygon

with open("18.txt") as f:
    input = f.read()
    
R_HEX = re.compile(r"#(.....)(.)")

points = [(0, 0)]
for mHex in R_HEX.finditer(input):
    prev = points[-1]
    distanceHex, dir = mHex.groups()
    dist = int(distanceHex, 16)
    print(mHex.group(), dir, distanceHex)
    match dir:
        case "0": # R
            points.append((prev[0] + dist, prev[1]))
        case "1": # D
            points.append((prev[0], prev[1] + dist))
        case "2": # L
            points.append((prev[0] - dist, prev[1]))
        case "3": # U
            points.append((prev[0], prev[1] - dist))

poly = Polygon(points)
buffer = poly.buffer(distance=0.5, join_style="mitre")          
part1Result = buffer.area

print(f"Part 2 result: {part1Result}")
