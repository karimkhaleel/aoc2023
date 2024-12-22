from typing import Any


def parse_data(data: str) -> list[int]:
    res = []
    for line in data.strip().splitlines():
        res.append(int(line))
    return res


def parse_data_two(data: str) -> list[list[tuple[int, int]]]:
    res: list[list[tuple[int, int]]] = [[] for _ in range(len(data.strip().splitlines()))]
    for i, line in enumerate(data.strip().splitlines()):
        for x in line.split("|"):
            d, c = x.split(" ")
            res[i].append((int(d), int(c)))
    return res


def mix(x: int, y: int) -> int:
    return x ^ y


def prune(x: int) -> int:
    return x % 16777216


def process(x: int) -> int:
    # step 1
    x = prune(mix(x, x * 64))
    # step 2
    x = prune(mix(x, x // 32))
    # step 3
    return prune(mix(x, x * 2048))


def predict(x: int, d: int) -> int:
    for _ in range(d):
        x = process(x)
    return x


def solution_one(data: str) -> Any:
    nums = parse_data(data)
    r = 0
    for n in nums:
        r += predict(n, 2000)
    return r


def solution_two(data: str) -> Any:
    parsed_data = parse_data_two(data)
    ds: list[dict[tuple[int, int, int, int], int]] = []
    for sequence in parsed_data:
        d: dict[tuple[int, int, int, int], int] = {}
        for i in range(3, len(sequence)):
            v3, c3 = sequence[i - 3]
            v2, c2 = sequence[i - 2]
            v1, c1 = sequence[i - 1]
            v0, c0 = sequence[i - 0]
            if (c3, c2, c1, c0) not in d:
                d[(c3, c2, c1, c0)] = v0
        ds.append(d)
    all_keys: set[tuple[int, int, int, int]] = set()
    for d in ds:
        for k in d:
            all_keys.add(k)
    best = 0
    best_key = None
    for key in all_keys:
        current_best = 0
        for d in ds:
            current_best += d.get(key, 0)
        if best < current_best:
            best = current_best
            best_key = key
    print(best_key)
    return best


def prepare_data_for_sol_two(data: str) -> None:
    nums = parse_data(data)
    res: list[list[tuple[int, int]]] = [[(n % 10, 0)] for n in nums]
    for i in range(len(nums)):
        r = nums[i]
        for _ in range(2000):
            r = process(r)
            x = r % 10
            res[i].append((x, x - res[i][-1][0]))
    with open("input2test.txt", "w") as f:
        for seed in res:
            f.write("|".join([f"{v[0]} {v[1]}" for v in seed]))
            f.write("\n")


def get_data(path: str) -> str:
    with open(path) as f:
        data = f.read()
        return data


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
    with open("input2.txt", "r") as f:
        data = f.read()
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
1
10
100
2024"""
    assert solution_one(data) == 37327623
    data = get_data("input2test.txt")
    assert solution_two(data) == 23
