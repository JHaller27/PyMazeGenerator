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

        # Link cells with neighbors

        # Link all rows east-to-west
        for r in range(self._height):
            for c in range(self._width - 1):
                self._cells[r][c][DIRECTION.EAST] = self._cells[r][c+1]
                self._cells[r][c+1][DIRECTION.WEST] = self._cells[r][c]

        # Link all columns north-to-south
        for c in range(self._width):
            for r in range(self._height - 1):
                self._cells[r][c][DIRECTION.SOUTH] = self._cells[r+1][c]
                self._cells[r+1][c][DIRECTION.NORTH] = self._cells[r][c]

    def __getitem__(self, *coords):
        row, col = coords

        return self._cells[row][col]

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
    V_LINE = '|'
    BEND = '+'

    H_SEP = f'{BEND}{H_LINE}' * maze.width + BEND
    ROW_FMT = f'{V_LINE}{{:^4}}' * maze.width + V_LINE

    for row in maze.rows:
        print(H_SEP)
        s_row = [str_func(c.value) for c in row]
        print(ROW_FMT.format(*s_row))
    print(H_SEP)


if __name__ == "__main__":
    size = 16
    m = Maze(size, size, lambda r, c: r * 0x10 + c)
    print_maze(m, lambda v: f'{v:02X}')
