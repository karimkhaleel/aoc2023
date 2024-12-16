import heapq
import math
from copy import copy
from typing import Any


def parse_data(data: str) -> list[list[str]]:
    grid = []
    for r in data.strip().splitlines():
        grid.append(list(r))
    return grid


def find(grid: list[list[str]], letter: str) -> tuple[int, int]:
    for j, r in enumerate(grid):
        for i, c in enumerate(r):
            if c == letter:
                return i, j
    return -1, -1


def print_maze(maze: list[list[str]], x: int, y: int, dir: str) -> None:
    for j, r in enumerate(maze):
        rr = []
        for i, c in enumerate(r):
            if (i, j) == (x, y):
                rr.append(dir)
            else:
                rr.append(c)
        print("".join(rr))


def solution_one(data: str) -> Any:
    print()
    maze = parse_data(data)
    S = find(maze, "S")
    E = find(maze, "E")
    q: list[tuple[int, int, int, str]] = [(0, S[0], S[1], ">")]
    best_score = math.inf
    scores = [[{d: math.inf for d in ["^", "v", ">", "<"]} for _ in range(len(maze[0]))] for _ in range(len(maze))]
    while q:
        score, x, y, dir = heapq.heappop(q)
        if (x, y) == (E[0], E[1]):
            best_score = min(best_score, score)
        match dir:
            case "^":
                if y > 0 and maze[y - 1][x] != "#" and scores[y - 1][x]["^"] > score + 1:
                    scores[y - 1][x]["^"] = score + 1
                    heapq.heappush(q, (score + 1, x, y - 1, "^"))
                if x > 0 and maze[y][x - 1] != "#" and scores[y][x - 1]["<"] > score + 1001:
                    scores[y][x - 1]["<"] = score + 1001
                    heapq.heappush(q, (score + 1001, x - 1, y, "<"))
                if x < len(maze[y]) - 1 and maze[y][x + 1] != "#" and scores[y][x + 1][">"] > score + 1001:
                    scores[y][x + 1][">"] = score + 1001
                    heapq.heappush(q, (score + 1001, x + 1, y, ">"))
            case "v":
                if y < len(maze) - 1 and maze[y + 1][x] != "#" and scores[y + 1][x]["v"] > score + 1:
                    scores[y + 1][x]["v"] = score + 1
                    heapq.heappush(q, (score + 1, x, y + 1, "v"))
                if x > 0 and maze[y][x - 1] != "#" and scores[y][x - 1]["<"] > score + 1001:
                    scores[y][x - 1]["<"] = score + 1001
                    heapq.heappush(q, (score + 1001, x - 1, y, "<"))
                if x < len(maze[y]) - 1 and maze[y][x + 1] != "#" and scores[y][x + 1][">"] > score + 1001:
                    scores[y][x + 1][">"] = score + 1001
                    heapq.heappush(q, (score + 1001, x + 1, y, ">"))
            case ">":
                if x < len(maze[y]) - 1 and maze[y][x + 1] != "#" and scores[y][x + 1][">"] > score + 1:
                    scores[y][x + 1][">"] = score + 1
                    heapq.heappush(q, (score + 1, x + 1, y, ">"))
                if y > 0 and maze[y - 1][x] != "#" and scores[y - 1][x][">"] > score + 1001:
                    scores[y - 1][x][">"] = score + 1001
                    heapq.heappush(q, (score + 1001, x, y - 1, "^"))
                if y < len(maze[y]) - 1 and maze[y + 1][x] != "#" and scores[y + 1][x]["v"] > score + 1001:
                    scores[y + 1][x]["v"] = score + 1001
                    heapq.heappush(q, (score + 1001, x, y + 1, "v"))
            case "<":
                if x > 0 and maze[y][x - 1] != "#" and scores[y][x - 1]["<"] > score + 1:
                    scores[y][x - 1]["<"] = score + 1
                    heapq.heappush(q, (score + 1, x - 1, y, "<"))
                if y > 0 and maze[y - 1][x] != "#" and scores[y - 1][x]["^"] > score + 1001:
                    scores[y - 1][x]["^"] = score + 1001
                    heapq.heappush(q, (score + 1001, x, y - 1, "^"))
                if y < len(maze[y]) - 1 and maze[y + 1][x] != "#" and scores[y + 1][x]["v"] > score + 1001:
                    scores[y + 1][x]["v"] = score + 1001
                    heapq.heappush(q, (score + 1001, x, y + 1, "v"))
    return best_score


def solution_two(data: str) -> Any:
    s1 = solution_one(data)
    print()
    maze = parse_data(data)
    S = find(maze, "S")
    E = find(maze, "E")
    q: list[tuple[int, int, int, str]] = [(0, S[0], S[1], ">", [S])]
    best_score = math.inf
    scores = [[{d: math.inf for d in ["^", "v", ">", "<"]} for _ in range(len(maze[0]))] for _ in range(len(maze))]
    best_paths = set([S, E])
    while q:
        score, x, y, dir, path = heapq.heappop(q)
        if (x, y) == (E[0], E[1]):
            best_score = min(best_score, score)
            if score == s1:
                for p in path:
                    best_paths.add(p)
        match dir:
            case "^":
                if y > 0 and maze[y - 1][x] != "#" and scores[y - 1][x]["^"] >= score + 1:
                    scores[y - 1][x]["^"] = score + 1
                    p = copy(path)
                    p.append((x, y - 1))
                    heapq.heappush(q, (score + 1, x, y - 1, "^", p))
                if x > 0 and maze[y][x - 1] != "#" and scores[y][x - 1]["<"] >= score + 1001:
                    scores[y][x - 1]["<"] = score + 1001
                    p = copy(path)
                    p.append((x - 1, y))
                    heapq.heappush(q, (score + 1001, x - 1, y, "<", p))
                if x < len(maze[y]) - 1 and maze[y][x + 1] != "#" and scores[y][x + 1][">"] >= score + 1001:
                    scores[y][x + 1][">"] = score + 1001
                    p = copy(path)
                    p.append((x + 1, y))
                    heapq.heappush(q, (score + 1001, x + 1, y, ">", p))
            case "v":
                if y < len(maze) - 1 and maze[y + 1][x] != "#" and scores[y + 1][x]["v"] >= score + 1:
                    scores[y + 1][x]["v"] = score + 1
                    p = copy(path)
                    p.append((x, y + 1))
                    heapq.heappush(q, (score + 1, x, y + 1, "v", p))
                if x > 0 and maze[y][x - 1] != "#" and scores[y][x - 1]["<"] >= score + 1001:
                    scores[y][x - 1]["<"] = score + 1001
                    p = copy(path)
                    p.append((x - 1, y))
                    heapq.heappush(q, (score + 1001, x - 1, y, "<", p))
                if x < len(maze[y]) - 1 and maze[y][x + 1] != "#" and scores[y][x + 1][">"] >= score + 1001:
                    scores[y][x + 1][">"] = score + 1001
                    p = copy(path)
                    p.append((x + 1, y))
                    heapq.heappush(q, (score + 1001, x + 1, y, ">", p))
            case ">":
                if x < len(maze[y]) - 1 and maze[y][x + 1] != "#" and scores[y][x + 1][">"] >= score + 1:
                    scores[y][x + 1][">"] = score + 1
                    p = copy(path)
                    p.append((x + 1, y))
                    heapq.heappush(q, (score + 1, x + 1, y, ">", p))
                if y > 0 and maze[y - 1][x] != "#" and scores[y - 1][x][">"] >= score + 1001:
                    scores[y - 1][x][">"] = score + 1001
                    p = copy(path)
                    p.append((x, y - 1))
                    heapq.heappush(q, (score + 1001, x, y - 1, "^", p))
                if y < len(maze[y]) - 1 and maze[y + 1][x] != "#" and scores[y + 1][x]["v"] >= score + 1001:
                    scores[y + 1][x]["v"] = score + 1001
                    p = copy(path)
                    p.append((x, y + 1))
                    heapq.heappush(q, (score + 1001, x, y + 1, "v", p))
            case "<":
                if x > 0 and maze[y][x - 1] != "#" and scores[y][x - 1]["<"] >= score + 1:
                    scores[y][x - 1]["<"] = score + 1
                    p = copy(path)
                    p.append((x - 1, y))
                    heapq.heappush(q, (score + 1, x - 1, y, "<", p))
                if y > 0 and maze[y - 1][x] != "#" and scores[y - 1][x]["^"] >= score + 1001:
                    scores[y - 1][x]["^"] = score + 1001
                    p = copy(path)
                    p.append((x, y - 1))
                    heapq.heappush(q, (score + 1001, x, y - 1, "^", p))
                if y < len(maze[y]) - 1 and maze[y + 1][x] != "#" and scores[y + 1][x]["v"] >= score + 1001:
                    scores[y + 1][x]["v"] = score + 1001
                    p = copy(path)
                    p.append((x, y + 1))
                    heapq.heappush(q, (score + 1001, x, y + 1, "v", p))
    return len(best_paths)


def main():
    #     data = """
    # ###############
    # #.......#....E#
    # #.#.###.#.###.#
    # #.....#.#...#.#
    # #.###.#####.#.#
    # #.#.#.......#.#
    # #.#.#####.###.#
    # #...........#.#
    # ###.#.#####.#.#
    # #...#.....#.#.#
    # #.#.#.###.#.#.#
    # #.....#...#.#.#
    # #.###.#.#.#.#.#
    # #S..#.....#...#
    # ###############
    #     """
    #     assert solution_one(data) == 7036
    #     assert solution_two(data) == 45
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
    """
    assert solution_one(data) == 7036
    assert solution_two(data) == 45
