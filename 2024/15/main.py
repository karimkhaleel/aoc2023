from typing import Any


def parse_data(data: str) -> tuple[list[list[str]], list[str]]:
    grid = []
    moves = []
    lines = data.strip().splitlines()
    for i, line in enumerate(lines):
        if line == "":
            break
        grid.append(list(line))
    for line in lines[i + 1 :]:
        moves.extend(list(line))
    return grid, moves


def parse_data_two(data: str) -> tuple[list[list[str]], list[str]]:
    grid = []
    moves = []
    lines = data.strip().splitlines()
    for i, line in enumerate(lines):
        if line == "":
            break
        row = []
        for c in line:
            if c == "O":
                row.append("[")
                row.append("]")
            elif c == "@":
                row.append("@")
                row.append(".")
            else:
                row.append(c)
                row.append(c)
        grid.append(row)
    for line in lines[i + 1 :]:
        moves.extend(list(line))
    return grid, moves


def print_grid(grid: list[list[str]]) -> None:
    for r in grid:
        print("".join(r))


def find_left(row: list[str], c: int) -> int:
    row = row[:c][::-1]
    box = len(row) - row.index("#") - 1
    try:
        free_space = len(row) - row.index(".") - 1
        if box > free_space:
            return -1
        return free_space
    except ValueError:
        return -1


def find_right(row: list[str], c: int) -> int:
    box = row[c:].index("#")
    try:
        free_space = row[c:].index(".")
        if box < free_space:
            return -1
        return free_space + c
    except ValueError:
        return -1


def solution_one(data: str) -> Any:
    grid, moves = parse_data(data)
    rx, ry = 0, 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == "@":
                rx, ry = x, y
    for m in moves:
        match m:
            case "^":
                d = [row[rx] for row in grid]
                i = find_left(d, ry)
                if i == -1:
                    continue
                grid[ry][rx] = "."
                if i + 1 != ry:  # We have a box in front of us
                    grid[i][rx] = "O"
                ry -= 1
                grid[ry][rx] = "@"
            case "v":
                d = [row[rx] for row in grid]
                i = find_right(d, ry)
                if i == -1:
                    continue
                grid[ry][rx] = "."
                if i - 1 != ry:  # We have a box in front of us
                    grid[i][rx] = "O"
                ry += 1
                grid[ry][rx] = "@"
            case "<":
                i = find_left(grid[ry], rx)
                if i == -1:
                    continue
                grid[ry][rx] = "."
                if i + 1 != rx:  # We have a box in front of us
                    grid[ry][i] = "O"
                rx -= 1
                grid[ry][rx] = "@"
            case ">":
                i = find_right(grid[ry], rx)
                if i == -1:
                    continue
                grid[ry][rx] = "."
                if i - 1 != rx:  # We have a box in front of us
                    grid[ry][i] = "O"
                rx += 1
                grid[ry][rx] = "@"
    res = 0
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "O":
                res += y * 100 + x
    return res


def can_move(
    grid: list[list[str]],
    boxes: set[tuple[int, int]],
    x: int,
    y: int,
    nx: int,
    ny: int,
) -> bool:
    if grid[y][x] == "]":
        x = x - 1
        nx = nx - 1

    dy = ny - y
    if grid[ny][nx] == "." and grid[ny][nx + 1] == ".":
        boxes.add((x, y))
        return True
    elif grid[ny][nx] == "]" and grid[ny][nx + 1] == ".":
        if can_move(grid, boxes, nx - 1, ny, nx - 1, ny + dy):
            boxes.add((x, y))
            return True
    elif grid[ny][nx] == "[" and grid[ny][nx + 1] == ".":
        if can_move(grid, boxes, nx, ny, nx, ny + dy):
            boxes.add((x, y))
            return True

    elif grid[ny][nx] == "." and grid[ny][nx + 1] == "[":
        if can_move(grid, boxes, nx + 1, ny, nx + 1, ny + dy):
            boxes.add((x, y))
            return True

    elif grid[ny][nx] == "]" and grid[ny][nx + 1] == "[":
        if can_move(grid, boxes, nx - 1, ny, nx - 1, ny + dy) and can_move(
            grid, boxes, nx + 1, ny, nx + 1, ny + dy
        ):
            boxes.add((x, y))
            return True
    elif grid[ny][nx] == "[" and grid[ny][nx + 1] == "]":
        if can_move(grid, boxes, nx, ny, nx, ny + dy):
            boxes.add((x, y))
            return True
    return False


def vmove_if_can(
    grid: list[list[str]],
    x: int,
    y: int,
    nx: int,
    ny: int,
) -> tuple[int, int]:
    if grid[ny][nx] == ".":
        grid[y][x] = "."
        grid[ny][nx] = "@"
        return nx, ny
    elif grid[ny][nx] == "#":
        return x, y

    boxes: set[tuple[int, int]] = set()
    dy = ny - y
    if can_move(grid, boxes, nx, ny, nx, ny + dy):
        for bx, by in boxes:
            grid[by + dy][bx] = "["
            grid[by + dy][bx + 1] = "]"
            grid[by][bx] = "."
            grid[by][bx + 1] = "."
        grid[y][x] = "."
        grid[ny][nx] = "@"
        return nx, ny
    return x, y


def hmove_if_can(
    grid: list[list[str]], x: int, y: int, nx: int, ny: int
) -> tuple[int, int]:
    if grid[ny][nx] == "[" or grid[ny][nx] == "]":
        dx = nx - x
        hmove_if_can(grid, nx, ny, nx + dx, ny)
    if (grid[y][x] == "[" or grid[y][x] == "]") and grid[ny][nx] == ".":
        grid[ny][nx] = grid[y][x]
        grid[y][x] = "."
    elif grid[y][x] == "@" and grid[ny][nx] == ".":
        grid[ny][nx] = "@"
        grid[y][x] = "."
    else:
        return x, y
    return nx, ny


def solution_two(data: str) -> Any:
    grid, moves = parse_data_two(data)
    rx, ry = 0, 0
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == "@":
                rx, ry = x, y
    for i, m in enumerate(moves):
        match m:
            case "^":
                rx, ry = vmove_if_can(grid, rx, ry, rx, ry - 1)
            case "v":
                rx, ry = vmove_if_can(grid, rx, ry, rx, ry + 1)
            case "<":
                rx, ry = hmove_if_can(grid, rx, ry, rx - 1, ry)
            case ">":
                rx, ry = hmove_if_can(grid, rx, ry, rx + 1, ry)
    res = 0
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == "[":
                res += y * 100 + x
    return res


def main():
    data = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
    assert solution_two(data) == 9021
    print()
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
    print()
    assert solution_one(data) == 10092
    assert solution_two(data) == 9021
