from typing import Any

type Key = tuple[int, ...]
type Lock = tuple[int, ...]


def parse_data(data: str) -> tuple[list[Key], list[Lock]]:
    lines = data.strip().splitlines()
    keys: list[Key] = []
    locks: list[Lock] = []
    i = 0
    while i < len(lines):
        item = [0, 0, 0, 0, 0]
        j = i + 1
        is_lock = lines[i][0] == "#"
        while j - i < 7:
            for xi, x in enumerate(lines[j]):
                item[xi] += lines[j][xi] == "#" if is_lock else lines[j][xi] == "."
            j += 1
        if is_lock:
            locks.append(tuple(item))
        else:
            item = [5 - x for x in item]
            keys.append(tuple(item))
        i += 8
    return keys, locks


def solution_one(data: str) -> Any:
    keys, locks = parse_data(data)
    res = 0
    for key in keys:
        for lock in locks:
            res += all([kk + ll <= 5 for kk, ll in zip(key, lock)])
    return res


def solution_two(data: str) -> Any:
    pass


def main():
    data = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
    assert solution_one(data) == 3
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
    print()
    assert solution_one(data) == 3
