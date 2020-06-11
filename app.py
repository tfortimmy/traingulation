import pdb
import numpy as np
import matplotlib.pyplot as plt
from triangulation.utils import Line, intersection

random_seed = 420
num_points = 5

np.random.seed(random_seed)

points = np.random.uniform(0, 1, (num_points, 2))

comp = np.array([np.complex(x, y) for x, y in points])
x, y = np.meshgrid(comp, comp)
distmat = np.abs(x - y)

del comp, x, y

# convert the distmat into a table where we have the distance, point 1 index, point 2 index
XX, YY = np.meshgrid(np.arange(num_points), np.arange(num_points))
dist_table = np.c_[distmat.ravel(), XX.ravel(), YY.ravel()]


del distmat, XX, YY

# remove all distances to themselves and the items with index lower than them (remove dupes)
dist_table = dist_table[dist_table[:, 1] > dist_table[:, 2], :]

# find the order of distances
dist_order = np.argsort(dist_table[:, 0])

lines = []

for i, (d, x, y) in enumerate(dist_table[dist_order]):

    print(i, d, x, y)

    # The line going from point x to point y
    tmp_line = Line(*points[int(x)], *points[int(y)])

    # Are we going to add this one to the list
    add = True

    # check if it intersects with any of the previous lines
    for l in lines:
        if intersection(l, tmp_line):

            print(f'\tIntersects with Line: ({l.x1}, {l.y1}) ({l.x2}, {l.y2})')

            # if it does then we don't want to add it
            add = False
            # stop checking as it has failed
            break

    # if it passed add the line
    if add:
        lines.append(tmp_line)

fig, ax = plt.subplots()

ax.scatter(points[:, 0], points[:, 1])

for i, p in enumerate(points):
    ax.annotate(i, (p[0], p[1]))

for l in lines:
    ax.plot([l.x1, l.x2], [l.y1, l.y2])

print(points)
# print(lines)

plt.show()
