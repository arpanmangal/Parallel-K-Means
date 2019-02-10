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
        with open('results/kmeans-sequential') as f:
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
        colors = ['r-', 'y-', 'g-', 'b-', 'm-']
        for i, t in enumerate([1, 2, 4, 6, 8]):
            X, Y = [], []
            with open(('results/kmeans-omp_' + str(t))) as f:
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
        colors = ['r-', 'y-', 'g-', 'b-', 'm-']
        for i, t in enumerate([1, 2, 4, 6, 8]):
            X, Y = [], []
            with open(('results/kmeans-pthread_' + str(t))) as f:
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
        Xlabel = "# Threads (p)"
        Ylabel = "Speedup"

        seq_timings = {}
        with open('results/kmeans-sequential') as f:
            for line in f:
                size, time = line.split(' ')
                seq_timings[int(size)] = (float(time))

        # OpenMP
        fig = plt.figure(1)
        colors = ['r-', 'y-', 'g-', 'c-', 'b-', 'm-', 'k-']
        for i, size in enumerate([1000, 5000, 10000, 20000, 50000, 75000, 100000]):
            X, Y = [], []
            with open(('results/kmeans-omp_' + str(size))) as f:
                for line in f:
                    t, time = line.split(' ')
                    X.append(int(t))
                    Y.append(seq_timings[size] / float(time))
            plt.plot(X, Y, colors[i], label=("n = "+str(size)) )
        plt.suptitle('OpenMP Speedup')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/speedup_omp.png')
        plt.show()
        
        # Pthread
        fig = plt.figure(2)
        colors = ['r-', 'y-', 'g-', 'c-', 'b-', 'm-', 'k-']
        for i, size in enumerate([1000, 5000, 10000, 20000, 50000, 75000, 100000]):
            X, Y = [], []
            with open(('results/kmeans-pthread_' + str(size))) as f:
                for line in f:
                    t, time = line.split(' ')
                    X.append(int(t))
                    Y.append(seq_timings[size] / float(time))
            plt.plot(X, Y, colors[i], label=("n = "+str(size)) )
        plt.suptitle('Pthread Speedup')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/speedup_pthread.png')
        plt.show()

    elif (sys.argv[1] == 'efficiencyW'):
        Xlabel = "# Data Points (W)"
        Ylabel = "Efficiency"

        seq_timings = []
        with open('results/kmeans-sequential') as f:
            for line in f:
                size, time = line.split(' ')
                seq_timings.append(float(time))

        # OpenMP
        fig = plt.figure(1)
        colors = ['r-', 'y-', 'g-', 'b-', 'm-']
        for i, t in enumerate([2, 4, 6, 8]):
            X, Y = [], []
            with open(('results/kmeans-omp_' + str(t))) as f:
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
        colors = ['r-', 'y-', 'g-', 'b-', 'm-']
        for i, t in enumerate([2, 4, 6, 8]):
            X, Y = [], []
            with open(('results/kmeans-pthread_' + str(t))) as f:
                for line in f:
                    size, time = line.split(' ')
                    X.append(float(size))
                    Y.append(float(time))
            Y = list(np.array(seq_timings) / (t * np.array(Y)))
            plt.plot(X, Y, colors[i], label=(str(t)+" threads"))
        plt.suptitle('Pthread Efficiency')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/efficiency_pthread.png')
        plt.show()

    elif (sys.argv[1] == 'efficiencyP'):
        Xlabel = "# Threads (p)"
        Ylabel = "Efficiency"

        seq_timings = {}
        with open('results/kmeans-sequential') as f:
            for line in f:
                size, time = line.split(' ')
                seq_timings[int(size)] = (float(time))

        # OpenMP
        fig = plt.figure(1)
        colors = ['r-', 'y-', 'g-', 'c-', 'b-', 'm-', 'k-']
        for i, size in enumerate([1000, 5000, 10000, 20000, 50000, 75000, 100000]):
            X, Y = [], []
            with open(('results/kmeans-omp_' + str(size))) as f:
                for line in f:
                    t, time = line.split(' ')
                    X.append(int(t))
                    Y.append(seq_timings[size] / (int(t) * float(time)) )
            plt.plot(X, Y, colors[i], label=("n = "+str(size)) )
        plt.suptitle('OpenMP Efficiency')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/efficiencyP_omp.png')
        plt.show()

        # Pthread
        fig = plt.figure(2)
        colors = ['r-', 'y-', 'g-', 'c-', 'b-', 'm-', 'k-']
        for i, size in enumerate([1000, 5000, 10000, 20000, 50000, 75000, 100000]):
            X, Y = [], []
            with open(('results/kmeans-pthread_' + str(size))) as f:
                for line in f:
                    t, time = line.split(' ')
                    X.append(int(t))
                    Y.append(seq_timings[size] / (int(t) * float(time)) )
            plt.plot(X, Y, colors[i], label=("n = "+str(size)) )
        plt.suptitle('Pthread Efficiency')
        plt.ylabel(Ylabel)
        plt.xlabel(Xlabel)
        plt.yscale('linear')
        plt.xscale('linear')
        plt.legend()
        fig.savefig('plots/efficiencyP_pthread.png')
        plt.show()