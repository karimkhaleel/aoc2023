from typing import Any


def parse_data(data: str) -> tuple[list[str], list[str]]:
    lines = data.strip().splitlines()
    a = [x.strip() for x in lines[0].split(",")]
    d = lines[2:]
    return a, d


def dfs(design: str, available: list[str], visited: set[str]) -> bool:
    if design in visited:
        return False
    if not design:
        return True
    for a in available:
        if design[: len(a)] == a:
            if dfs(design[len(a) :], available, visited):
                return True
    visited.add(design)
    return False


def dfs_two(design: str, available: list[str], cache: dict[str, int]) -> int:
    if not design:
        return 1
    if design in cache:
        return cache[design]
    c = 0
    for a in available:
        if design[: len(a)] == a:
            c += dfs_two(design[len(a) :], available, cache)
    cache[design] = c
    return c


def solution_one(data: str) -> Any:
    available, designs = parse_data(data)
    res = 0
    for d in designs:
        v: set[str] = set()
        if dfs(d, available, v):
            res += 1
    return res


def solution_two(data: str) -> Any:
    available, designs = parse_data(data)
    res = 0
    cache: dict[str, int] = {}
    for d in designs:
        res += dfs_two(d, available, cache)
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
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

    assert solution_one(data) == 6
    assert solution_two(data) == 16
