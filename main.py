import random

from sidewinder import carve_maze
from maze import Maze, print_maze


# Pretty-print maze-cell value as 2-digit hex
def print_hex(val):
    return f'{val:02X}'


def main(size: int, seed: int = None):
    # Set+print random seed
    if seed is None:
        seed = random.randrange(100000)
    random.seed(seed)
    print(f'{seed=}')

    # Create Maze object w/ custom cell values
    maze = Maze(size, size, lambda r, c: r * 0x10 + c)

    # Carve paths through the maze, and pretty-print result
    carve_maze(maze)
    print_maze(maze, print_hex)


if __name__ == "__main__":
    main(16)
