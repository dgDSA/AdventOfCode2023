"""
Advent of Code 2023
Day 13: Point of Incidence

Daniel Herding
"""

import re

def findSimilarLines(landscape, lineNumber):
    result = []
    line = landscape[lineNumber]
    for i, otherLine in enumerate(landscape):
        if i != lineNumber and line == otherLine:
            result.append(i)
    return result

def findHorizontalMirror(landscape, tabooLine):
    similarToFirst = findSimilarLines(landscape, 0)
    if similarToFirst:
        for similarIndex in similarToFirst:
            possibleMirror = similarIndex // 2 + 1
            if tabooLine != possibleMirror and landscape[:possibleMirror] == list(reversed(landscape[possibleMirror:possibleMirror * 2])):
                return possibleMirror

    lastIndex = len(landscape) - 1
    similarToLast = findSimilarLines(landscape, lastIndex)
    if similarToLast:
        for similarIndex in similarToLast:
            possibleMirror = similarIndex + (lastIndex - similarIndex) // 2 + 1
            if tabooLine != possibleMirror and landscape[similarIndex:possibleMirror] == list(reversed(landscape[possibleMirror:])):
                return possibleMirror

    return None

def flip(landscape):
    originalHeight  = len(landscape)
    originalWidth  = len(landscape[0])
    flipped = [[None for _ in range(originalHeight)] for _ in range(originalWidth)]
    for y, line in enumerate(landscape):
        for x, c in enumerate(line):
            flipped[x][y] = landscape[y][x]
    
    return flipped

def findMirrorPos(landscape, tabooResult=None):
    pos = findHorizontalMirror(landscape, None if tabooResult is None else tabooResult/100)
    if pos:
        return 100 * pos

    flippedLandscape = flip(landscape)
    pos = findHorizontalMirror(flippedLandscape, None if tabooResult is None else tabooResult)
    if pos:
        return pos

    return None


with open("13.txt") as f:
    input = f.read()

landscapes = input.split("\n\n")

def toggleSmudge(landscape, x, y):
    if landscape[y][x] == ".":
        landscape[y][x] = "#"
    else:
        landscape[y][x] = "."

def findDesmudgedMirrorPos(landscape, tabooResult):
    for y, line in enumerate(landscape):
        for x, c in enumerate(line):
            toggleSmudge(landscape, x, y)
            try:
                result = findMirrorPos(landscape, tabooResult)
            finally:
                toggleSmudge(landscape, x, y)
            if result:
                return result

part1Result = 0
part2Result = 0
for landscape in landscapes:
    lines = landscape.split("\n")
    landscape = [[c for c in line] for line in lines]

    mirrorPos = findMirrorPos(landscape)
    part1Result += mirrorPos

    desmudgedMirrorPos = findDesmudgedMirrorPos(landscape, mirrorPos)
    part2Result += desmudgedMirrorPos

print(f"Part 1: {part1Result}") # 34911
print(f"Part 2: {part2Result}")
