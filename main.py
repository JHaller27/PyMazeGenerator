from sidewinder import carve_maze
from maze import Maze, print_maze


def main(size: int):
    maze = Maze(size, size, lambda r, c: r * 0x10 + c)
    print_maze(maze, lambda v: f'{v:02X}')
    print()
    carve_maze(maze)
    print_maze(maze, lambda v: f'{v:02X}')


if __name__ == "__main__":
    main(16)
