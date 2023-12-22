"""
Advent of Code 2023
Day 21: Step Counter

Daniel Herding
"""

with open("21.txt") as f:
    input = f.read()

def createMap(sReplacement: str):
    map = []
    for line in input.split("\n"):
        row = list(line.replace("S", sReplacement))
        map.append(row)

    return map

def printMap(map):
    for row in map:
        for c in row:
            print(c, end="")
        print()
    print()
        
def walk(previousMap):
    map = createMap(sReplacement=".")
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == ".":
                if ((x > 0 and previousMap[y][x - 1] == "O")
                    or (y > 0 and previousMap[y - 1][x] == "O")
                    or (x < len(map[y]) - 1 and previousMap[y][x + 1] == "O")
                    or (y < len(map) - 1 and previousMap[y + 1][x] == "O")):
                    map[y][x] = "O"
    return map

def walkTimes(previousMap, steps):
    newMap = previousMap
    for _ in range(steps):
        newMap = walk(newMap)
    return newMap

def countOs(currentMap):
    result = 0
    for row in currentMap:
        result += row.count("O")
    return result

# Find start pos
part1StartMap = createMap(sReplacement="O")

height = len(part1StartMap)
width = len(part1StartMap[0])

for y, row in enumerate(part1StartMap):
    for x, c in enumerate(row):
        if c == "O":
            startY = y
            startX = x

part1FinishMap = walkTimes(part1StartMap, 64)
print(f"Part 1 result: {countOs(part1FinishMap)}")

fullMap = createMap(sReplacement="O")
fullMap = walkTimes(fullMap, width)
full = countOs(fullMap)

fullShiftedMap = createMap(sReplacement="O")
fullShiftedMap = walkTimes(fullShiftedMap, width + 1)
fullShifted = countOs(fullShiftedMap)

nMap = createMap(sReplacement=".")
nMap[height - 1][startX] = "O"
nMap = walkTimes(nMap, width - 1)
n = countOs(nMap)

eMap = createMap(sReplacement=".")
eMap[startY][0] = "O"
eMap = walkTimes(eMap, width - 1)
e = countOs(eMap)

sMap = createMap(sReplacement=".")
sMap[0][startX] = "O"
sMap = walkTimes(sMap, width - 1)
s = countOs(sMap)

wMap = createMap(sReplacement=".")
wMap[startY][width - 1] = "O"
wMap = walkTimes(wMap, width - 1)
w = countOs(wMap)

neMap = createMap(sReplacement=".")
neMap[height - 1][0] = "O"
neMap = walkTimes(neMap, width // 2 - 1)
ne = countOs(neMap)

seMap = createMap(sReplacement=".")
seMap[0][0] = "O"
seMap = walkTimes(seMap, width // 2 - 1)
se = countOs(seMap)

swMap = createMap(sReplacement=".")
swMap[0][width - 1] = "O"
swMap = walkTimes(swMap, width // 2 - 1)
sw = countOs(swMap)

nwMap = createMap(sReplacement=".")
nwMap[height - 1][width - 1] = "O"
nwMap = walkTimes(nwMap, width // 2 - 1)
nw = countOs(nwMap)

ne2Map = createMap(sReplacement=".")
ne2Map[height - 1][0] = "O"
ne2Map = walkTimes(ne2Map, width + width // 2 - 1)
ne2 = countOs(ne2Map)

se2Map = createMap(sReplacement=".")
se2Map[0][0] = "O"
se2Map = walkTimes(se2Map, width + width // 2 - 1)
se2 = countOs(se2Map)

nw2Map = createMap(sReplacement=".")
nw2Map[height - 1][width - 1] = "O"
nw2Map = walkTimes(nw2Map, width + width // 2 - 1)
nw2 = countOs(nw2Map)

sw2Map = createMap(sReplacement=".")
sw2Map[0][width - 1] = "O"
sw2Map = walkTimes(sw2Map, width + width // 2 - 1)
sw2 = countOs(sw2Map)

# printMap(nMap)
# printMap(fullShiftedMap)
# printMap(fullMap)
# printMap(fullShiftedMap)
# printMap(sMap)

# printMap(nwMap)
# printMap(wMap)
# printMap(swMap)

# printMap(neMap)
# printMap(eMap)
# printMap(seMap)

# printMap(se2Map)
# printMap(seMap)

# print(full, fullShifted)
# print(n, e, s, w)
# print(ne, se, sw, nw)
# print(ne2, se2, sw2, nw2)

PART_2_STEPS = 26501365
# PART_2_STEPS = width * 4 + 65

shiftedOnEquator = PART_2_STEPS // width

part2Result = nw + n + ne
for fullCount in range(1, shiftedOnEquator):
    part2Result += nw + nw2 + (fullCount-1)*full + fullCount*fullShifted + ne2 + ne
    #print(f"upper diagonals with {fullCount-1} full and {fullCount} shifted")
part2Result += w + (shiftedOnEquator-1)*full + shiftedOnEquator*fullShifted + e
#print(f"equator with {shiftedOnEquator-1} full and {shiftedOnEquator} shifted")
for fullCount in range(shiftedOnEquator - 1, 0, -1):
    part2Result += sw + sw2 + (fullCount-1)*full + fullCount*fullShifted + se2 + se
    #print(f"lower diagonals with {fullCount-1} full and {fullCount} shifted")
part2Result += sw + s + se

print(f"Part 2 result: {part2Result}")
