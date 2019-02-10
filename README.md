# Parallel-K-Means
Parallelised implementation of K-Means Algorithm


## Generate Data
```
$ python dataset.py
```

## Sequential
```
$ make clean
$ make sequential
$ ./sequential #clusters input.data output.clusters output.centroids
```

## OpenMP
```
$ make clean
$ make omp
$ ./omp #clusters #threads input.data output.clusters output.centroids
```


## PThread
```
$ make clean
$ make pthread
$ ./pthread #clusters #threads input.data output.clusters output.centroids
```

## Visualise Clusters
```
$ python3 visualise.py output.clusters #data_points #clusters
```

## Generate Performance curves
(Make datasets of sizes 1000, 5000, 10000, 20000, 50000, 75000, 100000 using `dataset.py`)
```
$ ./genpoints.sh seq
$ ./genpoints.sh omp
$ ./genpoints.sh pthread
$ ./genpoints.sh plot
```

