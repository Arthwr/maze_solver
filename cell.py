from graphics import Line, Point
from graphics import Window


class Cell:
    """Represents a single cell in the maze grid."""

    def __init__(self, window: Window = None):
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True

        self.visited = False

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
