from typing import Any


def parse_data(data: str) -> tuple[int, int, int, list[int]]:
    lines = data.strip().splitlines()
    A = int(lines[0][12:])
    B = int(lines[1][12:])
    C = int(lines[2][12:])
    program = [int(x) for x in lines[4][9:].strip().split(",")]
    return A, B, C, program


def solution_one(data: str) -> Any:
    A, B, C, program = parse_data(data)

    out = []

    def get_combo(x: int) -> int:
        match x:
            case 0 | 1 | 2 | 3 as d:
                return d
            case 4:
                return A
            case 5:
                return B
            case 6:
                return C
        raise ValueError("Invalid Program")

    i = 0
    while i < len(program):
        match program[i], program[i + 1]:
            case 0, x:
                A = A // (2 ** get_combo(x))
            case 1, x:
                B = B ^ x
            case 2, x:
                B = get_combo(x) % 8
            case 3, x:
                if A != 0:
                    i = x
                    continue
            case 4, x:
                B = B ^ C
            case 5, x:
                out.append(str(get_combo(x) % 8))
            case 6, x:
                B = A // (2 ** get_combo(x))
            case 7, x:
                C = A // (2 ** get_combo(x))
        i += 2
    return ",".join(out)


def solution_two_runner(A: int, B: int, C: int, program: list[int], expected: list[int]) -> Any:
    out = []

    def get_combo(x: int) -> int:
        match x:
            case 0 | 1 | 2 | 3 as d:
                return d
            case 4:
                return A
            case 5:
                return B
            case 6:
                return C
        raise ValueError("Invalid Program")

    i = 0
    oc = 0
    while i < len(program):
        match program[i], program[i + 1]:
            case 0, x:
                A = A // (2 ** get_combo(x))
            case 1, x:
                B = B ^ x
            case 2, x:
                B = get_combo(x) % 8
            case 3, x:
                if A != 0:
                    i = x
                    continue
            case 4, x:
                B = B ^ C
            case 5, x:
                o = get_combo(x) % 8
                if expected[oc] != o:
                    return False
                out.append(o)
                oc += 1
            case 6, x:
                B = A // (2 ** get_combo(x))
            case 7, x:
                C = A // (2 ** get_combo(x))
        i += 2
    return expected == out


def solution_two(data: str) -> Any:
    _, B, C, program = parse_data(data)
    f = 123405769773837
    c = 164541026365117
    A = c
    m = A
    while A > f:
        if solution_two_runner(A, B, C, program, program):
            m = min(A, m)
        A -= 256 * (256 * 8 * 16)
    return m


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""
    assert solution_one(data) == "4,6,3,5,6,3,5,2,1,0"
