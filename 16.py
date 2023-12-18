"""
Advent of Code 2023
Day 16: The Floor Will Be Lava

Daniel Herding
"""
from collections import defaultdict
from enum import Enum
import sys

sys.setrecursionlimit(10000)

class Dir(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

with open("16.txt") as f:
    input = f.read()

lines = input.split("\n")
height = len(lines)
width = len(lines[0])

class Energizer:
    def __init__(self):
        # Maps coordinates to incoming beam directions.
        self.visited = defaultdict(set)

    def _forward(self, x, y, dir):
        match(dir):
            case Dir.NORTH:
                newX = x
                newY = y - 1
            case Dir.EAST:
                newX = x + 1
                newY = y
            case Dir.SOUTH:
                newX = x
                newY = y + 1
            case Dir.WEST:
                newX = x - 1
                newY = y
        if 0 <= newX < width and 0 <= newY < height:
            self.follow(newX, newY, dir)

    def _turnLeft(self, x, y, dir):
        match(dir):
            case Dir.NORTH:
                newX = x - 1
                newY = y
                newDir = Dir.WEST
            case Dir.EAST:
                newX = x
                newY = y - 1
                newDir = Dir.NORTH
            case Dir.SOUTH:
                newX = x + 1
                newY = y
                newDir = Dir.EAST
            case Dir.WEST:
                newX = x
                newY = y + 1
                newDir = Dir.SOUTH
        if 0 <= newX < width and 0 <= newY < height:
            self.follow(newX, newY, newDir)

    def _turnRight(self, x, y, dir):
        match(dir):
            case Dir.NORTH:
                newX = x + 1
                newY = y
                newDir = Dir.EAST
            case Dir.EAST:
                newX = x
                newY = y + 1
                newDir = Dir.SOUTH
            case Dir.SOUTH:
                newX = x - 1
                newY = y
                newDir = Dir.WEST
            case Dir.WEST:
                newX = x
                newY = y - 1
                newDir = Dir.NORTH
        if 0 <= newX < width and 0 <= newY < height:
            self.follow(newX, newY, newDir)
            
    def _splitVertical(self, x, y, dir):
        match(dir):
            case Dir.NORTH | Dir.SOUTH:
                self._forward(x, y, dir)
            case Dir.EAST | Dir.WEST:
                self._turnLeft(x, y, dir)
                self._turnRight(x, y, dir)

    def _splitHorizontal(self, x, y, dir):
        match(dir):
            case Dir.WEST | Dir.EAST:
                self._forward(x, y, dir)
            case Dir.NORTH | Dir.SOUTH:
                self._turnLeft(x, y, dir)
                self._turnRight(x, y, dir)

    def _reflectBackslash(self, x, y, dir):
        match(dir):
            case Dir.NORTH | Dir.SOUTH:
                self._turnLeft(x, y, dir)
            case Dir.WEST | Dir.EAST:
                self._turnRight(x, y, dir)

    def _reflectSlash(self, x, y, dir):
        match(dir):
            case Dir.NORTH | Dir.SOUTH:
                self._turnRight(x, y, dir)
            case Dir.WEST | Dir.EAST:
                self._turnLeft(x, y, dir)

    def follow(self, x, y, dir):
        assert dir in (Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST)
        dirsVisitedHere = self.visited[x, y]
        if dir in dirsVisitedHere:
            return
        
        dirsVisitedHere.add(dir)
        currentTile = lines[y][x]
        if currentTile == ".":
            self._forward(x, y, dir)
        elif currentTile == "\\":
            self._reflectBackslash(x, y, dir)
        elif currentTile == "/":
            self._reflectSlash(x, y, dir)
        elif currentTile == "|":
            self._splitVertical(x, y, dir)
        elif currentTile == "-":
            self._splitHorizontal(x, y, dir)
        else:
            assert False
            
    # def showMaze(self, curX, curY, curDir):
        # for y in range(height):
            # for x in range(width):
                # if x == curX and y == curY:
                    # match(curDir):
                        # case Dir.NORTH:
                            # print("^", end="")
                        # case Dir.EAST:
                            # print(">", end="")
                        # case Dir.SOUTH:
                            # print("v", end="")
                        # case Dir.WEST:
                            # print("<", end="")
                        # case _:
                            # assert False
                # elif visited[x, y]:
                    # print("#", end="")
                # else:
                    # print(".", end="")
            # print()
        # print()

    def calcEnergy(self, x, y, dir):
        energyLevel = 0
        self.follow(x, y, dir)
        for position, dirs in self.visited.items():
            if len(dirs) > 0:
                energyLevel += 1
        return energyLevel

part1Result = Energizer().calcEnergy(0, 0, Dir.EAST)
print(f"Part 1: {part1Result}")


part2Result = 0
for y in range(height):
    part2Result = max(part2Result, Energizer().calcEnergy(0, y, Dir.EAST))
    part2Result = max(part2Result, Energizer().calcEnergy(width - 1, y, Dir.WEST))
for x in range(width):
    part2Result = max(part2Result, Energizer().calcEnergy(x, 0, Dir.SOUTH))
    part2Result = max(part2Result, Energizer().calcEnergy(x, height - 1, Dir.NORTH))
print(f"Part 2: {part2Result}")
