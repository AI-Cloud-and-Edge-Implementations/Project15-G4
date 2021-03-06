import math


def find_distance(pt1, pt2):
    return math.sqrt((pt2[1] - pt1[1]) ** 2 + (pt2[0] - pt1[0]) ** 2)
