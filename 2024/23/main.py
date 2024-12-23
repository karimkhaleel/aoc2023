from collections import defaultdict
from copy import copy
from typing import Any, MutableMapping


def parse_data(data: str) -> list[tuple[str, str]]:
    rows = []
    for line in data.strip().splitlines():
        x, y = line.split("-")
        rows.append((x, y))
    return rows


def solution_one(data: str) -> Any:
    parsed_data = parse_data(data)
    d: MutableMapping[str, set[str]] = defaultdict(set)
    for a, b in parsed_data:
        d[a].add(b)
        d[b].add(a)
    keys = list(d.keys())
    valid_sets: set[tuple[str, ...]] = set()
    for i in range(len(keys)):
        for j in d[keys[i]]:
            inter = d[keys[i]].intersection(d[j])
            for ix in inter:
                valid_sets.add(tuple(sorted((keys[i], j, ix))))
    res = 0
    for vs in valid_sets:
        for comp in vs:
            if comp.startswith("t"):
                res += 1
                break
    return res


def find_best_set(
    d: MutableMapping[str, set[str]],
    connected_computers: list[str],
    to_check: list[str],
    current_set: set[str],
) -> list[str]:
    if not current_set or not to_check:
        return connected_computers

    # included
    connected_if_include = copy(connected_computers)
    if_include_set = current_set.intersection([to_check[0], *d[to_check[0]]])
    if set(connected_computers).issubset(if_include_set):
        connected_if_include.append(to_check[0])
        connected_if_include = find_best_set(d, connected_if_include, to_check[1:], if_include_set)

    # excluded
    connected_if_exclude = find_best_set(d, copy(connected_computers), to_check[1:], copy(current_set))
    if len(connected_if_include) > len(connected_if_exclude):
        return connected_if_include
    else:
        return connected_if_exclude


def solution_two(data: str) -> Any:
    parsed_data = parse_data(data)
    d: MutableMapping[str, set[str]] = defaultdict(set)
    for a, b in parsed_data:
        d[a].add(b)
        d[b].add(a)
    keys = list(d.keys())
    longest: list[str] = []
    for i in range(len(keys)):
        common = set()
        common.add(keys[i])
        common.update(d[keys[i]])
        current_best = find_best_set(d, [keys[i]], list(d[keys[i]]), common)
        if len(longest) < len(current_best):
            longest = current_best

    return ",".join(sorted(longest))


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

    print()
    assert solution_one(data) == 7
    assert solution_two(data) == "co,de,ka,ta"
