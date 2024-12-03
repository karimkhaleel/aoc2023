from typing import Any, Iterable


def parse_data(data: str) -> list[list[int]]:
    res = []
    for line in data.splitlines():
        res.append([int(i) for i in line.split(" ")])
    return res


def solution_one(data: str) -> Any:
    res = 0
    for report in parse_data(data):
        safe = 0
        # increasing
        for i in range(1, len(report)):
            if not 1 <= report[i] - report[i - 1] <= 3:
                break
        else:
            safe = 1

        # decreasing
        if not safe:
            for i in range(1, len(report)):
                if not 1 <= report[i - 1] - report[i] <= 3:
                    break
            else:
                safe = 1

        res += safe

    return res


def skip_one(report: list[int]) -> Iterable[list[int]]:
    for i in range(len(report)):
        r = report[:i] + report[i + 1 :]
        yield r
        yield r[::-1]


def is_safe(report: list[int]):
    i = 0
    for report in skip_one(report):
        i = 0
        while i < len(report) - 1:
            if not 1 <= report[i] - report[i + 1] <= 3:
                break
            i += 1
        else:
            return True
    return False


def solution_two(data: str) -> Any:
    res = 0
    for report in parse_data(data):
        res += is_safe(report)
    return res


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    assert solution_one(data) == 2
    assert solution_two(data) == 4
