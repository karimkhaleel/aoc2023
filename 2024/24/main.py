import operator
from collections import deque
from typing import Any, Callable, Mapping


def parse_data(data: str) -> tuple[dict[str, bool], deque[tuple[str, str, str, str]]]:
    lines = data.strip().splitlines()
    facts: dict[str, bool] = {}
    q: deque[tuple[str, str, str, str]] = deque([])
    for i in range(len(lines)):
        if lines[i] == "":
            break
        x, y = lines[i].split(": ")
        facts[x] = y == "1"

    for i in range(i + 1, len(lines)):
        p, a = lines[i].split(" -> ")
        x, y, z = p.split(" ")
        q.append((x, y, z, a))
    return facts, q


def solution_one(data: str) -> Any:
    initial_facts, q = parse_data(data)

    facts = create_circuit(initial_facts, q)

    zs = []
    for f, c in facts.items():
        if f.startswith("z"):
            zs.append((-int(f[1:]), c()))
    zs.sort()
    return int("".join(["1" if z[1] else "0" for z in zs]), 2)


def create_circuit(initial_facts: Mapping[str, bool], q) -> dict[str, Callable[[], bool]]:
    facts: dict[str, Callable[[], bool]] = {}

    def make_gate(op, x, y, op_str):
        def gate(p1=x, p2=y, i=0):
            res = op(
                (facts.get(p1)(i=i + 1) if facts.get(p1) else initial_facts.get(p1)),
                (facts.get(p2)(i=i + 1) if facts.get(p2) else initial_facts.get(p2)),
            )
            return res

        return gate

    for p1, p, p2, r in q:
        match p:
            case "AND":
                facts[r] = make_gate(operator.and_, p1, p2, "AND")
            case "OR":
                facts[r] = make_gate(operator.or_, p1, p2, "OR")
            case "XOR":
                facts[r] = make_gate(operator.xor, p1, p2, "XOR")

    return facts


def get_ans_2(x: int, y: int, initial_facts: dict[str, bool], facts: dict[str, Callable[[], bool]]) -> int:
    x_bin = [z == "1" for z in reversed(f"{bin(x)[2:]:0>45}")]
    y_bin = [z == "1" for z in reversed(f"{bin(y)[2:]:0>45}")]

    for i, (xx, yy) in enumerate(zip(x_bin, y_bin)):
        initial_facts[f"x{i:0>2}"] = xx
        initial_facts[f"y{i:0>2}"] = yy
    return get_num(facts, "z")


def get_ans(input: str, x: int, y: int):
    x_bin = [z == "1" for z in reversed(f"{bin(x)[2:]:0>45}")]
    y_bin = [z == "1" for z in reversed(f"{bin(y)[2:]:0>45}")]

    with open(input) as f:
        data = f.read()
    initial_facts, q = parse_data(data)
    for i, (xx, yy) in enumerate(zip(x_bin, y_bin)):
        initial_facts[f"x{i:0>2}"] = xx
        initial_facts[f"y{i:0>2}"] = yy
    facts = create_circuit(initial_facts, q)
    return get_num(facts, "z")


def get_ans_3(a: str, b: str, x: int, y: int):
    x_bin = [z == "1" for z in reversed(f"{bin(x)[2:]:0>45}")]
    y_bin = [z == "1" for z in reversed(f"{bin(y)[2:]:0>45}")]

    with open("input2.txt") as f:
        data = f.read()
    initial_facts, q = parse_data(data)
    for i, (xx, yy) in enumerate(zip(x_bin, y_bin)):
        initial_facts[f"x{i:0>2}"] = xx
        initial_facts[f"y{i:0>2}"] = yy
    facts = create_circuit(initial_facts, q)
    facts[a], facts[b] = facts[b], facts[a]
    return get_num(facts, "z"), x + y, get_num(facts, "z") == x + y


def solution_two(data: str) -> Any:
    initial_facts, q = parse_data(data)

    facts = create_circuit(initial_facts, q)

    swapped = set(["z14", "vhm", "z27", "mps", "z39", "msq"])

    keys = list(facts.keys())
    for i in range(len(facts)):
        if keys[i] in swapped:
            continue
        for j in range(i + 1, len(facts)):
            if keys[j] in swapped:
                continue
            facts[keys[i]], facts[keys[j]] = facts[keys[j]], facts[keys[i]]
            try:
                r = get_ans_2(51112, 512351, initial_facts, facts)
            except:
                r = -1
            if r == 51112 + 512351:
                print(keys[i], keys[j])
            facts[keys[i]], facts[keys[j]] = facts[keys[j]], facts[keys[i]]


def get_num(facts: Mapping[str, Callable[[], bool]], s: str) -> int:
    wires = []
    for f, bit in facts.items():
        if f.startswith(s):
            wires.append((-int(f[1:]), bit()))
    wires.sort()
    return int("".join(["1" if z[1] else "0" for z in wires]), 2)


def main():
    # with open("input.txt", "r") as f:
    #     data = f.read()
    #     print(f"one -> {solution_one(data)}")
    with open("input2.txt", "r") as f:
        data = f.read()
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

    print()
    assert solution_one(data) == 2024
    solution_two(data)
