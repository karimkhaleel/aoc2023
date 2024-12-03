from typing import Any, Counter


def parse_data(data: str) -> tuple[list[int], list[int]]:
    l1 = []
    l2 = []
    for line in data.splitlines():
        ns = line.split("  ")
        i, j = int(ns[0]), int(ns[1])
        l1.append(i)
        l2.append(j)
    return l1, l2


def solution_one(data: str) -> Any:
    l1, l2 = parse_data(data)
    l1.sort()
    l2.sort()
    return sum(abs(i - j) for i, j in zip(l1, l2))


def solution_two(data: str) -> Any:
    l1, l2 = parse_data(data)
    l2c = Counter(l2)
    return sum(i * l2c[i] for i in l1)


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """3   4
4   3
2   5
1   3
3   9
3   3"""
    assert solution_one(data) == 11
    assert solution_two(data) == 31
