/** Code for OpenMP implementation of K-Means */
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <random>
#include <fstream>
#include <omp.h>
using namespace std;

#ifndef THREADS
#define THREADS 4
#endif

#define Point vector<int>

int distance (Point A, Point B) {
    // Calculated distance squared from point A to point B
    // !Take care of long long
    return pow(A[0] - B[0], 2) + pow(A[1] - B[1], 2) + pow(A[2] - B[2], 2);
}

int main () {
    int N, K; // Number of points and clusters
    cin >> N >> K;

    vector<Point> centroids(K); // K centroid
    vector<pair<Point, int>> points(N); // N points with corresponding centroid assignment

    for (int i = 0; i < N; i++) {
        // Input the N points
        int x, y, z;
        cin >> x >> y >> z;
        Point p{x, y, z};
        points[i] = make_pair(p, 0);
    }

    /** Begin timer */
    double start_time = omp_get_wtime();
    // Shuffle the points
    // auto rng = default_random_engine {};
    // shuffle(begin(points), end(points), rng);
    
    // Initialisation
    for (int i = 0; i < K; i++) {
        centroids[i] = points[i].first;
    }

    /* initialize random seed: */
    srand (time(NULL));

    /* number of threads */
    omp_set_num_threads(THREADS);
    // cout << "Number of threads: " << omp_get_num_threads() << endl;

    // Loop
    int iters = 200;
    double iter_start_time = omp_get_wtime();
    while (iters--) {
        // Assign each point to a centroid
        #pragma omp parallel for schedule(dynamic, 64)
        for (int i = 0; i < N; i++) {
            // printf("thread: %d , index: %d\n", omp_get_thread_num(), i);
            int minDist = distance(points[i].first, centroids[0]);
            int minCentroid = 0;
            
            for (int j = 1; j < K; j++) {
                // Compute distance with jth centroid
                int dist = distance(points[i].first, centroids[j]);
                if (dist < minDist) {
                    minDist = dist;
                    minCentroid = j;
                    // points[i].second = j;
                }
            }

            points[i].second = minCentroid;
        }

        // Recompute the centroids
        vector<int> pointCount(K, 0); // Number of points alloted to kth centroid
        for (int j = 0; j < K; j++) {
            // Each centroid -> (0,0,0)
            centroids[j][0] = 0;
            centroids[j][1] = 0;
            centroids[j][2] = 0;
        }

        #pragma omp parallel for schedule(static, 64)
        for (int i = 0; i < N; i++) {
            // Add point to corresponding centroid
            int c = points[i].second;
            pointCount[c]++;
            centroids[c][0] += points[i].first[0];
            centroids[c][1] += points[i].first[1];
            centroids[c][2] += points[i].first[2];
        }

        for (int j = 0; j < K; j++) {
            // Divide each centroid sum by freq, to get coordi.
            if (pointCount[j] == 0) {
                int r = rand() % N; // A random point
                centroids[j] = points[r].first;
            } else {
                centroids[j][0] /= pointCount[j];
                centroids[j][1] /= pointCount[j];
                centroids[j][2] /= pointCount[j];
            }
        }
    }

    /** End time */
    double end_time = omp_get_wtime();
    cout << "Time taken: " << end_time - start_time << " secs" << endl;
    cout << "Iter time: " << end_time - iter_start_time << " secs" << endl;
    // cout << "Number of threads: " << omp_get_num_threads() << endl;

    // Output the results
    ofstream output;
    output.open("results2.txt");
    output << N << " " << K << endl;
    for (int i = 0; i < N; i++) {
        output << points[i].first[0] << " " <<  points[i].first[1] << " " <<  points[i].first[2] << " " <<  points[i].second << endl;
    }
    output.close();

    return 0;
}