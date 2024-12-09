import math
from typing import Any


def solution_one(data: str) -> Any:
    data = data.strip("\n")
    expanded = []
    id = -1
    for i in range(len(data)):
        if i % 2 == 0:
            id += 1
            expanded.extend([str(id)] * int(data[i]))
        else:
            expanded.extend(["."] * int(data[i]))
    try:
        left = expanded.index(".")
    except ValueError:
        left = int(math.inf)
    try:
        right = len(expanded) - expanded[::-1].index(str(id)) - 1
    except ValueError:
        right = int(-math.inf)

    while left <= right:
        expanded[left], expanded[right] = expanded[right], expanded[left]
        left += 1
        while left < len(expanded) and expanded[left] != ".":
            left += 1
        right -= 1
        while right >= 0 and expanded[right] == ".":
            right -= 1
    return sum(i * int(n) for i, n in enumerate(expanded[: right + 1]))


def find_start_end(nums, id):
    left = nums.index(str(id))
    right = len(nums) - nums[::-1].index(str(id)) - 1
    return left, right


def solution_two(data: str) -> Any:
    data = data.strip("\n")
    expanded = []
    id = -1
    for i in range(len(data)):
        if i % 2 == 0:
            id += 1
            expanded.extend([str(id)] * int(data[i]))
        else:
            expanded.extend(["."] * int(data[i]))

    blocks: list[list[str]] = []
    block: list[str] = []
    for c in expanded:
        if not block:
            block.append(c)
            continue
        if block[-1] != c:
            blocks.append(block)
            block = [c]
        else:
            block.append(c)
    if block:
        blocks.append(block)

    i = len(blocks) - 1
    while i >= -1:
        if blocks[i][0] == ".":
            i -= 1
            continue
        for j in range(i):
            li = len(blocks[i])
            lj = len(blocks[j])
            if blocks[j][0] == "." and li <= lj:
                blocks[j] = blocks[i]
                if li < lj:
                    blocks.insert(j + 1, ["."] * (lj - li))
                    blocks[i + 1] = ["."] * li
                    i += 1
                else:
                    blocks[i] = ["."] * li
                break
        i -= 1

    expanded = []
    for block in blocks:
        expanded.extend(block)
    res = 0
    for i in range(len(expanded)):
        if expanded[i] != ".":
            res += int(expanded[i]) * i
    return res


def main():
    assert solution_two("0123102") == 24
    with open("input.txt", "r") as f:
        data = f.read().strip()
        print(f"one -> {solution_one(data)}")
        s2 = solution_two(data)
        print(f"two -> {s2}")
        print(s2 == 6485614478062)


if __name__ == "__main__":
    main()


def test_solution() -> None:
    # fmt: off
    assert solution_one("2333133121414131402") == 1928
    assert solution_two("2333133121414131402") == 2858
    assert solution_two("010101010101") == 0
    assert solution_two("101010101") == 30
    assert solution_two("12345") == 132
    assert solution_two("14113") == 16
    assert solution_two("1010101010101010101010") == 385
    assert solution_two("354631466260") == 1325
    assert solution_two("252") == 5
    assert solution_two("123125124123123") == 685
    assert solution_two("01231029") == 24
    assert solution_two("0123102") == 24
    # fmt: on
