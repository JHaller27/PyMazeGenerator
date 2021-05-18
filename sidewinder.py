from maze import DIRECTION, Maze
from itertools import islice
from random import choice


def carve_maze(maze: Maze):
    # Remove top row
    for c in range(maze.width - 1):
        maze.carve(0, c, DIRECTION.EAST)

    # Carve each row, skipping the first row
    for ridx, row in islice(enumerate(maze.rows), 1, None):
        # Initialize an empty set of "visited" cells in this row
        run_set = set()

        for cidx, cell in enumerate(row):
            # Add each cell to the run set
            run_set.add((ridx, cidx))

            # Randomly choose whether or not to carve east

            # Carve east if possible
            if cidx < (maze.width - 1) and choice([True, False]):
                maze.carve(ridx, cidx, DIRECTION.EAST)

            # Don't carve east
            else:
                # Carve north (to connect this section)
                carve_r, carve_c = choice(list(run_set))
                maze.carve(carve_r, carve_c, DIRECTION.NORTH)

                # Empty run_set
                run_set = set()
