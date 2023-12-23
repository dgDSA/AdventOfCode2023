"""
Advent of Code 2023
Day 23: A Long Walk
Part 1

Daniel Herding
"""
from collections import defaultdict, deque

with open("23.txt") as f:
    input = f.read()

lines = input.split("\n")
height = len(lines)
width = len(lines[0])
start = (1, 0)
finish = (width - 2, height - 1)

UP_SLOPES = {
    (0, -1): "v",
    (1, 0): "<",
    (0, 1): "^",
    (-1, 0): ">",
}

possibleMoves = defaultdict(list)

for y, line in enumerate(lines):
    for x, tile in enumerate(line):
        if tile != "#":
            for diff, forbiddenSlope in UP_SLOPES.items():
                nextY = y + diff[1]
                nextX = x + diff[0]
                if nextY > 0 and nextY < height and nextX > 0 and nextX < width:
                    nextTile = lines[nextY][nextX]
                    if nextTile not in (forbiddenSlope, "#"):
                        possibleMoves[(x, y)].append((nextX, nextY))


queue = deque()
queue.append((start, set(), 0))
part1Result = 0

while queue:
    pos, seenNodes, steps = queue.pop()
    if pos == finish:
        part1Result = max(part1Result, steps)

    nextPositions = [next for next in possibleMoves[pos] if next not in seenNodes]
    if nextPositions:
        seenNodesCopy = seenNodes.copy()
        seenNodesCopy.add(pos)

        for next in nextPositions:
            queue.append((next, seenNodesCopy, 1 + steps))

print(f"Part 1 result: {part1Result}")
