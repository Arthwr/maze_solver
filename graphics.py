from tkinter import Tk, BOTH, Canvas


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
