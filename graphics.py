from tkinter import Tk, BOTH, Canvas


class Window:
    """Represents the main application window and canvas."""

    def __init__(self, width, height):
        self._root = Tk()
        self._root.title("Maze Solver")
        self._root.protocol("WM_DELETE_WINDOW", self.close)

        self._canvas = Canvas(self._root, bg="white", width=width, height=height)
        self._canvas.pack(fill=BOTH, expand=1)
        self.running = False

    def redraw(self):
        """Refresh the canvas and process events."""
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        """Enter loop until the user closes the window."""
        self.running = True
        while self.running:
            self.redraw()
        print("window closed...")

    def draw_line(self, line, fill_color="black"):
        """Draw a line on the canvas."""
        line.draw(self._canvas, fill_color)

    def close(self):
        """Stop the window loop and close the window."""
        self.running = False


class Point:
    """Represents a 2D point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    """Represents a line between two points."""

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        """Draw the line on the given canvas."""
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Cell:
    """Represents a single cell in the maze grid."""

    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self._x1 = -1  # left
        self._y1 = -1  # bottom
        self._x2 = -1  # right
        self._y2 = -1  # top

        self._win = window

    def _draw_wall(self, x1, y1, x2, y2):
        """Helper method to draw a wall (line) using the window's draw_line()."""
        self._win.draw_line(Line(Point(x1, y1), Point(x2, y2)))

    def draw(self, x1, y1, x2, y2):
        """Draw the cell with walls based on its state."""
        self._x1, self._y1, self._x2, self._y2 = x1, y1, x2, y2

        if self.has_left_wall:
            self._draw_wall(x1, y1, x1, y2)  # left

        if self.has_top_wall:
            self._draw_wall(x1, y2, x2, y2)  # top

        if self.has_right_wall:
            self._draw_wall(x2, y2, x2, y1)  # right

        if self.has_bottom_wall:
            self._draw_wall(x1, y1, x2, y1)  # bottom
