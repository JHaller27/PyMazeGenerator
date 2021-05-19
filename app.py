import random

from starlette.responses import HTMLResponse

from sidewinder import carve_maze
from dijkstra import map_maze
from maze import Maze, maze_to_str
from main import print_hex

from fastapi import FastAPI


app = FastAPI(name="Maze Generator")



@app.get('/sidewinder/{size}', response_class=HTMLResponse)
def sidewinder(size: int, seed: int = None, distances: bool = False):
    m_str = ""

    # Set+print random seed
    if seed is None:
        seed = random.randrange(100000)
    random.seed(seed)

    # Create Maze object w/ custom cell values
    maze = Maze(size, size, lambda r, c: r * 0x10 + c)

    # Carve paths through the maze, and pretty-print result
    carve_maze(maze)

    # Find the distance to all cells
    if distances:
        map_maze(maze)
        m_str += maze_to_str(maze, print_hex)

    else:
        m_str += maze_to_str(maze, lambda v: '')

    m_str += f'{seed=}'

    return f'<pre style="font-family: Consolas">\n{m_str}</pre>'
