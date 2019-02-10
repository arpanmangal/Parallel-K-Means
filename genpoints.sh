#!/bin/bash
#script to generate datapoints for plotting for performance measurements
if [ $# -lt 1 ]; then
    echo "Go Away"
    exit
fi

make clean
if [[ $1 == "seq" ]]; then
    # Sequential
    make sequential
    rm -rf "kmeans-sequential"
    for size in 1000 5000 10000 50000 100000;
    do
        echo $size
        inputFile="dataset_" && inputFile+=$size && inputFile+="_5.txt"
        timeTaken=$(./sequential 5 $inputFile "clusters.out" "centroids.out" | grep "omp_get_wtime" | grep -wo "[0-9]*\.[0-9]*")
        echo "$size $timeTaken" | tee -a "kmeans-sequential"
    done
    exit
fi

if [[ $1 == "omp" ]]; then
    # OpenMP
    make omp
    for t in 1 2 4 8;
    do
        rm -rf "kmeans-omp_${t}"
        for size in 1000 5000 10000 50000 100000;
        do
            echo $size
            inputFile="dataset_" && inputFile+=$size && inputFile+="_5.txt"
            timeTaken=$(./omp 5 ${t} ${inputFile} "clusters.out" "centroids.out" | grep "omp_get_wtime" | grep -wo "[0-9]*\.[0-9]*")
            echo "$size $timeTaken" | tee -a "kmeans-omp_${t}"
        done
    done
    exit
fi

if [[ $1 == "pthread" ]]; then
    # Pthread
    make pthread
    for t in 1 2 4 8;
    do
        rm -rf "kmeans-pthread_${t}"
        for size in 1000 5000 10000 50000 100000;
        do
            echo $size
            inputFile="dataset_" && inputFile+=$size && inputFile+="_5.txt"
            timeTaken=$(./pthread 5 ${t} ${inputFile} "clusters.out" "centroids.out" | grep "omp_get_wtime" | grep -wo "[0-9]*\.[0-9]*")
            echo "$size $timeTaken" | tee -a "kmeans-pthread_${t}"
        done
    done
    exit
fi

if [[ $1 == "plot" ]]; then
    # Plot the graphs
    python3 plot.py "time"
    python3 plot.py "speedup"
    python3 plot.py "efficiency"
    exit
fi

echo "Go Away"