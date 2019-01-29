"""
Python module to generate random data (normally distributed around k-centroids)
for K-Means
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
from itertools import cycle
cycol = cycle('bgrcmk')

def generate3Dpoint (centroid, var):
    return [int(np.random.normal(centroid[0], var, 1)), int(np.random.normal(centroid[1], var, 1)), int(np.random.normal(centroid[2], var, 1))]


def generateData ():
    """
    Generate data for k-means
    """
    # print (np.random.randint(1000, size=(10, 3)))
    k = 10 # 10 clusters
    n = 100 # 100 points
    var = 50
    ulimit = 1000 # 0-1000 range

    centroids = np.random.randint(ulimit, size=(k, 3))
    points = []
    for idx, centroid in enumerate(centroids):
        for i in range(n):
            points.append((generate3Dpoint(centroid, var), idx))

    for point in points:
        print (point)

    np.random.shuffle(points)

    dataFile = open('data.txt', 'w')
    dataFile.write('%d %d\n' % (n*k, k))
    for point in points:
        dataFile.write('%d %d %d\n' % (point[0][0], point[0][1], point[0][2]))

    resultFile = open('result.txt', 'w')
    resultFile.write('%d %d\n' % (n*k, k))
    for point in points:
        resultFile.write('%d %d %d %d\n' % (point[0][0], point[0][1], point[0][2], point[1]))


def plotData (resultFile="result.txt"):
    """
    Reads cluster data and plots it
    """
    resultFile = open(resultFile, 'r')
    (n, k) = tuple(map(int, resultFile.readline().split(' ')))
    print (n, k)
    clusters = []
    for c in range(k):
        clusters.append([])

    for p in range(n):
        (x, y, z, c) = tuple(map(int, resultFile.readline().split(' ')))
        clusters[c].append((x, y, z))
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for cluster in clusters:
        color = np.random.rand(3,)
        points = np.array(cluster)
        print (points.shape)
        print (points)

        ax.scatter(points[:,0], points[:,1], points[:,2], c=next(cycol), marker='o')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

    plt.show()



if __name__ == '__main__':
    # generateData()
    plotData()