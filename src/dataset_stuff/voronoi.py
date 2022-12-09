import json
from scipy.spatial import KDTree


def iteration(points, centroids):
    tree = KDTree(centroids)
    out = (tree.query([[0, 0]]))
    print(centroids[out[1][0]])


with open("files/step2.json", "r") as read_file:
    raw_points = json.load(read_file)
    point_list = []

    for p in raw_points:
        point_list.append([p[1], p[0]])

    iteration(point_list, point_list)
