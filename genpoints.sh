#!/bin/bash
#script to generate datapoints for plotting for performance measurements
if [ $# -lt 1 ]; then
    echo "Go Away"
    exit
fi

make clean
mkdir results
if [[ $1 == "seq" ]]; then
    # Sequential
    make sequential
    rm -rf "results/kmeans-sequential"
    for size in 1000 5000 10000 20000 50000 75000 100000;
    do
        echo $size
        inputFile="dataset_" && inputFile+=$size && inputFile+="_5.txt"
        timeTaken=$(./sequential 5 $inputFile "clusters.out" "centroids.out" | grep "omp_get_wtime" | grep -wo "[0-9]*\.[0-9]*")
        echo "$size $timeTaken" | tee -a "results/kmeans-sequential"
    done
    exit
fi

if [[ $1 == "omp" ]]; then
    # OpenMP
    make omp
    for t in 1 2 4 6 8;
    do
        rm -rf "results/kmeans-omp_${t}"
    done
    for size in 1000 5000 10000 20000 50000 75000 100000;
    do
        rm -rf "results/kmeans-omp_${size}"
        for t in 1 2 4 6 8;
        do
            inputFile="dataset_" && inputFile+=$size && inputFile+="_5.txt"
            timeTaken=$(./omp 5 ${t} ${inputFile} "clusters.out" "centroids.out" | grep "omp_get_wtime" | grep -wo "[0-9]*\.[0-9]*")
            echo "$t $timeTaken" | tee -a "results/kmeans-omp_${size}"
            echo "$size $timeTaken" | tee -a "results/kmeans-omp_${t}"
        done
    done
    exit
fi

if [[ $1 == "pthread" ]]; then
    # Pthread
    make pthread
    for t in 1 2 4 6 8;
    do
        rm -rf "results/kmeans-pthread_${t}"
    done
    for size in 1000 5000 10000 20000 50000 75000 100000;
    do
        rm -rf "results/kmeans-pthread_${size}"
        for t in 1 2 4 6 8;
        do
            inputFile="dataset_" && inputFile+=$size && inputFile+="_5.txt"
            timeTaken=$(./pthread 5 ${t} ${inputFile} "clusters.out" "centroids.out" | grep "omp_get_wtime" | grep -wo "[0-9]*\.[0-9]*")
            echo "$t $timeTaken" | tee -a "results/kmeans-pthread_${size}"
            echo "$size $timeTaken" | tee -a "results/kmeans-pthread_${t}"
        done
    done
    exit
fi

if [[ $1 == "plot" ]]; then
    # Plot the graphs
    python3 plot.py "time"
    python3 plot.py "speedup"
    python3 plot.py "efficiencyW"
    python3 plot.py "efficiencyP"
    exit
fi

echo "Go Away"