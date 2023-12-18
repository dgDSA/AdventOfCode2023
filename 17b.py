"""
Advent of Code 2023
Day 17: Clumsy Crucible
Part 2

Daniel Herding
"""

from collections import defaultdict
from enum import Enum
import sys

sys.setrecursionlimit(100000)

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

shortestPath = width * height * 100

def maxint():
    return width * height * 100

minDistances = defaultdict(maxint)

def search(x, y, heatLoss, dir, straightsCount):
    global minDistances

    heatLoss += city[y][x]
    
    if heatLoss >= minDistances[(x, y, straightsCount, dir)]:
        return
    
    minDistances[(x, y, straightsCount, dir)] = heatLoss
    
    global shortestPath

    if x == width - 1 and y == height - 1 and straightsCount >= 3:
        shortestPath = min(shortestPath, heatLoss)
        print(">>>>>>>", shortestPath)
    elif heatLoss < shortestPath - 1:
        # Move East
        if x < width - 1:
            if straightsCount + 1 < 10 and dir in (Dir.EAST, None):
                search(x + 1, y, heatLoss, Dir.EAST, straightsCount + 1)
            if straightsCount >= 3 and dir in (Dir.NORTH, Dir.SOUTH):
                search(x + 1, y, heatLoss, Dir.EAST, 0)

        # Move South
        if y < height - 1:
            if straightsCount + 1 < 10 and dir in (Dir.SOUTH, None):
                search(x, y + 1, heatLoss, Dir.SOUTH, straightsCount + 1)
            if straightsCount >= 3 and dir in (Dir.EAST, Dir.WEST):
                search(x, y + 1, heatLoss, Dir.SOUTH, 0)

        # Move North
        if y > 0:
            if straightsCount + 1 < 10 and dir in (Dir.NORTH, None):
                search(x, y - 1, heatLoss, Dir.NORTH, straightsCount + 1)
            if straightsCount >= 3 and dir in (Dir.EAST, Dir.WEST):
                search(x, y - 1, heatLoss, Dir.NORTH, 0)
    
        # Move West
        if x > 0:
            if straightsCount + 1 < 10 and dir in (Dir.WEST, None):
                search(x - 1, y, heatLoss, Dir.WEST, straightsCount + 1)
            if straightsCount >= 3 and dir in (Dir.NORTH, Dir.SOUTH):
                search(x - 1, y, heatLoss, Dir.WEST, 0)


search(0, 0, -city[0][0], None, 0)
print(f"Part 2 solution: {shortestPath}")
