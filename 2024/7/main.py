from typing import Any


def parse_data(data: str) -> list[tuple[int, list[int]]]:
    parsed: list[tuple[int, list[int]]] = []
    for line in data.splitlines():
        res, v = line.split(":")
        nums = [int(x.strip(" ")) for x in v.strip(" ").split(" ")]
        parsed.append((int(res), nums))
    return parsed


def dfs_one(expected: int, res: int, nums: list[int]):
    if not nums:
        if res == expected:
            return res
        else:
            return None
    res_add = dfs_one(expected, res + nums[0], nums[1:])
    if res_add is not None:
        return res_add
    res_mul = dfs_one(expected, res * nums[0], nums[1:])
    if res_mul is not None:
        return res_mul


def dfs_two(expected: int, res: int, nums: list[int]):
    if not nums:
        if res == expected:
            return res
        else:
            return None
    res_add = dfs_two(expected, res + nums[0], nums[1:])
    if res_add is not None:
        return res_add
    res_mul = dfs_two(expected, res * nums[0], nums[1:])
    if res_mul is not None:
        return res_mul
    res_concat = dfs_two(expected, int(str(res) + str(nums[0])), nums[1:])
    if res_concat is not None:
        return res_concat


def solution_one(data: str) -> Any:
    res = 0
    lines = parse_data(data)
    for expected, nums in lines:
        if dfs_one(expected, nums[0], nums[1:]) is not None:
            res += expected
    return res


def solution_two(data: str) -> Any:
    res = 0
    lines = parse_data(data)
    for expected, nums in lines:
        if dfs_two(expected, nums[0], nums[1:]) is not None:
            res += expected
    return res


def main():
    data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    assert solution_one(data) == 3749
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    assert solution_one(data) == 3749
    assert solution_two(data) == 11387
