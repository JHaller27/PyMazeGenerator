from maze import DIRECTION, Maze


def map_maze(maze: Maze):
    # Clear all cell values
    for c in maze.cells:
        c.value = None

    # Queue containing cells: (row, col, distance)
    queue = [(0, 0, 0)]

    # While there are still cells in the queue...
    while len(queue) > 0:
        ridx, cidx, dist = queue.pop(0)
        cell = maze[ridx, cidx]

        # Set this cell's value to its distance
        cell.value = dist

        for d in DIRECTION:
            neighbor = cell[d]

            # If this cell has a neighbor in this direction,
            #   and that cell does not yet have a value (ie it's unvisited),
            #   add that neighbor to the queue
            if neighbor is not None and neighbor.value is None:
                n_ridx, n_cidx = d.translate(ridx, cidx)
                queue.append((n_ridx, n_cidx, dist + 1))
