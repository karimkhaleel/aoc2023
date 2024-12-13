import dataclasses
from typing import Any


@dataclasses.dataclass
class Coord:
    X: int
    Y: int


@dataclasses.dataclass
class Game:
    A: Coord
    B: Coord
    Prize: Coord


def parse_data(data: str) -> list[Game]:
    games: list[Game] = []
    lines = data.strip().splitlines()
    i = 0
    while i < len(lines):
        if lines[i] == "":
            i += 1
            continue
        comma = lines[i].find(",")
        ax = int(lines[i][12:comma])
        ay = int(lines[i][comma + 4 :])
        comma = lines[i + 1].find(",")
        bx = int(lines[i + 1][12:comma])
        by = int(lines[i + 1][comma + 4 :])
        comma = lines[i + 2].find(",")
        px = int(lines[i + 2][9:comma])
        py = int(lines[i + 2][comma + 4 :])
        games.append(Game(Coord(ax, ay), Coord(bx, by), Coord(px, py)))
        i += 3

    return games


def play_game(game: Game) -> int:
    b = ((game.Prize.X * game.A.Y) - (game.A.X * game.Prize.Y)) // (
        (game.B.X * game.A.Y) - (game.A.X * game.B.Y)
    )
    a = (game.Prize.Y - game.B.Y * b) // game.A.Y
    print(
        a,
        b,
        (game.A.X * a + game.B.X * b),
        (game.A.Y * a + game.B.Y * b),
        game.Prize.X,
        game.Prize.Y,
    )
    if (
        game.A.X * a + game.B.X * b == game.Prize.X
        and game.A.Y * a + game.B.Y * b == game.Prize.Y
    ):
        return a * 3 + b
    return 0


def play_game_two(game: Game) -> int:
    game.Prize.X += 10000000000000
    game.Prize.Y += 10000000000000
    b = ((game.Prize.X * game.A.Y) - (game.A.X * game.Prize.Y)) // (
        (game.B.X * game.A.Y) - (game.A.X * game.B.Y)
    )
    a = (game.Prize.Y - game.B.Y * b) // game.A.Y
    if (
        game.A.X * a + game.B.X * b == game.Prize.X
        and game.A.Y * a + game.B.Y * b == game.Prize.Y
    ):
        return a * 3 + b
    return 0


def solution_one(data: str) -> Any:
    print()
    games = parse_data(data)
    res = 0
    for game in games:
        res += play_game(game)
    return res


def solution_two(data: str) -> Any:
    games = parse_data(data)
    res = 0
    for game in games:
        res += play_game_two(game)
    return res


def main():
    with open("input.txt", "r") as f:
        data = f.read()
        print(f"one -> {solution_one(data)}")
        print(f"two -> {solution_two(data)}")


if __name__ == "__main__":
    main()


def test_solution() -> None:
    data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    assert solution_one(data) == 480
    assert solution_two(data) == 875318608908
