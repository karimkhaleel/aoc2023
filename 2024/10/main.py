from copy import copy
from typing import Any


def parse_data(data: str) -> list[list[int]]:
    res = []
    for r in data.strip().splitlines():
        res.append([int(c) if c != "." else -10000 for c in r])
    return res


def print_path(grid: list[list[int]], path: list[tuple[int, int, int]]):
    c = 0
    path.sort(key=lambda x: tuple([x[0], x[1]]))
    for i in range(len(grid)):
        row = []
        for j in range(len(grid[i])):
            if c < len(path) and path[c][0] == i and path[c][1] == j:
                row.append(str(path[c][2]))
                c += 1
            else:
                row.append(".")
        print("".join(row))


def dfs(
    grid: list[list[int]], x: int, y: int, path: list, trailends: set[tuple[int, int]]
):
    path.append((x, y, grid[x][y]))
    if grid[x][y] == 9:
        print_path(grid, path)
        trailends.add((x, y))
    # up
    new_x = x - 1
    if new_x >= 0 and grid[new_x][y] - grid[x][y] == 1:
        dfs(grid, new_x, y, copy(path), trailends)
    # down
    new_x = x + 1
    if new_x < len(grid) and grid[new_x][y] - grid[x][y] == 1:
        dfs(grid, new_x, y, copy(path), trailends)
    # left
    new_y = y - 1
    if new_y >= 0 and grid[x][new_y] - grid[x][y] == 1:
        dfs(grid, x, new_y, copy(path), trailends)
    # right
    new_y = y + 1
    if new_y < len(grid[x]) and grid[x][new_y] - grid[x][y] == 1:
        dfs(grid, x, new_y, copy(path), trailends)


def dfs_two(grid: list[list[int]], x: int, y: int, path: list) -> int:
    path.append((x, y, grid[x][y]))
    if grid[x][y] == 9:
        print_path(grid, path)
        return 1
    res = 0
    # up
    new_x = x - 1
    if new_x >= 0 and grid[new_x][y] - grid[x][y] == 1:
        res += dfs_two(grid, new_x, y, copy(path))
    # down
    new_x = x + 1
    if new_x < len(grid) and grid[new_x][y] - grid[x][y] == 1:
        res += dfs_two(grid, new_x, y, copy(path))
    # left
    new_y = y - 1
    if new_y >= 0 and grid[x][new_y] - grid[x][y] == 1:
        res += dfs_two(grid, x, new_y, copy(path))
    # right
    new_y = y + 1
    if new_y < len(grid[x]) and grid[x][new_y] - grid[x][y] == 1:
        res += dfs_two(grid, x, new_y, copy(path))

    return res


def solution_one(data: str) -> Any:
    grid = parse_data(data)
    res = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 0:
                trailends: set[tuple[int, int]] = set()
                dfs(grid, x, y, list(), trailends)
                res += len(trailends)
    return res


def solution_two(data: str) -> Any:
    grid = parse_data(data)
    res = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 0:
                res += dfs_two(grid, x, y, list())
    return res


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    assert solution_one(data) == 36
    assert solution_two(data) == 81
    data = """ ...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"""
    assert solution_one(data) == 2

    data = """..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""
    assert solution_one(data) == 4
