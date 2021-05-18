import random

from sidewinder import carve_maze
from maze import Maze, print_maze


def print_hex(val):
    return f'{val:02X}'


def main(size: int, seed: int = None):
    if seed is None:
        seed = random.randrange(100000)
    random.seed(seed)

    print(f'{seed=}')

    maze = Maze(size, size, lambda r, c: r * 0x10 + c)

    print_maze(maze, print_hex)
    print()

    carve_maze(maze)

    print_maze(maze, print_hex)


if __name__ == "__main__":
    main(16)
