"""
Advent of Code 2023
Day 15: Lens Library

Daniel Herding
"""
from collections import defaultdict

with open("15.txt") as f:
    input = f.read()

def calcHash(step):
    stepHash = 0
    for c in step:
        stepHash += ord(c)
        stepHash *= 17
        stepHash = stepHash % 256
    return stepHash

part1Result = 0
for step in input.split(","):
    part1Result += calcHash(step)
print(f"Part 1: {part1Result}")

boxes = defaultdict(list)
    
for step in input.split(","):
    if "=" in step:
        label, focalLengthStr = step.split("=")
        focalLength = int(focalLengthStr)
        labelHash = calcHash(label)
        boxLenses = boxes[labelHash]
        for i, (currentLabel, _) in enumerate(boxLenses):
            if currentLabel == label:
                boxLenses.pop(i)
                boxLenses.insert(i, (label, focalLength))
                break
        else:
            boxLenses.append((label, focalLength))
    else:
        assert "-" in step
        label, _ = step.split("-")
        labelHash = calcHash(label)
        boxLenses = boxes[labelHash]
        for i, (currentLabel, _) in enumerate(boxLenses):
            if currentLabel == label:
                boxLenses.pop(i)

part2Result = 0
for labelHash, boxLenses in boxes.items():
    for lensSlot, (_, focalLength) in enumerate(boxLenses):
        lensFocusingPower = (1 + labelHash) * (1 + lensSlot) * focalLength
        part2Result += lensFocusingPower

print(f"Part 2: {part2Result}")
