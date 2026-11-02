import time
import random

from cell import Cell
from graphics import Window


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window|None = None,
        seed: str | None = None,
        skip_break: bool = False
    ) -> None:
        self.__cells: list[list[Cell]] = []
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win

        self.__create_cells()
        self.__break_entrance_and_exit()
        if not skip_break:
            self.__break_walls_r(0,0)
        self.__reset_cells_visited()

        if seed != None:
            random.seed(seed)

    def __create_cells(self) -> None:
        for i in range(self.__num_cols):
            col_cells: list[Cell] = []
            for j in range(self.__num_rows):
                col_cells.append(Cell(self.__win))
            self.__cells.append(col_cells)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i: int, j: int) -> None:
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self) -> None:
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.005)

    def __break_entrance_and_exit(self) -> None:
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        
        end_row = self.__num_rows - 1
        end_col = self.__num_cols - 1
        self.__cells[end_col][end_row].has_bottom_wall = False
        self.__draw_cell(end_col, end_row)

    def get_neighbours(self, i, j) -> dict[str, list[int, int]]:
        neighbours = {}
        if i > 0:
            neighbours["w"] = [int(i-1), int(j)]
        if j > 0:
            neighbours["n"] = [int(i), int(j-1)]
        if i < self.__num_cols - 1:
            neighbours["e"] = [int(i+1), int(j)]
        if j < self.__num_rows - 1:
            neighbours["s"] = [int(i), int(j+1)]

        return neighbours

    def __break_walls_r(self, i: int, j: int) -> None:
        cur_cell = self.__cells[i][j]
        cur_cell.visited = True
        while True:
            neighbours = self.get_neighbours(i, j)
            to_visit = []
            for neighbour_direction, neighbour_point in neighbours.items():
                neighbour_cell = self.__cells[neighbour_point[0]][neighbour_point[1]]
                if neighbour_cell.visited:
                    continue
                to_visit.append({neighbour_direction: neighbour_point})

            if len(to_visit) == 0:
                self.__draw_cell(i, j)
                return

            rand_direction = random.randrange(0, len(to_visit), 1)
            rand_direction, rand_neighbour = list(to_visit[rand_direction].items())[0]
            self.__break_walls_r(rand_neighbour[0], rand_neighbour[1])
            rand_neighbour = self.__cells[rand_neighbour[0]][rand_neighbour[1]]

            if rand_direction == "n":
                cur_cell.has_top_wall = False
                rand_neighbour.has_bottom_wall = False
            if rand_direction == "e":
                cur_cell.has_right_wall = False
                rand_neighbour.has_left_wall = False
            if rand_direction == "s":
                cur_cell.has_bottom_wall = False
                rand_neighbour.has_top_wall = False
            if rand_direction == "w":
                cur_cell.has_left_wall = False
                rand_neighbour.has_right_wall = False

    def __reset_cells_visited(self) -> None:
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__cells[i][j].visited = False

    def solve(self) -> bool:
        return self.__solve_r(0, 0)

    def __solve_r(self, i: int, j: int) -> bool:
        cur_cell = self.__cells[i][j]
        cur_cell.visited = True
        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        neighbours = self.get_neighbours(i, j)
        for neighbour_direction, neighbour_point in neighbours.items():
            neighbour_cell = self.__cells[neighbour_point[0]][neighbour_point[1]]
            if neighbour_cell.visited:
                continue
            if neighbour_direction == "n" and cur_cell.has_top_wall:
                continue
            if neighbour_direction == "e" and cur_cell.has_right_wall:
                continue
            if neighbour_direction == "s" and cur_cell.has_bottom_wall:
                continue
            if neighbour_direction == "w" and cur_cell.has_left_wall:
                continue

            cur_cell.draw_move(neighbour_cell)
            is_end = self.__solve_r(neighbour_point[0], neighbour_point[1])
            if is_end:
                return True
            else:
                cur_cell.draw_move(neighbour_cell, undo=True)

        return False
