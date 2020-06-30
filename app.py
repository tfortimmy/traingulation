import pdb
import numpy as np
import matplotlib.pyplot as plt
from triangulation.utils import Line, Triangle
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import argparse


class Triangulation():

    def __init__(self, num_points, edge_points_prop=0.2, random_seed=420):

        num_edge_points = int(num_points * edge_points_prop)

        self.points = Triangulation.create_points(
            num_points, num_edge_points, random_seed)

    def run(self):
        self.find_lines()

        self.find_triangles()

    @staticmethod
    def create_points(num_points, num_edge_points, random_seed):

        assert num_points > num_edge_points + 4

        np.random.seed(random_seed)

        # remove the corner
        points = np.random.uniform(0, 1, (num_points - num_edge_points - 4, 2))

        # add in the corner points
        corner_points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        points = np.concatenate((points, corner_points), axis=0)

        # create the edge points
        edge_points = np.random.uniform(0, 1, (num_edge_points, 2))
        edge_points[range(0, num_edge_points, 4), 0] = 0
        edge_points[range(1, num_edge_points, 4), 0] = 1
        edge_points[range(2, num_edge_points, 4), 1] = 0
        edge_points[range(3, num_edge_points, 4), 1] = 1
        points = np.concatenate((points, edge_points), axis=0)

        return points

    @staticmethod
    def calculate_distance_matrix(points):
        # cheat way to calculate the distance matrix
        comp = np.array([np.complex(x, y) for x, y in points])
        x, y = np.meshgrid(comp, comp)
        distmat = np.abs(x - y)

        return distmat

    @staticmethod
    def get_dist_table(distmat):

        # convert the distmat into a table where we have the distance, point 1 index, point 2 index
        XX, YY = np.meshgrid(np.arange(len(distmat)), np.arange(len(distmat)))
        dist_table = np.c_[distmat.ravel(), XX.ravel(), YY.ravel()]

        # remove all distances to themselves and the items with index higher than them (remove dupes/upper triangular)
        dist_table = dist_table[dist_table[:, 1] < dist_table[:, 2], :]

        return dist_table

    def find_lines(self):

        # calculate the distance matrix
        distmat = Triangulation.calculate_distance_matrix(self.points)

        # order the distance matrix into a table
        dist_table = Triangulation.get_dist_table(distmat)

        # find the order of distances
        dist_order = np.argsort(dist_table[:, 0])

        self.lines = []

        # loop through all points
        for i, (d, x, y) in enumerate(dist_table[dist_order]):

            # The line going from point x to point y
            tmp_line = Line(
                int(x),
                *self.points[int(x)],
                int(y),
                *self.points[int(y)]
            )

            # Are we going to add this one to the list
            add = True

            # check if it intersects with any of the previous lines
            for l in self.lines:
                ix, iy = l.intersection(tmp_line)

                if ix is not None:
                    # if it does then we don't want to add it
                    add = False
                    # stop checking as it has failed
                    break

            # if it passed add the line
            if add:
                self.lines.append(tmp_line)

    def find_triangles(self):
        self.triangles = []
        # find triangles
        for i, p in enumerate(self.points):
            # Find all lines that connect to this point
            p_lines = [l for l in self.lines if l.point_in(i)]

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
                                l for l in self.lines
                                if l.point_in(l1_idx) and l.point_in(l2_idx)
                            ]

                            # If the do connect create a new triangle
                            if connector:
                                self.triangles.append(
                                    Triangle(
                                        i, *p, l1_idx,
                                        *self.points[l1_idx], l2_idx,
                                        *self.points[l2_idx]
                                    )
                                )

    def plot(self, annotate=False):
        fig, ax = plt.subplots()

        # ax.scatter(points[:, 0], points[:, 1])

        if annotate:
            for i, p in enumerate(self.points):
                ax.annotate(i, (p[0], p[1]))

        # for l in lines:
        #     ax.plot([l.x1, l.x2], [l.y1, l.y2])

        # print("LINES")
        # for l in lines:
        #     print(l.i1, l.i2)

        # print("Triangles")
        # for t in triangles:
        #     print(t.i1, t.i2, t.i3)

        patches = []
        centers = []
        for t in self.triangles:
            c_x, c_y = t.center
            centers.append([c_x, c_y])

            p = Polygon(t.to_plot, color=(c_x, 0, c_y))
            patches.append(p)

        # add the triangles to a patch collection and add it to the axes
        p = PatchCollection(patches, match_original=True)
        ax.add_collection(p)

        plt.axis('off')
        plt.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="Triangulation",
        description="Make pretty triangles"
    )

    parser.add_argument('-p', '--points', type=int, default=50)
    parser.add_argument('-e', '--edge-points', type=float, default=0.2)
    parser.add_argument('-r', '--random-seed', type=int, default=420)

    args = parser.parse_args()

    app = Triangulation(args.points, args.edge_points, args.random_seed)

    app.run()
    app.plot()
