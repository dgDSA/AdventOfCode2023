"""
Advent of Code 2023
Day 22: Sand Slabs
Part 1

Daniel Herding
"""

import re
from collections import defaultdict
from copy import deepcopy

with open("22.txt") as f:
    input = f.read()

R_BLOCK = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self):
        return self.x * 2 + self.y * 3 # self.z is mutable
        
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

class Block:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.points = set()
        if self.point1.x == self.point2.x and self.point1.y == self.point2.y:
            self.isVertical = True
            for z in range(min(self.point1.z, self.point2.z), max(self.point1.z, self.point2.z) + 1):
                self.points.add(Point(self.point1.x, self.point1.y, z))
        elif self.point1.x == self.point2.x and self.point1.z == self.point2.z:
            self.isVertical = False
            for y in range(min(self.point1.y, self.point2.y), max(self.point1.y, self.point2.y) + 1):
                self.points.add(Point(self.point1.x, y, self.point1.z))
        else:
            assert self.point1.y == self.point2.y and self.point1.z == self.point2.z
            self.isVertical = False
            for x in range(min(self.point1.x, self.point2.x), max(self.point1.x, self.point2.x) + 1):
                self.points.add(Point(x, self.point1.y, self.point1.z))
            
    def __repr__(self):
        return f"{self.point1} -> {self.point2}"
    
    def isOnGround(self):
        return self.point1.z == 1 or self.point2.z == 1
    
    def canFall(self, pointsWithBlocks):
        if self.isOnGround():
            return False

        if self.isVertical:
            targetPoints = {Point(self.point1.x, self.point1.y, min(self.point1.z, self.point2.z) - 1)}
        else:
            targetPoints = {Point(p.x, p.y, p.z - 1) for p in self.points}
        return not any(p in pointsWithBlocks for p in targetPoints)
    
    def intersects(self, other):
        return any(p in other.points for p in self.points)
        
    def moveDown(self):
        self.point1.z -= 1
        self.point2.z -= 1
        for p in self.points:
            p.z -= 1

    def moveUp(self):
        self.point1.z += 1
        self.point2.z += 1
        for p in self.points:
            p.z += 1

blocks = []

for m in R_BLOCK.finditer(input):
    x1, y1, z1, x2, y2, z2 = m.groups()
    block = Block(Point(int(x1), int(y1), int(z1)), Point(int(x2), int(y2), int(z2)))
    blocks.append(block)

for i, block in enumerate(blocks):
    print(i, block)

falling = True
iterations = 0
while falling:
    falling = False
    
    pointsWithBlocks = set.union(*[b.points for b in blocks])
    for i, block in enumerate(blocks):
        if block.canFall(pointsWithBlocks):
            pointsWithBlocks -= block.points
            block.moveDown()
            pointsWithBlocks |= block.points
            # print(f"Block {i} is falling.")
            falling = True
    iterations += 1
    print(f"{iterations} iterations")

# Preparation for part 2
with open("22b.txt", "w") as f:
    f.write("\n".join(f"{b.point1.x},{b.point1.y},{b.point1.z}~{b.point2.x},{b.point2.y},{b.point2.z}" for b in blocks))

supportedBy = defaultdict(list)
for i, block in enumerate(blocks):
    block.moveDown()
    for j, other in enumerate(blocks):
        if i != j and block.intersects(other):
            # print(f"Block {i} {block} is supported by block {j} {other}.")
            supportedBy[i].append(other)
    block.moveUp()


part1Result = 0

for i, block in enumerate(blocks):
    isSoleSupport = False
    for v in supportedBy.values():
        if len(v) == 1 and v[0] == block:
            isSoleSupport = True
    if not isSoleSupport:
        part1Result += 1

print(f"Part 1 result: {part1Result}")
