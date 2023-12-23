"""
Advent of Code 2023
Day 23: A Long Walk
Part 2

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

DIFFS = [
    (0, -1),
    (-1, 0),
    (0, 1),
    (1, 0),
]

possibleMoves = {}

for y, line in enumerate(lines):
    for x, tile in enumerate(line):
        if tile != "#":
            possibleMoves[(x, y)] = set()
            for diff in DIFFS:
                nextY = y + diff[1]
                nextX = x + diff[0]
                if nextY > 0 and nextY < height and nextX > 0 and nextX < width:
                    nextTile = lines[nextY][nextX]
                    if nextTile != "#":
                        possibleMoves[(x, y)].add((nextX, nextY))

junctions = {start, finish}
for y in range(1, height - 1):
    for x in range(1, width - 1):
        if lines[y][x] != "#":
            neighbors = 0
            for diff in DIFFS:
                nextY = y + diff[1]
                nextX = x + diff[0]
                if lines[nextY][nextX] != "#":
                    neighbors += 1
            if neighbors >= 3:
                junctions.add((x, y))

junctionConnections = defaultdict(list)
junctionQueue = deque()
for junction in junctions:
    junctionQueue.append((junction, junction, set(), 0))

while junctionQueue:
    fromJunction, pos, seenNodes, steps = junctionQueue.pop()
    steps += 1
    nextPositions = [next for next in possibleMoves[pos] if next not in seenNodes]
    if nextPositions:
        seenNodesCopy = seenNodes.copy()
        seenNodesCopy.add(pos)

        for next in nextPositions:
            if next in junctions:
                junctionConnections[fromJunction].append((next, steps))
            else:
                junctionQueue.appendleft((fromJunction, next, seenNodesCopy, steps))

queue = deque()
queue.append((start, [], 0))
part2Result = 0

while queue:
    pos, seenJunctions, steps = queue.pop()
    if pos == finish:
        if steps > part2Result:
            print(f"Found path with length {steps}: {seenJunctions}")
            part2Result = steps
    else:
        seenJunctionsCopy = seenJunctions.copy()
        seenJunctionsCopy.append(pos)
        for (next, dist) in junctionConnections[pos]:
            if next not in seenJunctions:
                queue.appendleft((next, seenJunctionsCopy, dist + steps))

print(f"Part 2 result: {part2Result}")
