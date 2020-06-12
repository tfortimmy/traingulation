from unittest import TestCase
from triangulation.utils import Line, intersection, Triangle


class TestIntersection(TestCase):

    def test_parallel(self):
        self.assertFalse(
            intersection(
                Line(0, 0, 0, 1, 1, 1),
                Line(0, 0, 0, 1, 1, 1)
            )
        )

    def test_orthogonal(self):
        self.assertTrue(
            intersection(
                Line(0, -1, -1, 1, 1, 1),
                Line(0, -1, 1, 1, 1, -1)
            )
        )

    def test_is_close(self):

        p2 = [0.86816648, 0.62972852]
        p3 = [.35251871, 0.0675376]
        p4 = [0.62635059, 0.59866086]

        self.assertFalse(
            intersection(
                Line(2, *p2, 4, *p4),
                Line(2, *p2, 3, *p3)
            )
        )
