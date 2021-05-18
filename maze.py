from typing import Tuple
from enum import Enum


class DIRECTION(int, Enum):
    EAST = -1
    WEST = 1
    NORTH = -2
    SOUTH = 2

    @property
    def invert(self) -> 'DIRECTION':
        return DIRECTION(-self)

    def translate(self, row: int, col: int) -> Tuple[int, int]:
        if self == DIRECTION.EAST:
            return (row, col + 1)

        if self == DIRECTION.NORTH:
            return (row - 1, col)

        if self == DIRECTION.WEST:
            return (row, col - 1)

        if self == DIRECTION.SOUTH:
            return (row + 1, col)

        raise ValueError(f"Could not translate coordinate - {self} unhandled")


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
        other_r, other_c = dir.translate(row, col)
        self[row, col].set_neighbor(dir, self[other_r, other_c])

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
    # Straight bars
    H_FLAT = '─'
    V_FLAT = '│'

    H_LINE = H_FLAT * 4
    H_OPEN = '    '
    V_LINE = V_FLAT * 1
    V_OPEN = ' '

    # Bends
    TOP_LEFT = '┌'
    TOP_MIDDLE = '┬'
    TOP_RIGHT = '┐'

    LEFT_MIDDLE = '├'
    RIGHT_MIDDLE = '┤'

    BOTTOM_LEFT = '└'
    BOTTOM_MIDDLE = '┴'
    BOTTOM_RIGHT = '┘'

    # Middle crosses (for top-left corners)
    bEast =  0b0001
    bNorth = 0b0010
    bWest =  0b0100
    bSouth = 0b1000
    CROSS_MAP = {
        0b0000: ' ',  # Empty intersection
        0b0001: '╶',  # E - East neighbor only
        0b0010: '╵',  # N - North only
        0b0011: '└',  # NE - North + East

        0b0100: '╴',  # W
        0b0101: '─',  # WE
        0b0110: '┘',  # WN
        0b0111: '┴',  # WNE

        0b1000: '╷',  # S
        0b1001: '┌',  # SE
        0b1010: '│',  # SN
        0b1011: '├',  # SNE

        0b1100: '┐',  # SW
        0b1101: '┬',  # SWE
        0b1110: '┤',  # SWN
        0b1111: '┼',  # SWNE
    }

    rows = maze.rows
    for ridx, row in enumerate(rows):
        top_line = ''
        cell_line = ''

        for cidx, cell in enumerate(row):
            # Top-left corner of cell
            # ...first row
            if ridx == 0:
                # ...first col
                if cidx == 0:
                    top_line += TOP_LEFT
                # ...some middle col
                else:
                    if maze[ridx, cidx][DIRECTION.WEST] is None:
                        top_line += TOP_MIDDLE
                    else:
                        top_line += H_FLAT

            # ...some middle row
            else:
                # ...first col
                if cidx == 0:
                    if maze[ridx, cidx][DIRECTION.NORTH] is None:
                        top_line += LEFT_MIDDLE
                    else:
                        top_line += V_FLAT
                # ...some middle col
                else:
                    cross_bit = 0b0000
                    # Check cross's east
                    if maze[ridx, cidx][DIRECTION.NORTH] is None:
                        cross_bit |= bEast
                    # Check cross's north
                    if maze[ridx-1, cidx][DIRECTION.WEST] is None:
                        cross_bit |= bNorth
                    # Check cross's west
                    if maze[ridx, cidx-1][DIRECTION.NORTH] is None:
                        cross_bit |= bWest
                    # Check cross's south
                    if maze[ridx, cidx][DIRECTION.WEST] is None:
                        cross_bit |= bSouth

                    top_line += CROSS_MAP[cross_bit]

            # Top bar
            top_line += '────' if cell.wall(DIRECTION.NORTH) else H_OPEN

            # Cell value + vertical bar
            cell_line += V_LINE if cell.wall(DIRECTION.WEST) else V_OPEN
            cell_line += f'{str_func(cell.value):^4}'

        # Top-right of row
        # ...first row
        if ridx == 0:
            top_line += TOP_RIGHT
        # ...some middle col
        else:
            if maze[ridx, -1][DIRECTION.NORTH] is None:
                top_line += RIGHT_MIDDLE
            else:
                top_line += V_FLAT

        # Right-most vertical bar of row
        cell_line += V_LINE if cell.wall(DIRECTION.EAST) else V_OPEN

        print(top_line)
        print(cell_line)

    bottom_line = ''
    for cidx, cell in enumerate(rows[-1]):
        # Bottom-left of cells in last row
        # ...first col
        if cidx == 0:
            bottom_line += BOTTOM_LEFT
        # ...some middle col
        else:
            if maze[-1, cidx][DIRECTION.WEST] is None:
                bottom_line += BOTTOM_MIDDLE
            else:
                bottom_line += H_FLAT

        # Vertical bars
        bottom_line += H_LINE if cell.wall(DIRECTION.SOUTH) else H_OPEN

    # Bottom-right of last cell in last row
    bottom_line += BOTTOM_RIGHT

    print(bottom_line)


if __name__ == "__main__":
    size = 16
    m = Maze(size, size, lambda r, c: r * 0x10 + c)
    print_maze(m, lambda v: f'{v:02X}')
