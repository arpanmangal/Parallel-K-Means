"""
For plotting timings
"""

import matplotlib.pyplot as plt
import numpy as np
import sys

if __name__ == '__main__':
    if (sys.argv[1] == 'time'):
        Xlabel = "# Data Points"
        Ylabel = "Time taken (secs)"

        # Sequential
        X, Y = [], []
        with open('kmeans-sequential') as f:
            for line in f:
                size, time = line.split(' ')
                X.append(float(size))
                Y.append(float(time))

        fig = plt.figure(1)
        plt.plot(X, Y, 'r-', label="sequential")
        plt.suptitle('Sequential')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/sequential.png')
        plt.show()


        # OpenMP
        fig = plt.figure(2)
        colors = ['r-', 'y-', 'g-', 'b-']
        for i, t in enumerate([1, 2, 4, 8]):
            X, Y = [], []
            with open(('kmeans-omp_' + str(t))) as f:
                for line in f:
                    size, time = line.split(' ')
                    X.append(float(size))
                    Y.append(float(time))
            plt.plot(X, Y, colors[i], label=(str(t)+" threads"))
        plt.suptitle('OpenMP')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/omp.png')
        plt.show()


        # Pthread
        fig = plt.figure(3)
        colors = ['r-', 'y-', 'g-', 'b-']
        for i, t in enumerate([1, 2, 4, 8]):
            X, Y = [], []
            with open(('kmeans-pthread_' + str(t))) as f:
                for line in f:
                    size, time = line.split(' ')
                    X.append(float(size))
                    Y.append(float(time))
            plt.plot(X, Y, colors[i], label=(str(t)+" threads"))
        plt.suptitle('PThread')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/pthread.png')
        plt.show()

    elif (sys.argv[1] == 'speedup'):
        Xlabel = "# Data Points"
        Ylabel = "Speedup"

        seq_timings = []
        with open('kmeans-sequential') as f:
            for line in f:
                size, time = line.split(' ')
                seq_timings.append(float(time))

        # OpenMP
        fig = plt.figure(1)
        colors = ['r-', 'y-', 'g-', 'b-']
        for i, t in enumerate([2, 4, 8]):
            X, Y = [], []
            with open(('kmeans-omp_' + str(t))) as f:
                for line in f:
                    size, time = line.split(' ')
                    X.append(float(size))
                    Y.append(float(time))
            Y = list(np.array(seq_timings) / np.array(Y))
            plt.plot(X, Y, colors[i], label=(str(t)+" threads"))
        plt.suptitle('OpenMP Speedup')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/speedup_omp.png')
        plt.show()

        # OpenMP
        fig = plt.figure(2)
        colors = ['r-', 'y-', 'g-', 'b-']
        for i, t in enumerate([2, 4, 8]):
            X, Y = [], []
            with open(('kmeans-pthread_' + str(t))) as f:
                for line in f:
                    size, time = line.split(' ')
                    X.append(float(size))
                    Y.append(float(time))
            Y = list(np.array(seq_timings) / np.array(Y))
            plt.plot(X, Y, colors[i], label=(str(t)+" threads"))
        plt.suptitle('Pthread Speedup')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/speedup_pthread.png')
        plt.show()

    elif (sys.argv[1] == 'efficiency'):
        Xlabel = "# Data Points"
        Ylabel = "Efficiency"

        seq_timings = []
        with open('kmeans-sequential') as f:
            for line in f:
                size, time = line.split(' ')
                seq_timings.append(float(time))

        # OpenMP
        fig = plt.figure(1)
        colors = ['r-', 'y-', 'g-', 'b-']
        for i, t in enumerate([2, 4, 8]):
            X, Y = [], []
            with open(('kmeans-omp_' + str(t))) as f:
                for line in f:
                    size, time = line.split(' ')
                    X.append(float(size))
                    Y.append(float(time))
            Y = list(np.array(seq_timings) / (t * np.array(Y)))
            plt.plot(X, Y, colors[i], label=(str(t)+" threads"))
        plt.suptitle('OpenMP Efficiency')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/efficiency_omp.png')
        plt.show()

        # OpenMP
        fig = plt.figure(2)
        colors = ['r-', 'y-', 'g-', 'b-']
        for i, t in enumerate([2, 4, 8]):
            X, Y = [], []
            with open(('kmeans-pthread_' + str(t))) as f:
                for line in f:
                    size, time = line.split(' ')
                    X.append(float(size))
                    Y.append(float(time))
            Y = list(np.array(seq_timings) / (t * np.array(Y)))
            print (Y)
            plt.plot(X, Y, colors[i], label=(str(t)+" threads"))
        plt.suptitle('Pthread Efficiency')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/efficiency_pthread.png')
        plt.show()