from cell import Cell
from graphics import Window
import random
import time


class Maze:
    """
    Represents a rectangular maze grid and handles rendering cells on a canvas
    """

    def __init__(
        self,
        x1: float,
        y1: float,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window = None,
        seed: int = None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells: list[list[Cell]] = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self.draw()
        self._break_entrance_and_exit()
        self._break_walls(0, 0)

    def _animate(self) -> None:
        """
        Pause briefly and update the window to animate the drawing process.
        Used to create a visual step-by-step effect while drawing the maze.
        """
        if self._win is None:
            return

        self._win.redraw()
        time.sleep(0.05)

    def _draw_cell(self, row: int, col: int) -> None:
        """
        Draw a single cell at the specified row and column coordinates.
        """
        if self._win is None:
            return

        cell_x1 = self._x1 + self._cell_size_x * col
        cell_y1 = self._y1 + self._cell_size_y * row
        cell_x2 = cell_x1 + self._cell_size_x
        cell_y2 = cell_y1 + self._cell_size_y

        self._cells[row][col].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate()

    def _break_entrance_and_exit(self) -> None:
        """
        Modify and redraw the maze to create an entrance at top left cell and exit at bottom right cell.
        """
        if not self._cells or not self._cells[0]:
            return

        # Top-left entrance
        entrance_row, entrance_col = 0, 0
        entrance_cell = self._cells[entrance_row][entrance_col]
        entrance_cell.has_top_wall = False
        self._draw_cell(entrance_row, entrance_col)

        # Bottom-right exit
        exit_row, exit_col = self._num_rows - 1, self._num_cols - 1
        exit_cell = self._cells[exit_row][exit_col]
        exit_cell.has_bottom_wall = False
        self._draw_cell(len(self._cells) - 1, len(self._cells[0]) - 1)

    def _break_walls(self, start_i: int, start_j: int) -> None:
        """
        Generate a maze by breaking walls between random unvisited neighboring cells in a depth-first manner.
        """
        stack = [(start_i, start_j)]
        self._cells[start_i][start_j].visited = True

        while stack:
            # Peek at current cell
            i, j = stack[-1]
            current_cell = self._cells[i][j]

            # Gather all unvisited neighboring cells and their directions
            neightbours = []
            if i > 0 and not self._cells[i - 1][j].visited:
                neightbours.append(("top", i - 1, j))
            if j < self._num_cols - 1 and not self._cells[i][j + 1].visited:
                neightbours.append(("right", i, j + 1))
            if i < self._num_rows - 1 and not self._cells[i + 1][j].visited:
                neightbours.append(("bottom", i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                neightbours.append(("left", i, j - 1))

            if neightbours:
                # Choose random unvisited neighbore and remove wall between them
                direction, ni, nj = random.choice(neightbours)
                next_cell = self._cells[ni][nj]
                next_cell.visited = True

                if direction == "top":
                    current_cell.has_top_wall = False
                    next_cell.has_bottom_wall = False
                elif direction == "right":
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False
                elif direction == "bottom":
                    current_cell.has_bottom_wall = False
                    next_cell.has_top_wall = False
                elif direction == "left":
                    current_cell.has_left_wall = False
                    next_cell.has_right_wall = False

                # Push newly visited cell to the stack
                stack.append((ni, nj))

                # Redraw both cells to update GUI
                self._draw_cell(i, j)
                self._draw_cell(ni, nj)
            else:
                # No valid neighbors -> backtrack
                stack.pop()

    def _create_cells(self) -> None:
        """
        Initialize the grid of Cell objects.
        """
        for _row in range(self._num_rows):
            row_cells = []
            for _col in range(self._num_cols):
                row_cells.append(Cell(self._win))
            self._cells.append(row_cells)

    def draw(self) -> None:
        """
        Draw the grid of Cell objects on canvas.
        """
        for row in range(self._num_rows):
            for col in range(self._num_cols):
                self._draw_cell(row, col)
