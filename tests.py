import unittest

from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )
    def test_maze_create_numerous_cells(self):
        num_cols = 2**11
        num_rows = 2**11
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, skip_break=True)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )
    def test_draw_cell(self):
        num_cols = 12
        num_rows = 10

        i = num_cols // 2
        j = num_rows // 2

        expected_x1 = 0 + i * 10
        expected_y1 = 0 + j * 10
        expected_x2 = expected_x1 + 10
        expected_y2 = expected_y1 + 10

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        x1 = m1._Maze__x1 + i * m1._Maze__cell_size_x
        y1 = m1._Maze__y1 + j * m1._Maze__cell_size_y
        x2 = x1 + m1._Maze__cell_size_x
        y2 = y1 + m1._Maze__cell_size_y
        self.assertEqual(
                (expected_x1, expected_x2, expected_y1, expected_y2), (x1,x2,y1,y2)
        )

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        prev_cells = m1._Maze__cells.copy()
        m1._Maze__break_entrance_and_exit()
        self.assertEqual(
                False, prev_cells[0][0].has_top_wall)
        self.assertEqual(
                False,prev_cells[-1][-1].has_bottom_wall)

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10

        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(m1._Maze__cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()
