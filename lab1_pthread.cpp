#include "lab1_pthread.h"
#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <omp.h>
using namespace std;

#define Point vector<float>

float distance (Point &A, Point &B) {
    // Calculated distance squared from point A to point B
    return pow(A[0] - B[0], 2) + pow(A[1] - B[1], 2) + pow(A[2] - B[2], 2);
}

void populatePoints (vector<pair<Point, int>> &points, int *data_point_cluster, int N) {
    for (int i = 0; i < N; i++) {
        Point p;
        p.push_back(data_point_cluster[3*i+0]);
        p.push_back(data_point_cluster[3*i+1]);
        p.push_back(data_point_cluster[3*i+2]);
        points[i] = (make_pair(p, 0));
    }
}

void populateCentroids (const vector<Point> &centroidsVec, float *centroids, int K, int offset=0) {
    for (int c = 0; c < K; c++) {
        centroids[3*K*offset + 3*c + 0] = centroidsVec[c][0];
        centroids[3*K*offset + 3*c + 1] = centroidsVec[c][1];
        centroids[3*K*offset + 3*c + 2] = centroidsVec[c][2]; 
    }
}

void populateDataPointClusters (const vector<pair<Point, int>> &points, int *data_point_cluster, int N) {
    for (int i = 0; i < N; i++) {
        data_point_cluster[4*i + 0] = points[i].first[0];
        data_point_cluster[4*i + 1] = points[i].first[1];
        data_point_cluster[4*i + 2] = points[i].first[2];
        data_point_cluster[4*i + 3] = points[i].second;
    }
}

// Object for storing everything to be passed to pthread function call
struct pthreadObj {
    int tid;
    int N;
    int K;
    int t;
    vector<pair<Point, int>> *points;
    vector<Point> *centroidsVec;
};

void* assignCentroid (void *arg) {
    pthreadObj *obj = (pthreadObj *) arg;
    int tid = obj->tid;
    int N = obj->N;
    int K = obj->K;
    int t = obj->t;
    vector<pair<Point, int>> *points = obj->points;
    vector<Point> *centroidsVec = obj->centroidsVec;

    int length_per_thread = N / t;
    int start = tid * length_per_thread;

    for (int i = start; i < start+length_per_thread; i++) {
        float minDist = distance((*points)[i].first, (*centroidsVec)[0]);
        int minCentroid = 0;
        for (int j = 1; j < K; j++) {
            // Compute distance with jth centroid
            float dist = distance((*points)[i].first, (*centroidsVec)[j]);
            if (dist < minDist) {
                minDist = dist;
                minCentroid = j;
            }
        }
        (*points)[i].second = minCentroid;
    }

    return NULL;
}

void kmeans_pthread(int num_threads, int N, int K, int* data_points, int** data_point_cluster, float** centroids, int* num_iterations ) {     
    // Initialise constants (hyperparameters)
    int numIters = *num_iterations = 100;

    // Allocate memory
    *data_point_cluster = (int*)malloc(sizeof(int)*(N*4));
    *centroids = (float*)malloc(sizeof(float)*( 3 * (numIters + 1) * K ));

    vector<Point> centroidsVec(K); // K centroid
    vector<pair<Point, int>> points(N); // N points with corresponding centroid assignment

    populatePoints(points, data_points, N);

    /** Begin timer */
    double start_time = omp_get_wtime();
    // Shuffle the points
    // auto rng = default_random_engine {};
    // shuffle(begin(points), end(points), rng);
    
    /* initialize random seed: deterministically random */
    srand (0);

    // Initialisation (forgy method)
    for (int i = 0; i < K; i++) {
        int r = rand() % N; // A random point
        centroidsVec[i] = points[r].first;
    }
    populateCentroids (centroidsVec, *centroids, K, 0);

    /* Setting up threads */
    pthread_t threads[num_threads];
    pthreadObj args[num_threads];

    // Loop
    for (int it = 1; it <= numIters; it++) {
        // Assign each point to a centroid
        for (int tid = 0; tid < num_threads; tid++) {
            args[tid] = {tid, N, K, num_threads, &points, &centroidsVec};
            pthread_create(&threads[tid], NULL, assignCentroid, &args[tid]);
        }
        for (int tid = 0; tid < num_threads; tid++)
            pthread_join(threads[tid], NULL);

        // Recompute the centroidsVec
        vector<int> pointCount(K, 0); // Number of points alloted to kth centroid
        for (int j = 0; j < K; j++) {
            // Each centroid -> (0,0,0)
            centroidsVec[j][0] = 0.0;
            centroidsVec[j][1] = 0.0;
            centroidsVec[j][2] = 0.0;
        }
        for (int i = 0; i < N; i++) {
            // Add point to corresponding centroid
            int c = points[i].second;
            pointCount[c]++;
            centroidsVec[c][0] += points[i].first[0];
            centroidsVec[c][1] += points[i].first[1];
            centroidsVec[c][2] += points[i].first[2];
        }

        for (int j = 0; j < K; j++) {
            // Divide each centroid sum by freq, to get coordi.
            if (pointCount[j] == 0) {
                int r = rand() % N; // A random point
                centroidsVec[j] = points[r].first;
            } else {
                centroidsVec[j][0] /= pointCount[j];
                centroidsVec[j][1] /= pointCount[j];
                centroidsVec[j][2] /= pointCount[j];
            }
        }

        // Copy the centroid vector
        populateCentroids (centroidsVec, *centroids, K, it);
    }

    // Copy the points to data cluster
    populateDataPointClusters(points, *data_point_cluster, N);

    /** End time */
    double end_time = omp_get_wtime();
    cout << "Time taken(mine): " << end_time - start_time << " secs" << endl;
}
