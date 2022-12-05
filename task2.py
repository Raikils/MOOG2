from functools import lru_cache
from open3d.cpu.pybind.geometry import PointCloud
from open3d.cpu.pybind.io import read_point_cloud, write_point_cloud
from open3d.cpu.pybind.utility import Vector3dVector
from open3d.cpu.pybind.visualization import draw_geometries
from tqdm import tqdm
import json
import numpy as np




def R(index, u, v):
    if not numerator(index, u, v):
        return numerator(index, u, v)
    return numerator(index, u, v) / dominator(u, v)


def numerator(index, u, v):
    return n_i_k(u)[index[0]] * n_j_l(v)[index[1]]


def dominator(u, v):
    result = 0
    for i in range(0, 13):
        for j in range(0, 13):
            result += n_i_k(u)[i] * n_j_l(v)[j]
    return result


@lru_cache
def n_i_k(u):
    return [n(u, i, 3) for i in range(13)]


@lru_cache
def n_j_l(v):
    return [n(v, j, 3) for j in range(13)]



@lru_cache
def n(u, i, k):
    if k == 1:
        if knot_vector[i] <= u < knot_vector[i + 1]:
            return 1
        else:
            return 0
    else:
        first = (u - knot_vector[i]) / (knot_vector[i + k - 1] - knot_vector[i])
        second = (knot_vector[i + k] - u) / (knot_vector[i + k] - knot_vector[i + 1])
        return first * n(u, i, k - 1) + second * n(u, i + 1, k - 1)




if __name__ == '__main__':
    x = []
    y = []
    z = []
    result_points = []
    controls = []
    points = []
    indices = []
    grid_size = []

    f = open('8.json')
    data = json.load(f)
    for point in data['surface']['points']:
        points.append(point)
    for i in data['surface']['indices']:
        indices.append(i)
    f.close()

    knot_vector = tuple(range(17))
    controls = np.arange(max(knot_vector), step=0.1)


    for u in tqdm(controls):
        for v in controls:
            result = 0
            for i in range(13):
                for j in range(13):
                    result += points[indices.index([i, j])][0] * R([i, j], u, v)
            x.append(result)

    for u in tqdm(controls):
        for v in controls:
            result = 0
            for i in range(13):
                for j in range(13):
                    result += points[indices.index([i, j])][1] * R([i, j], u, v)
            y.append(result)

    for u in tqdm(controls):
        for v in controls:
            result = 0
            for i in range(13):
                for j in range(13):
                    result += points[indices.index([i, j])][2] * R([i, j], u, v)
            z.append(result)

    result = []

    for i in range(0, len(x)):
        if x[i] != 0 and y[i] != 0 and z[i] != 0:
            result.append([x[i], y[i], z[i]])

    pcd = PointCloud()
    pcd.points = Vector3dVector(result)
    write_point_cloud("surface.ply", pcd)
    pcd = read_point_cloud("surface.ply")
    draw_geometries([pcd])