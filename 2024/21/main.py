import heapq
from functools import cache
from typing import Any


def parse_data(data: str) -> list[tuple[str, int]]:
    res = []
    for line in data.strip().splitlines():
        res.append((line, int(line[:-1])))
    return res


dirs = [(-1, 0, "^"), (1, 0, "v"), (0, -1, "<"), (0, 1, ">")]

type Numpad = tuple[tuple[str, str, str], tuple[str, str, str], tuple[str, str, str], tuple[str, str, str]]
type Arrows = tuple[tuple[str, str, str], tuple[str, str, str]]

arrows: Arrows = (
    ("#", "^", "A"),
    ("<", "v", ">"),
)
numpad: Numpad = (
    ("7", "8", "9"),
    ("4", "5", "6"),
    ("1", "2", "3"),
    ("#", "0", "A"),
)


@cache
def get_xy(grid: Numpad | Arrows, button: str) -> tuple[int, int]:
    for j, r in enumerate(grid):
        for i, c in enumerate(r):
            if c == button:
                return i, j
    return -1, -1


@cache
def find_best_segment_at_depth(is_numpad: bool, start: str, end: str, depth: int) -> int:
    if is_numpad:
        grid: Numpad | Arrows = numpad
    else:
        grid = arrows
    if len(grid) == 4:
        sx, sy = get_xy(numpad, start)
    else:
        sx, sy = get_xy(arrows, start)

    q: list[tuple[int, int, int, list[str], list[str]]] = [(0, sx, sy, [], [])]
    paths = []
    while q:
        d, x, y, v, p = heapq.heappop(q)
        if grid[y][x] == end:
            p.append("A")
            paths.append(p)
            continue
        for dy, dx, b in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and grid[ny][nx] not in v and grid[ny][nx] != "#":
                nv = v[:]
                nv.append(grid[ny][nx])
                np = p[:]
                np.append(b)
                heapq.heappush(q, (d + 1, nx, ny, nv, np))
    if depth > 0:
        m = find_best_path(False, tuple(paths[0]), depth - 1)
        for p in paths[1:]:
            cm = find_best_path(False, tuple(p), depth - 1)
            if cm < m:
                m = cm
        return m
    return len(paths[0])


def find_best_path(is_numpad: bool, code: tuple[str, ...], depth: int) -> int:
    start = "A"
    path: int = 0
    for c in code:
        segment = find_best_segment_at_depth(is_numpad, start, c, depth)
        path += segment
        start = c
    return path


def decode_path(path: str | list[str]) -> str:
    x, y = 2, 0
    r = []
    for c in path:
        match c:
            case "^":
                y -= 1
            case "v":
                y += 1
            case "<":
                x -= 1
            case ">":
                x += 1
            case "A":
                r.append(arrows[y][x])
    return "".join(r)


def solution_one(data: str) -> Any:
    res = 0
    codes = parse_data(data)
    for code, n in codes:
        path = find_best_path(True, tuple(code), 2)
        res += n * path
    return res


def solution_two(data: str) -> Any:
    res = 0
    codes = parse_data(data)
    for code, n in codes:
        path = find_best_path(True, tuple(code), 25)
        res += n * path
    return res


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
029A
980A
179A
456A
379A"""
    print()
    assert solution_one(data) == 126384
