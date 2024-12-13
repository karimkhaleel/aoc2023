from typing import Any


def parse_data(data: str) -> list[list[str]]:
    return [list(r) for r in data.strip().splitlines()]


dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))


def dfs(
    grid: list[list[str]], c: str, i: int, j: int, p: int, a: int
) -> tuple[int, int]:
    if not (0 <= i < len(grid) and 0 <= j < len(grid[i])):
        return 0, p + 1
    if grid[i][j] == f"X{c}":
        return 0, 0
    if len(grid[i][j]) == 2:
        return 0, 1
    if grid[i][j] != c:
        return 0, p + 1
    grid[i][j] = f"X{c}"
    na, np = 0, 0
    for dir in dirs:
        naa, npp = dfs(grid, c, i + dir[0], j + dir[1], p, a)
        na += naa
        np += npp
    return na + 1, np


def solution_one(data: str) -> Any:
    grid = parse_data(data)
    res = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if len(grid[i][j]) != 2:
                a, p = dfs(grid, grid[i][j], i, j, 0, 0)
                res += a * p
    return res


def dfs_two(
    grid: list[list[str]], c: str, i: int, j: int, flowers: list[tuple[int, int]]
):
    if not (0 <= i < len(grid) and 0 <= j < len(grid[i])):
        return
    if len(grid[i][j]) == 2:
        return
    if grid[i][j] != c:
        return
    grid[i][j] = f"X{c}"
    for dir in dirs:
        dfs_two(grid, c, i + dir[0], j + dir[1], flowers)
    flowers.append((i, j))


def solution_two(data: str) -> Any:
    grid = parse_data(data)
    res = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if len(grid[i][j]) != 2:
                flowers: list[tuple[int, int]] = []
                dfs_two(grid, grid[i][j], i, j, flowers)
                res += len(flowers) * get_num_sides(flowers)
    return res


def get_num_sides(flowers: list[tuple[int, int]]) -> int:
    x1 = min([g[0] for g in flowers])
    y1 = min([g[1] for g in flowers])
    x2 = max([g[0] for g in flowers]) + 1
    y2 = max([g[1] for g in flowers]) + 1
    garden = [[0] * (y2 - y1) for _ in range(x2 - x1)]
    for x, y in flowers:
        garden[x - x1][y - y1] = 1

    total = 0
    # tops
    sides = 0
    for x in range(len(garden)):
        in_side = False
        for y in range(len(garden[x])):
            if garden[x][y] and (x == 0 or not garden[x - 1][y]):
                if not in_side:
                    sides += 1
                    in_side = True
            else:
                in_side = False
    total += sides
    # bottoms
    sides = 0
    for x in reversed(range(len(garden))):
        in_side = False
        for y in range(len(garden[x])):
            if garden[x][y] and (x == len(garden) - 1 or not garden[x + 1][y]):
                if not in_side:
                    sides += 1
                    in_side = True
            else:
                in_side = False
    total += sides
    # lefts
    sides = 0
    for y in range(len(garden[0])):
        in_side = False
        for x in range(len(garden)):
            if garden[x][y] and (y == 0 or not garden[x][y - 1]):
                if not in_side:
                    sides += 1
                    in_side = True
            else:
                in_side = False
    total += sides
    # rights
    sides = 0
    for y in reversed(range(len(garden[0]))):
        in_side = False
        for x in range(len(garden)):
            if garden[x][y] and (y == len(garden[0]) - 1 or not garden[x][y + 1]):
                if not in_side:
                    sides += 1
                    in_side = True
            else:
                in_side = False
    total += sides
    return total


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

    assert solution_one(data) == 1930
    assert solution_two(data) == 1206
