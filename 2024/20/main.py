import copy
import heapq
from typing import Any, Callable


def parse_data(data: str) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    grid = []
    start = (-1, -1)
    end = (-1, -1)
    for i, r in enumerate(data.strip().splitlines()):
        row = []
        for j, c in enumerate(r):
            row.append(c)
            if c == "S":
                start = (j, i)
            if c == "E":
                end = (j, i)
        grid.append(row)
    return grid, start, end


def print_grid(grid: list[list[str]], path: dict[tuple[int, int], tuple[int, int]]):
    for i, r in enumerate(grid):
        row = []
        for j, c in enumerate(r):
            if (j, i) in path and grid[i][j] not in ["S", "E"]:
                row.append(" ")
            else:
                row.append(c)
        print("".join(row))


dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def create_solver(grid: list[list[str]]) -> Callable[[int, int, int, int], int]:
    cache: dict[tuple[int, int], int] = {}

    def f(sx: int, sy: int, ex: int, ey: int) -> int:
        if (sx, sy) in cache:
            return cache[sx, sy]
        q: list[tuple[int, int, int, dict[tuple[int, int], int]]] = [(0, sx, sy, {(sx, sy): -1})]
        visited: set[tuple[int, int]] = set([(sx, sy)])
        while q:
            d, x, y, p = heapq.heappop(q)
            if (x, y) == (ex, ey):
                for xx, yy in p:
                    cache[xx, yy] = len(p) - p[xx, yy]
                return len(p)
            for dy, dx in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[nx]) and grid[ny][nx] != "#" and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    np = copy.copy(p)
                    np[(nx, ny)] = d + 1
                    heapq.heappush(q, (d + 1, nx, ny, np))
        return -1

    return f


def find_path(grid: list[list[str]], sx: int, sy: int, ex: int, ey: int) -> dict[tuple[int, int], tuple[int, int]]:
    q: list[tuple[int, int, int, dict[tuple[int, int], tuple[int, int]]]] = [(0, sx, sy, {(sx, sy): (-1, -1)})]
    visited: set[tuple[int, int]] = set([(sx, sy)])
    while q:
        d, x, y, p = heapq.heappop(q)
        if (x, y) == (ex, ey):
            L = len(p)
            p[(sx, sy)] = (0, L)
            for k in list(p.keys())[1:]:
                p[k] = (p[k][0], L - p[k][0])
            return p
        for dy, dx in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[nx]) and grid[ny][nx] != "#" and (nx, ny) not in visited:
                visited.add((nx, ny))
                np = copy.copy(p)
                np[(nx, ny)] = (d + 1, -1)
                heapq.heappush(q, (d + 1, nx, ny, np))
    return {}


cdirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]


def find_cheats(
    grid: list[list[str]],
    sx: int,
    sy: int,
    ex: int,
    ey: int,
    path: dict[tuple[int, int], tuple[int, int]],
) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
    cheats: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
    f = create_solver(grid)
    for x, y in path:
        for (dx, dy), (cdx, cdy) in zip(dirs, cdirs):
            # cheat middle (x, y)
            cmx, cmy = x + dx, y + dy
            # cheat end (x, y)
            cex, cey = x + cdx, y + cdy
            if 0 <= cey < len(grid) and 0 <= cex < len(grid[cey]) and grid[cmy][cmx] == "#" and grid[cey][cex] != "#":
                cheats[((x, y), (cex, cey))] = path[x, y][0] + 1 + f(cex, cey, ex, ey)
    return cheats


def find_cheats_two(
    grid: list[list[str]],
    sx: int,
    sy: int,
    ex: int,
    ey: int,
    path: dict[tuple[int, int], tuple[int, int]],
) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
    cheats: dict[tuple[tuple[int, int], tuple[int, int]], int] = {}
    f = create_solver(grid)
    for x, y in path:
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and grid[ny][nx] == "#":
                for cdy in range(-20, 21):
                    for cdx in range(-20, 21):
                        cex, cey = x + cdx, y + cdy
                        cheat_length = abs(cdy) + abs(cdx)
                        if (
                            cheat_length <= 20
                            and 0 <= cey < len(grid)
                            and 0 <= cex < len(grid[cey])
                            and grid[cey][cex] != "#"
                        ):
                            cheats[((x, y), (cex, cey))] = path[x, y][0] + cheat_length + f(cex, cey, ex, ey)
    return cheats


def solution_one(data: str, save: int) -> Any:
    grid, (sx, sy), (ex, ey) = parse_data(data)
    p = find_path(grid, sx, sy, ex, ey)
    cheats = find_cheats(grid, sx, sy, ex, ey, p)
    i = 0
    for cheat in cheats:
        if len(p) - cheats[cheat] >= save:
            i += 1
    return i


def solution_two(data: str, save: int) -> Any:
    grid, (sx, sy), (ex, ey) = parse_data(data)
    p = find_path(grid, sx, sy, ex, ey)
    cheats = find_cheats_two(grid, sx, sy, ex, ey, p)
    i = 0
    for cheat in cheats:
        if len(p) - cheats[cheat] >= save:
            i += 1
    return i


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data, 100)}")
        print(f"two -> {solution_two(data, 100)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    print()
    assert solution_one(data, 2) == 44
    assert solution_two(data, 50) == 285
