from tkinter import Tk, BOTH, Canvas
import time


class Window:
    """Represents the main application window and canvas."""

    def __init__(self, width: int, height: int):
        self._root = Tk()
        self._root.title("Maze Solver")
        self._root.protocol("WM_DELETE_WINDOW", self.close)

        self._canvas = Canvas(self._root, bg="white", width=width, height=height)
        self._canvas.pack(fill=BOTH, expand=1)
        self._running: bool = False

    def redraw(self) -> None:
        """Refresh the canvas and process events."""
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self) -> None:
        """Enter loop until the user closes the window."""
        self._running = True
        while self._running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line: "Line", fill_color: str = "black") -> None:
        """Draw a line on the canvas."""
        line.draw(self._canvas, fill_color)

    def close(self) -> None:
        """Stop the window loop and close the window."""
        self._running = False


class Point:
    """Represents a 2D point."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Line:
    """Represents a line between two points."""

    def __init__(self, p1: "Point", p2: "Point"):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: "Canvas", fill_color: str = "black") -> None:
        """Draw the line on the given canvas."""
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Cell:
    """Represents a single cell in the maze grid."""

    def __init__(self, window: "Window" = None):
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True

        self._x1: float = -1  # left
        self._y1: float = -1  # bottom
        self._x2: float = -1  # right
        self._y2: float = -1  # top

        self._win = window

    def __repr__(self) -> str:
        walls = "".join(
            [
                "L" if self.has_left_wall else "_",
                "T" if self.has_top_wall else "_",
                "R" if self.has_right_wall else "_",
                "B" if self.has_bottom_wall else "_",
            ]
        )

        return f"Cell(walls={walls})"

    def _center(self) -> tuple[float, float]:
        """Return (cx, cy) center of this cell in canvas coordinates."""
        cx = (self._x1 + self._x2) / 2
        cy = (self._y1 + self._y2) / 2
        return cx, cy

    def _draw_wall(
        self, x1: float, y1: float, x2: float, y2: float, fill_color: str = "black"
    ) -> None:
        """Helper method to draw a wall (line) using the window's draw_line()."""
        if self._win == None:
            return

        self._win.draw_line(Line(Point(x1, y1), Point(x2, y2)), fill_color)

    def draw(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """Draw the cell with walls based on its state."""
        self._x1, self._y1, self._x2, self._y2 = x1, y1, x2, y2

        if self.has_left_wall:
            self._draw_wall(x1, y1, x1, y2)
        else:
            self._draw_wall(x1, y1, x1, y2, "white")

        if self.has_top_wall:
            self._draw_wall(x1, y1, x2, y1)
        else:
            self._draw_wall(x1, y1, x2, y1, "white")

        if self.has_right_wall:
            self._draw_wall(x2, y1, x2, y2)
        else:
            self._draw_wall(x2, y1, x2, y2, "white")

        if self.has_bottom_wall:
            self._draw_wall(x1, y2, x2, y2)
        else:
            self._draw_wall(x1, y2, x2, y2, "white")

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        """
        Draw a move from this cell to the neighboring cell.
        Draw center-to-center so the path stays inside the cells.
        """
        if self._win is None:
            return

        x_center, y_center = self._center()
        x_center2, y_center2 = to_cell._center()

        fill_color = "gray" if undo else "red"

        self._win.draw_line(
            Line(
                Point(x_center, y_center),
                Point(x_center2, y_center2),
            ),
            fill_color,
        )


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
        win: "Window" = None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells: list[list[Cell]] = []

        self._create_cells()
        self.draw()
        self._break_entrance_and_exit()

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

        entrance_row, entrance_col = 0, 0
        entrance_cell = self._cells[entrance_row][entrance_col]
        entrance_cell.has_top_wall = False
        self._draw_cell(entrance_row, entrance_col)

        exit_row, exit_col = self._num_rows - 1, self._num_cols - 1
        exit_cell = self._cells[exit_row][exit_col]
        exit_cell.has_bottom_wall = False
        self._draw_cell(len(self._cells) - 1, len(self._cells[0]) - 1)

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
