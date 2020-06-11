import numpy as np
import matplotlib.pyplot as plt

random_seed = 420
num_points = 10

np.random.seed(random_seed)

points = np.random.uniform(0, 1, (num_points, 2))

comp = np.array([np.complex(x, y) for x, y in points])
x, y = np.meshgrid(comp, comp)
distmat = np.abs(x - y)

del comp, x, y

# convert the distmat into a table where we have the distance, point 1 index, point 2 index
XX, YY = np.meshgrid(np.arange(num_points), np.arange(num_points))
dist_table = np.vstack(distmat.ravel(), XX.ravel(), YY.ravel())

del distmat, XX, YY

# remove all distances to themselves and the items with index lower than them (remove dupes)
dist_table = dist_table[dist_table[:, 1] > dist_table[:, 2], :]

# find the order of distances
dist_order = np.argsort(dist_table[:, 0])

lines = []

for i, (d, x, y) in enumerate(dist_table[dist_order]):
    pass

plt.scatter(points[:, 0], points[:, 1])
plt.show()


class Line:

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    @property
    def length(self):
        return np.sqrt((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)

    @property
    def gradient(self):
        return (self.x2 - self.x2)/(self.y2 - self.y1)

    @property
    def intersect(self):
        return self.y1 - (self.gradient * self.x1)


# class Triangle:

#     def __init__(self, p1, p2, p3):

#         self


def intersection(l1, l2):
    """
    Do these lines intersect
    """

    # If the gradients are the same then we assume they do not intersect
    if l1.gradient == l2.gradient:
        return False
    else:
        # Find the intersection point if they were both infinite lines
        ix = (l1.intersect - l2.intersect) / (l2.gradient - l1.gradient)

        # is the point of intersection on the actual line?
        if ix > l1.x1 and ix < l1.x2 or ix > l1.x2 and ix < l1.x1:
            return True
        else:
            return False
