import json
import math
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    points = []
    points_x = []
    points_y = []

    f = open('8.json')
    data = json.load(f)
    for point in data['curve']:
        points.append(point)
        points_x.append(point[0])
        points_y.append(point[1])
    f.close()


    def evalue(j, a, i):
        return (math.pow(1 - j, 3) * a[i]) + (3 * j * (math.pow(1 - j, 2)) * a[i + 1]) + (
                    3 * (math.pow(j, 2)) * (1 - j) * a[i + 2]) + (math.pow(j, 3) * a[i + 3])


    x = []
    y = []

    index = 0
    for i in range(0, 3):
        for j in np.arange(0, 1, 0.001):
            x.append(evalue(j, points_x, index))
        index += 3

    index = 0
    for i in range(0, 3):
        for j in np.arange(0, 1, 0.001):
            y.append(evalue(j, points_y, index))
        index += 3

    plt.plot(points_x, points_y)
    plt.plot(x, y)
    plt.show()


