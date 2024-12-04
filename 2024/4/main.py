from typing import Any

directions = [(0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (1, 1), (-1, -1), (1, -1)]


def dfs_xmas(grid: list[list[str]], i: int, j: int, di: int, dj: int, d: int) -> int:
    if not (0 <= i < len(grid) and 0 <= j < len(grid[i])):
        return 0
    match d, grid[i][j]:
        case (0, "X") | (1, "M") | (2, "A"):
            return dfs_xmas(grid, i + di, j + dj, di, dj, d + 1)
        case 3, "S":
            return 1
        case _:
            return 0


def parse_data(data: str) -> list[list[str]]:
    return data.splitlines()


def solution_one(data: str) -> Any:
    grid = parse_data(data)
    res = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                res += sum(dfs_xmas(grid, i, j, di, dj, 0) for di, dj in directions)
    return res


def solution_two(data: str) -> Any:
    grid = parse_data(data)
    res = 0
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] == "A":
                if [
                    grid[i - 1][j - 1],
                    grid[i + 1][j + 1],
                ] in [["M", "S"], ["S", "M"]] and [
                    grid[i + 1][j - 1],
                    grid[i - 1][j + 1],
                ] in [["M", "S"], ["S", "M"]]:
                    res += 1

    return res


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
    assert solution_one(data) == 18
    assert solution_two(data) == 9
