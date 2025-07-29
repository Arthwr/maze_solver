from graphics import Window, Line, Point


def main():
    win = Window(800, 600)
    line = Line(Point(100, 100), Point(100, 300))
    lin2 = Line(Point(100, 100), Point(300, 100))
    win.draw_line(line, "black")
    win.draw_line(lin2, "red")
    win.wait_for_close()


main()
