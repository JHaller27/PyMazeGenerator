from maze import DIRECTION, Maze


def carve_maze(maze: Maze):
    # Remove top row
    for c in range(maze.width - 1):
        maze.carve(0, c, DIRECTION.EAST)
