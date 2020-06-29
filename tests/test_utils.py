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
