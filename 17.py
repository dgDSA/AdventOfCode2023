"""
Advent of Code 2023
Day 17: Clumsy Crucible
Part 1

Daniel Herding
"""

from collections import defaultdict
from enum import Enum
import sys

sys.setrecursionlimit(10000)

with open("17.txt") as f:
    input = f.read()

class Dir(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

city = []
for line in input.split("\n"):
    city.append([int(c) for c in line])

height = len(city)
width = len(city[0])

shortestPath = width * height * 10

def maxint():
    return width * height * 10

minDistances = defaultdict(maxint)

def search(x, y, heatLoss, dir, straightsCount):
    if straightsCount >= 3:
        return

    global minDistances

    heatLoss += city[y][x]
    
    for sc in range(0, straightsCount + 1):
        if heatLoss >= minDistances[(x, y, sc, dir)]:
            return
    
    minDistances[(x, y, straightsCount, dir)] = heatLoss
    
    global shortestPath

    if x == width - 1 and y == height - 1:
        shortestPath = min(shortestPath, heatLoss)
        print(">>>>>>>", shortestPath)
    elif heatLoss < shortestPath:
        # Move South
        if y < height - 1 and dir != Dir.NORTH:
            search(x, y + 1, heatLoss, Dir.SOUTH, straightsCount + 1 if dir == Dir.SOUTH else 0)

        # Move East
        if x < width - 1 and dir != Dir.WEST:
            search(x + 1, y, heatLoss, Dir.EAST, straightsCount + 1 if dir == Dir.EAST else 0)

        # Move North
        if y > 0 and dir != Dir.SOUTH:
            search(x, y - 1, heatLoss, Dir.NORTH, straightsCount + 1 if dir == Dir.NORTH else 0)
    
        # Move West
        if x > 0 and dir != Dir.EAST:
            search(x - 1, y, heatLoss, Dir.WEST, straightsCount + 1 if dir == Dir.WEST else 0)

search(0, 0, -city[0][0], None, 0)
print(f"Part 1 solution: {shortestPath}")
