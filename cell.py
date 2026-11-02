from graphics import Line, Point, Window


class Cell:
    def __init__(self, win: Window|None = None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1.0
        self.__x2 = -1.0
        self.__y1 = -1.0
        self.__y2 = -1.0
        self.__win = win
        self.visited = False


    def draw(self, x1: float, y1: float, x2: float, y2: float) -> None:
        if self.__win is None:
            return
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2


        lines = [Line(Point(x1, y1), Point(x1, y2)), Line(Point(x1, y1), Point(x2, y1)), Line(Point(x2, y1), Point(x2, y2)), Line(Point(x1, y2), Point(x2, y2))]
        colors = ["black" if wall else "white" for wall in [self.has_left_wall, self.has_top_wall, self.has_right_wall, self.has_bottom_wall]]
        for line, color in zip(lines, colors):
            self.__win.draw_line(line, color)

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        half_length = abs(self.__x2 - self.__x1) // 2
        x_center = half_length + self.__x1
        y_center = half_length + self.__y1

        half_length2 = abs(to_cell.__x2 - to_cell.__x1) // 2
        x_center2 = half_length2 + to_cell.__x1
        y_center2 = half_length2 + to_cell.__y1

        fill_color = "red"
        if undo:
            fill_color = "gray"

        line = Line(Point(x_center, y_center), Point(x_center2, y_center2))
        if self.__win != None:
            self.__win.draw_line(line, fill_color)

