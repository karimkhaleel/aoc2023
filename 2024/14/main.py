import dataclasses
from typing import Any

from PIL import Image


@dataclasses.dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int


def parse_data(data: str) -> list[Robot]:
    robots = []
    for line in data.strip().splitlines():
        eq = line.index("=")
        comma = line.index(",")
        v = line.index("v")
        comma2 = line[v:].index(",")
        x = int(line[eq + 1 : comma])
        y = int(line[comma + 1 : v - 1])
        dx = int(line[v + 2 : v + comma2])
        dy = int(line[v + comma2 + 1 :])
        robots.append(Robot(x, y, dx, dy))
    return robots


def add_to_quadrant(q: list[int], x: int, y: int, X: int, Y: int) -> None:
    if x < X // 2 and y < Y // 2:
        q[0] += 1
    elif x > X // 2 and y < Y // 2:
        q[1] += 1
    elif x > X // 2 and y > Y // 2:
        q[2] += 1
    elif x < X // 2 and y > Y // 2:
        q[3] += 1


def add_frame(grid: list[list[bool]], x: int, y: int, idx: int, frames: list):
    img = Image.new("RGB", (x, y), "white")
    pixels = img.load()
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            if c:
                pixels[j, i] = (0, 0, 0)
    img.save(f"pics/{idx}.png")


def solution_one(data: str, x: int, y: int) -> Any:
    robots = parse_data(data)
    q = [0, 0, 0, 0]
    for robot in robots:
        add_to_quadrant(
            q, (robot.x + 100 * robot.dx) % x, (robot.y + 100 * robot.dy) % y, x, y
        )
    return q[0] * q[1] * q[2] * q[3]


def solution_two(data: str, x: int, y: int) -> Any:
    robots = parse_data(data)
    frames: list[Any] = []
    for i in range(8007):
        grid = [[False] * x for _ in range(y)]
        for robot in robots:
            nx, ny = ((robot.x + i * robot.dx) % x, (robot.y + i * robot.dy) % y)
            grid[ny][nx] = True
        add_frame(grid, x, y, i, frames)
    return 0


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data, 101, 103)}")
        print(f"two -> {solution_two(data, 101, 103)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    assert solution_one(data, 11, 7) == 12
