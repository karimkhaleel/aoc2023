from functools import lru_cache
from typing import Any


def parse_data(data: str) -> list[int]:
    return [int(d) for d in data.strip().split(" ")]


def solution_one(data: str) -> Any:
    stones = parse_data(data)
    for _ in range(25):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                strstone = str(stone)
                new_stones.append(int(strstone[: len(strstone) // 2]))
                new_stones.append(int(strstone[len(strstone) // 2 :]))
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    return len(stones)


@lru_cache(maxsize=None)
def dfs(stone: int, i: int) -> int:
    if i == 75:
        return 1
    if stone == 0:
        return dfs(1, i + 1)
    elif len(str(stone)) % 2 == 0:
        strstone = str(stone)
        return dfs(int(strstone[len(strstone) // 2 :]), i + 1) + dfs(
            int(strstone[: len(strstone) // 2]), i + 1
        )
    else:
        return dfs(stone * 2024, i + 1)


def solution_two(data: str) -> Any:
    stones = parse_data(data)
    res = 0
    for stone in stones:
        res += dfs(stone, 0)
    return res


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    assert solution_one("125 17") == 55312
