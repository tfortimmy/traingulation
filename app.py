import pdb
import numpy as np
import matplotlib.pyplot as plt
from triangulation.utils import Line, Triangle, intersection

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

# remove all distances to themselves and the items with index higher than them (remove dupes/upper triangular)
dist_table = dist_table[dist_table[:, 1] < dist_table[:, 2], :]

# find the order of distances
dist_order = np.argsort(dist_table[:, 0])

lines = []

for i, (d, x, y) in enumerate(dist_table[dist_order]):

    # The line going from point x to point y
    tmp_line = Line(int(x), *points[int(x)], int(y), *points[int(y)])

    # Are we going to add this one to the list
    add = True

    # check if it intersects with any of the previous lines
    for l in lines:
        if intersection(l, tmp_line):

            # if it does then we don't want to add it
            add = False
            # stop checking as it has failed
            break

    # if it passed add the line
    if add:
        lines.append(tmp_line)

print("LINES")
for l in lines:
    print(l.i1, l.i2)


triangles = []
# find triangles
for i, p in enumerate(points):
    # Find all lines that connect to this point
    p_lines = [l for l in lines if l.point_in(i)]

    # loop through all lines connected to the point
    # don't loop through the last one as we have a nested loop that starts at j+1
    for j, l1 in enumerate(p_lines[:-1]):
        # the index of the point (That is not i)
        l1_idx = l1.i1 if l1.i1 != i else l1.i2

        # we don't want to check for things we have already checked
        if l1_idx > i:
            for l2 in p_lines[j+1:]:
                # the index of the point (That is not i)
                l2_idx = l2.i1 if l2.i1 != i else l2.i2

                # we can exclude points which have already been inspected
                if l2_idx > i:
                    # find out if any lines connect the other two points
                    connector = [
                        l for l in lines
                        if l.point_in(l1_idx) and l.point_in(l2_idx)
                    ]

                    # If the do connect create a new triangle
                    if connector:
                        triangles.append(
                            Triangle(
                                i, *p, l1_idx, *
                                points[l1_idx], l2_idx, *points[l2_idx]
                            )
                        )


fig, ax = plt.subplots()

ax.scatter(points[:, 0], points[:, 1])

for i, p in enumerate(points):
    ax.annotate(i, (p[0], p[1]))

for l in lines:
    ax.plot([l.x1, l.x2], [l.y1, l.y2])

print("Triangles")
for t in triangles:
    print(t.i1, t.i2, t.i3)

plt.show()
