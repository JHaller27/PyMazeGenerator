import random

from sidewinder import carve_maze
from dijkstra import map_maze
from maze import Maze, maze_to_str

import typer


# Pretty-print maze-cell value as 2-digit hex
def print_hex(val):
    return f'{val:02X}'


def main(size: int, seed: int = None, distances: bool = False):
    # Set+print random seed
    if seed is None:
        seed = random.randrange(100000)
    random.seed(seed)
    print(f'{seed=}')

    # Create Maze object w/ custom cell values
    maze = Maze(size, size, lambda r, c: r * 0x10 + c)

    # Carve paths through the maze, and pretty-print result
    carve_maze(maze)

    # Find the distance to all cells
    if distances:
        map_maze(maze)
        m_str = maze_to_str(maze, print_hex)

    else:
        m_str = maze_to_str(maze, lambda v: '')

    print(m_str)


if __name__ == "__main__":
    typer.run(main)
