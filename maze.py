from enum import Enum


class DIRECTION(int, Enum):
    EAST = -1
    WEST = 1
    NORTH = -2
    SOUTH = 2

    @property
    def invert(self) -> 'DIRECTION':
        return DIRECTION(-self)


class Cell:
    def __init__(self, val = None) -> None:
        self._value = val
        self._neighbors = {d: None for d in DIRECTION}

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    def wall(self, dir: DIRECTION) -> bool:
        return self._neighbors[dir] is None

    def __getitem__(self, dir: DIRECTION) -> 'Cell':
        return self._neighbors[dir]

    def __setitem__(self, dir: DIRECTION, neighbor: 'Cell'):
        self._neighbors[dir] = neighbor

    def __str__(self) -> str:
        neigh_list = []
        for d in DIRECTION:
            n = self[d]
            v = 'None' if n is None else str(n.value)
            neigh_list.append(f'{d.name[0].upper()}={v}')
        neighbors = ', '.join(neigh_list)

        return f'<{self.value} ({neighbors})>'

    def set_neighbor(self, dir: DIRECTION, other: 'Cell'):
        self[dir] = other
        other[dir.invert] = self


def default_fill_func(row: int, col: int):
    return str((row, col))


class Maze:
    def __init__(self, height: int, width: int, fill_func = None):
        assert height >= 1
        assert width >= 1

        self._height = height
        self._width = width

        if fill_func is None:
            fill_func = default_fill_func

        self._cells = [[Cell(fill_func(r, c)) for c in range(height)] for r in range(width)]

    def __getitem__(self, coords):
        if len(coords) == 1:
            row, = coords
            return self._cells[row]

        row, col = coords
        return self._cells[row][col]

    def carve(self, row: int, col: int, dir: DIRECTION):
        if dir == DIRECTION.EAST:
            self[row, col].set_neighbor(DIRECTION.EAST, self[row, col + 1])

        elif dir == DIRECTION.NORTH:
            self[row, col].set_neighbor(DIRECTION.NORTH, self[row - 1, col])

        elif dir == DIRECTION.WEST:
            self[row, col].set_neighbor(DIRECTION.WEST, self[row, col - 1])

        elif dir == DIRECTION.SOUTH:
            self[row, col].set_neighbor(DIRECTION.SOUTH, self[row + 1, col])

        else:
            raise ValueError(f"Direction {dir} not recognized for Maze.carve")

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def rows(self):
        return list(self._cells)

    @property
    def cells(self):
        l = []
        for row in self._cells:
            for cell in row:
                l.append(cell)

        return l


def print_maze(maze: Maze, str_func = str):
    H_LINE = '----'
    H_OPEN = '    '
    V_LINE = '|'
    V_OPEN = ' '
    BEND = '+'

    rows = maze.rows
    for row in rows:
        top_line = ''
        cell_line = ''

        for cell in row:
            top_line += BEND
            top_line += H_LINE if cell.wall(DIRECTION.NORTH) else H_OPEN

            cell_line += V_LINE if cell.wall(DIRECTION.WEST) else V_OPEN
            cell_line += f'{str_func(cell.value):^4}'

        top_line += BEND
        cell_line += V_LINE if cell.wall(DIRECTION.EAST) else V_OPEN

        print(top_line)
        print(cell_line)

    bottom_line = BEND
    for cell in rows[-1]:
        bottom_line += H_LINE if cell.wall(DIRECTION.SOUTH) else H_OPEN
        bottom_line += BEND

    print(bottom_line)


if __name__ == "__main__":
    size = 16
    m = Maze(size, size, lambda r, c: r * 0x10 + c)
    print_maze(m, lambda v: f'{v:02X}')
