"""
Advent of Code 2023
Day 12: Hot Springs

Daniel Herding
"""
import re
from functools import lru_cache

# Matches a group of one or more machines that work.
R_WORKING = re.compile(r"\.+")

with open("12.txt") as f:
    input = f.read()

@lru_cache
def getRePossiblyBroken(i):
    """
    Returns a pattern which matches a group of one or more machines which has exactly the given length.
    Uses an LRU cache so that we don't recompile the same patterns again and again
    """
    return re.compile(r"[\#\?]{%i}(\.|\?|$)" % i)

@lru_cache
def findArrangements(row: str, damagedList: tuple) -> int:
    """
    Uses an LRU cache so that we don't recalculate identical situations again and again

    Despite its name, damagedList is actually not a list, but a tuple, as lists are not hashable and thus cannot go in an LRU cache.
    """
    if not row:
        if damagedList:
            # Fail: reached end of row
            return 0
        # Arrangement found
        return 1

    if not damagedList:
        if "#" in row:
            # Fail: Leftover hashes
            return 0
        # Arrangement found; assume the remaining machines all work.
        return 1

    mWorking = R_WORKING.match(row)
    if mWorking:
        return findArrangements(row[len(mWorking.group()) :], damagedList)

    arrangements = 0
    if row[0] == "?":
        # Assume this machine works.
        arrangements += findArrangements(row[1:], damagedList)

    currentDamaged = damagedList[0]
    mPossiblyBroken = getRePossiblyBroken(currentDamaged).match(row)
    if mPossiblyBroken:
        damagedRest = damagedList[1:]
        # Assume all machines in this range are broken.
        arrangements += findArrangements(
            row[len(mPossiblyBroken.group()) :], damagedRest
        )

    return arrangements


resultPart1 = 0

for line in input.split("\n"):
    row, damagedStr = line.split(" ")
    damaged = tuple([int(d) for d in damagedStr.split(",")])
    arrangements = findArrangements(row, damaged)
    # print(f"{line} -> {arrangements}")
    resultPart1 += arrangements

print(f"Part 1: {resultPart1}")

resultPart2 = 0

for i, line in enumerate(input.split("\n")):
    row, damagedStr = line.split(" ")
    row = "?".join([row for _ in range(5)])
    damagedStr = ",".join([damagedStr for _ in range(5)])
    damaged = tuple([int(d) for d in damagedStr.split(",")])
    arrangements = findArrangements(row, damaged)
    # print(f"{line} -> {arrangements}")
    resultPart2 += arrangements

print(f"Part 2: {resultPart2}")
