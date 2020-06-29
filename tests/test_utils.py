from unittest import TestCase
from triangulation.utils import Line, Triangle


class TestLine(TestCase):

    def test_parallel(self):
        ix, iy = Line(0, 0, 0, 1, 1, 1).intersection(
            Line(1, 1, 1, 2, 2, 2)
        )

        self.assertIsNone(ix)
        self.assertIsNone(iy)

    def test_orthogonal(self):
        ix, iy = Line(0, -1, -1, 1, 1, 1).intersection(
            Line(0, -1, 1, 1, 1, -1)
        )

        self.assertEqual(ix, 0)
        self.assertEqual(iy, 0)

    def test_is_close(self):

        p2 = [0.86816648, 0.62972852]
        p3 = [.35251871, 0.0675376]
        p4 = [0.62635059, 0.59866086]

        ix, iy = Line(2, *p2, 4, *p4).intersection(
            Line(2, *p2, 3, *p3)
        )

        self.assertIsNone(ix)
        self.assertIsNone(iy)

    def test_vertical_adjacent(self):

        ix, iy = Line(0, 0, 0, 1, 0, 1).intersection(
            Line(1, 0, 1, 2, 0, 2)
        )

        self.assertIsNone(ix)
        self.assertIsNone(iy)

    def test_vertical_enclosed(self):

        # the second line is included in the first line
        ix, iy = Line(0, 0, 0, 3, 0, 3).intersection(
            Line(1, 0, 1, 2, 0, 2)
        )

        # all have value x as 0
        self.assertEqual(ix, 0)
        # choose the smallest possible y value
        self.assertEqual(iy, 1)

    def test_one_vertical(self):
        ix, iy = Line(0, 0, -1, 1, 0, 1).intersection(
            Line(2, -1, -1, 3, 1, 1)
        )

        self.assertEqual(ix, 0)
        self.assertEqual(iy, 0)

    def test_horizontal_adjacent(self):

        ix, iy = Line(0, 0, 0, 1, 1, 0).intersection(
            Line(1, 1, 0, 2, 2, 0)
        )

        self.assertIsNone(ix)
        self.assertIsNone(iy)

    def test_horizontal_enclosed(self):

        # the second line is included in the first line
        ix, iy = Line(0, 0, 0, 3, 3, 0).intersection(
            Line(1, 1, 0, 2, 2, 0)
        )

        # all have value y as 0
        self.assertEqual(iy, 0)
        # choose the smallest possible x value
        self.assertEqual(ix, 1)

    def test_one_horizontal(self):
        ix, iy = Line(0,  -1, 0, 1,  1, 0).intersection(
            Line(2, -1, -1, 3, 1, 1)
        )

        self.assertEqual(ix, 0)
        self.assertEqual(iy, 0)

    def test_vertical_horizontal(self):
        # one vertical line intersecting one horizontal line
        ix, iy = Line(0, 0, -1, 1, 0, 1).intersection(
            Line(0,  -1, 0, 1,  1, 0)
        )

        self.assertEqual(ix, 0)
        self.assertEqual(iy, 0)

    def test_horizontal_vertical(self):
        ix, iy = Line(0,  -1, 0, 1,  1, 0).intersection(
            Line(0, 0, -1, 1, 0, 1)
        )

        self.assertEqual(ix, 0)
        self.assertEqual(iy, 0)
