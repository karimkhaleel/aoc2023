import re
from typing import Any


def solution_one(data: str) -> Any:
    res = 0
    pattern = re.compile(r"(mul\((\d+),(\d+)\))")
    for m in pattern.finditer(data):
        res += int(m[2]) * int(m[3])
    return res


def solution_two(data: str) -> Any:
    res = 0
    pattern = re.compile(r"don't\(\)|do\(\)|(mul\((\d+),(\d+)\))")
    do = True
    for m in pattern.finditer(data):
        if m[0] == "don't()":
            do = False
        elif m[0] == "do()":
            do = True
        elif do:
            res += int(m[2]) * int(m[3])
    return res


def main():
    data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert solution_two(data) == 48
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    assert solution_one(data) == 161
    data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    assert solution_two(data) == 48
