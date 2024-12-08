from typing import Any


def parse_data(data: str) -> tuple[list[list[str]], int, int]:
    gridraw = data.splitlines()
    grid = [[x for x in r] for r in gridraw]
    x, y = 0, 0
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            if c == "^":
                x, y = i, j
                break
        else:
            continue
        break
    return grid, x, y


def solution_one(data: str) -> Any:
    grid, x, y = parse_data(data)
    res = 1
    dx, dy = -1, 0
    while 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        if grid[x][y] == "#":
            # step back
            x, y = x - dx, y - dy
            if (dx, dy) == (-1, 0):
                dx, dy = 0, 1
            elif (dx, dy) == (0, 1):
                dx, dy = 1, 0
            elif (dx, dy) == (1, 0):
                dx, dy = (0, -1)
            elif (dx, dy) == (0, -1):
                dx, dy = (-1, 0)
        if grid[x][y] == ".":
            res += 1
        grid[x][y] = "X"
        x, y = x + dx, y + dy
    return res


def can_leave(
    x: int,
    y: int,
    dx: int,
    dy: int,
    visited: set[tuple[int, int, int, int]],
    grid: list[list[str]],
) -> bool:
    if (x, y, dx, dy) in visited:
        return False
    visited.add((x, y, dx, dy))
    while 0 <= x < len(grid) and 0 <= y < len(grid[x]):
        new_x = x + dx
        new_y = y + dy
        if (
            0 <= new_x < len(grid)
            and 0 <= new_y < len(grid[new_x])
            and grid[new_x][new_y] == "#"
        ):
            return can_leave(x, y, dy, -dx, visited, grid)
        x, y = new_x, new_y

    return True


def solution_two(data: str) -> Any:
    grid, x, y = parse_data(data)
    xi, yi = x, y
    blockers = set()
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == ".":
                if (x, y) == (6, 3):
                    pass
                grid[x][y] = "#"
                if not can_leave(xi, yi, -1, 0, set(), grid):
                    blockers.add((x, y))
                grid[x][y] = "."
    return len(blockers)


def main():
    data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

    assert solution_one(data) == 41
    assert solution_two(data) == 6
