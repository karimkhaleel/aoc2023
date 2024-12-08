from collections import defaultdict
from typing import Any, Mapping


def parse_data(data: str) -> Mapping[str, list[tuple[int, int]]]:
    parsed = defaultdict(list)
    for i, r in enumerate(data.splitlines()):
        for j, c in enumerate(r):
            if c != ".":
                parsed[c].append((i, j))
    return parsed


def solution_one(data: str) -> Any:
    rows = data.splitlines()
    ROWS = len(rows)
    COLS = len(rows[0])
    antennas = parse_data(data)
    nodes: set[tuple[int, int]] = set()
    for freq in antennas:
        for i in range(len(antennas[freq])):
            for j in range(i + 1, len(antennas[freq])):
                a1 = antennas[freq][i]
                a2 = antennas[freq][j]
                diff = a1[0] - a2[0], a1[1] - a2[1]
                n1 = a1[0] + diff[0], a1[1] + diff[1]
                n2 = a2[0] - diff[0], a2[1] - diff[1]
                if 0 <= n1[0] < ROWS and 0 <= n1[1] < COLS:
                    nodes.add(n1)
                if 0 <= n2[0] < ROWS and 0 <= n2[1] < COLS:
                    nodes.add(n2)

    return len(nodes)


def solution_two(data: str) -> Any:
    rows = data.splitlines()
    ROWS = len(rows)
    COLS = len(rows[0])
    antennas = parse_data(data)
    nodes: set[tuple[int, int]] = set()
    for freq in antennas:
        if len(antennas[freq]) > 1:
            for i in range(len(antennas[freq])):
                nodes.add((antennas[freq][i][0], antennas[freq][i][1]))
        for i in range(len(antennas[freq])):
            for j in range(i + 1, len(antennas[freq])):
                a1 = antennas[freq][i]
                a2 = antennas[freq][j]
                diff = a1[0] - a2[0], a1[1] - a2[1]
                n1 = a1[0] + diff[0], a1[1] + diff[1]
                while 0 <= n1[0] < ROWS and 0 <= n1[1] < COLS:
                    if 0 <= n1[0] < ROWS and 0 <= n1[1] < COLS:
                        nodes.add(n1)
                    n1 = n1[0] + diff[0], n1[1] + diff[1]
                n2 = a2[0] - diff[0], a2[1] - diff[1]
                while 0 <= n2[0] < ROWS and 0 <= n2[1] < COLS:
                    if 0 <= n2[0] < ROWS and 0 <= n2[1] < COLS:
                        nodes.add(n2)
                    n2 = n2[0] - diff[0], n2[1] - diff[1]

    return len(nodes)


def main():
    data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    assert solution_two(data) == 34
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    assert solution_one(data) == 14
    assert solution_two(data) == 34


def test_solution1() -> None:
    data = """..........
..........
..........
....aa....
..........
....aa....
..........
..........
..........
.........."""

    assert solution_one(data) == 12
