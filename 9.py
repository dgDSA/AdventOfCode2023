"""
Advent of Code 2023
Day 9: Mirage Maintenance

Daniel Herding
"""

import re

R_NUM = re.compile(r"([-\d])+")

with open("9.txt") as f:
    input = f.read()

def diffs(nums):
    result = []
    for i in range(len(nums) - 1):
        result.append(nums[i + 1] - nums[i])
    return result

def extrapolate(nums):
    if len(nums) == 2:
        return nums[1] - nums[0]
    
    next = nums[-1] + extrapolate(diffs(nums))
    return next

lines = input.split("\n")
part1Result = 0

for line in lines:
    nums = [int(m.group()) for m in R_NUM.finditer(line)]
    next = extrapolate(nums)
    part1Result += next

print(f"Part 1 result: {part1Result}")


part2Result = 0

for line in lines:
    nums = [int(m.group()) for m in R_NUM.finditer(line)]
    nums.reverse()
    next = extrapolate(nums)
    part2Result += next

print(f"Part 2 result: {part2Result}")
