from graphics import Window, Line, Point, Cell


def main():
    win = Window(800, 600)

    c = Cell(win)
    c.has_right_wall = False
    c.draw(100, 100, 200, 200)

    c2 = Cell(win)
    c2.has_left_wall = False
    c2.draw(200, 100, 300, 200)

    c.draw_move(c2)

    win.wait_for_close()


main()
