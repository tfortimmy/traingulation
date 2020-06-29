import numpy as np


class Line():

    def __init__(self, i1, x1, y1, i2, x2, y2):

        assert x1 != x2 or y1 != y2, f"Cannot have a 0 length line here ({i1}, {i2})"

        self.i1, self.i2 = i1, i2
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    @property
    def length(self):
        return np.sqrt((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)

    @property
    def is_vertical(self):
        return self.x1 == self.x2

    @property
    def gradient(self):
        if not self.is_vertical:
            return (self.y2 - self.y1)/(self.x2 - self.x1)
        else:
            return np.PINF

    @property
    def intercept(self):
        return self.y1 - (self.gradient * self.x1)

    @property
    def to_plot(self):
        return [self.x1, self.x2], [self.y1, self.y2]

    @property
    def mid_point(self):
        return (self.x1 + self.x2)/2, (self.y1 + self.y2)/2

    @property
    def ordered_x(self):
        """Min and max X values for the line"""
        return sorted([self.x1, self.x2])

    @property
    def ordered_y(self):
        """Min and max Y values for the line"""
        return sorted([self.y1, self.y2])

    def x_in_range(self, x, strict=True):

        # is the value inside the range
        in_bounds = x >= self.ordered_x[0] and x <= self.ordered_x[1]

        # as we are dealing with floats we get some variation so we want to be extra careful
        is_close = np.isclose(x, self.x1) or np.isclose(x, self.x2)

        if strict:
            # if strict ignore close
            return in_bounds and not is_close
        else:
            # otherwise allow it
            return in_bounds or is_close

    def y_in_range(self, y, strict=True):

        # is the value inside the range
        in_bounds = y >= self.ordered_y[0] and y <= self.ordered_y[1]

        # as we are dealing with floats we get some variation so we want to be extra careful
        is_close = np.isclose(y, self.y1) or np.isclose(y, self.y2)

        if strict:
            # if strict ignore close
            return in_bounds and not is_close
        else:
            # otherwise allow it
            return in_bounds or is_close

    def point_in(self, i):
        return i in [self.i1, self.i2]

    def y_at_x(self, x):
        """
        What is the value of y at a certain x value
        """
        return self.intercept + (x * self.gradient)

    def x_at_y(self, y):
        """
        What is the value of x at a given y value
        """
        return (y - self.intercept) / self.gradient

    def intersection(self, l):
        """
        Calculate the intersection of this line with another

        Returns
        -------
        ix: float
        None if no intersection

        iy: float
        None if no intersection
        """
        # if the x values don't overlap return no
        if self.ordered_x[1] < l.ordered_x[0] or \
                self.ordered_x[0] > l.ordered_x[1]:
            return None, None

        # if the y values don't overlap return no
        elif self.ordered_y[1] < l.ordered_y[0] or \
                self.ordered_y[0] > l.ordered_y[1]:
            return None, None

        # if they are vertical we need some special logic
        elif self.is_vertical:
            if l.is_vertical:
                # all yvals which intersect
                y_vals = []

                if self.y_in_range(l.y1):
                    y_vals.append(l.y1)
                if self.y_in_range(l.y2):
                    y_vals.append(l.y2)
                if l.y_in_range(self.y1):
                    y_vals.append(self.y1)
                if l.y_in_range(self.y2):
                    y_vals.append(self.y2)

                # if we have any useful points return the minimum
                if y_vals:
                    return self.x1, min(y_vals)
                else:
                    return None, None
            else:
                iy = l.y_at_x(self.x1)
                if self.y_in_range(iy) and l.y_in_range(iy):
                    return self.x1, l.y_at_x(self.x1)
                else:
                    return None, None

        # if they are horizontal we need some special logic
        elif self.gradient == 0:
            if l.gradient == 0:
                # all xvals which intersect
                x_vals = []

                if self.x_in_range(l.x1):
                    x_vals.append(l.x1)
                if self.x_in_range(l.x2):
                    x_vals.append(l.x2)
                if l.x_in_range(self.x1):
                    x_vals.append(self.x1)
                if l.x_in_range(self.x2):
                    x_vals.append(self.x2)

                # if we have any useful points return the minimum
                if x_vals:
                    return min(x_vals), self.y1
                else:
                    return None, None
            else:
                ix = l.x_at_y(self.y1)
                if self.x_in_range(ix) and l.x_in_range(ix):
                    return ix, self.y1
                else:
                    return None, None

        # If the gradients are the same then we assume they do not intersect
        elif self.gradient == l.gradient:
            return None, None

        else:
            # Find the intersection point if they were both infinite lines
            ix = (self.intercept - l.intercept) / (l.gradient - self.gradient)

            # is the point of intersection on the actual line?
            if self.x_in_range(ix) and l.x_in_range(ix):
                return ix, self.y_at_x(ix)
            else:
                return None, None


class Triangle():

    def __init__(self, i1, x1, y1, i2, x2, y2, i3, x3, y3):
        self.i1, self.i2, self.i3 = i1, i2, i3
        self.x1, self.y1, self.x2, self.y2, self.x3, self.y3 = x1, y1, x2, y2, x3, y3

    def point_in(self, i):
        return i in [self.i1, self.i2, self.i3]

    @property
    def center(self):
        """
        Returns the central coordinate of the triangle

        Find the intersection of two lines from corner to midpoint of opposite side
        """

        # The midpoint between point 1 and 2 (and 1 and 3 respectively)
        mp12 = Line(
            self.i1, self.x1, self.y1, self.i2,
            self.x2, self.y2
        ).mid_point
        mp13 = Line(
            self.i1, self.x1, self.y1, self.i3,
            self.x3, self.y3
        ).mid_point

        # create lines from the midpoints to the opposite corners
        # the line for corner 3
        l3 = Line(self.i3, self.x3, self.y3, -1, *mp12)
        l2 = Line(self.i2, self.x2, self.y2, -1, *mp13)

        center_x, center_y = l2.intersection(l3)

        if center_x is None:
            raise RuntimeError("Something has gone very wrong")

        return center_x, center_y

    @property
    def to_plot(self):
        return [
            [self.x1, self.y1],
            [self.x2, self.y2],
            [self.x3, self.y3],
        ]
