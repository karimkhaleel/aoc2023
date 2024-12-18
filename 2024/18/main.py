import heapq


def print_grid(grid: list[list[bool]]) -> None:
    for r in grid:
        print("".join(["." if x else "#" for x in r]))


def parse_data_one(data: str, dim: int, n_bytes: int) -> list[list[bool]]:
    dim += 1
    grid = [[True for _ in range(dim)] for _ in range(dim)]
    for line in data.strip().splitlines()[:n_bytes]:
        sx, sy = line.split(",")
        x, y = int(sx.strip()), int(sy.strip())
        grid[y][x] = False
    return grid


dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def solution_one(data: str, dim: int, n_bytes: int) -> int:
    grid = parse_data_one(data, dim, n_bytes)
    q = [(0, 0, 0)]
    visited = set()
    while q:
        d, x, y = heapq.heappop(q)
        if (x, y) == (dim, dim):
            return d
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx, ny) not in visited and grid[ny][nx]:
                heapq.heappush(q, (d + 1, nx, ny))
                visited.add((nx, ny))
    return dim * dim


def run_maze(data: str, dim: int, n_bytes: int) -> bool:
    grid = parse_data_one(data, dim, n_bytes)
    q = [(0, 0, 0)]
    visited = set()
    while q:
        d, x, y = heapq.heappop(q)
        if (x, y) == (dim, dim):
            return True
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx, ny) not in visited and grid[ny][nx]:
                heapq.heappush(q, (d + 1, nx, ny))
                visited.add((nx, ny))
    return False


def solution_two(data: str, dim: int) -> str:
    lp, rp = 1, len(data.strip().splitlines())
    while lp < rp:
        m = lp + ((rp - lp) // 2)

        can_pass = run_maze(data, dim, m)
        if can_pass:
            lp = m + 1
        else:
            rp = m

    return data.strip().splitlines()[lp - 1]


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data, 70, 1024)}")
        print(f"two -> {solution_two(data, 70)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

    print()
    assert solution_one(data, 6, 12) == 22
    assert solution_two(data, 6) == "6,1"
