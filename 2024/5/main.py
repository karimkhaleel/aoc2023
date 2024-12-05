from collections import defaultdict
from typing import Any


def parse_data(data: str) -> tuple[list[tuple[str, str]], list[list[str]]]:
    rules = []
    pages = []
    first_part = True
    for line in data.splitlines():
        if line == "":
            first_part = False
        if first_part:
            n1, n2 = line.split("|")
            rules.append((n1, n2))
        else:
            if line:
                pages.append(line.split(","))
    return rules, pages


def solution_one(data: str) -> Any:
    rules, pageset = parse_data(data)
    d = defaultdict(list)
    for s, e in rules:
        d[s].append(e)

    res = 0
    for pages in pageset:
        seen = set()
        for page in pages:
            if any(p in seen for p in d[page]):
                break
            seen.add(page)
        else:
            mid = int(pages[len(pages) // 2])
            res += mid
    return res


def solution_two(data: str) -> Any:
    rules, pageset = parse_data(data)
    d = defaultdict(set)
    for s, e in rules:
        d[s].add(e)

    res = 0
    for pages in pageset:
        op = []
        for p in pages:
            if not op:
                op.append(p)
            for i in range(len(op)):
                if p in d[op[i]]:
                    op.insert(i, p)
                    break
            else:
                if op[-1] != p:
                    op.append(p)
        res += int(op[len(op) // 2])

    return res - solution_one(data)


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    assert solution_one(data) == 143
    assert solution_two(data) == 123
