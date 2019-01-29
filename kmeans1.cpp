/** Code for sequential implementation of K-Means */
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <random>
#include <fstream>
using namespace std;

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

    // Shuffle the points
    // auto rng = default_random_engine {};
    // shuffle(begin(points), end(points), rng);
    
    // Initialisation
    for (int i = 0; i < K; i++) {
        centroids[i] = points[i].first;
    }

    /* initialize random seed: */
    srand (time(NULL));
    // Loop
    int iters = 1000;
    while (iters--) {
        // Assign each point to a centroid
        for (int i = 0; i < N; i++) {
            int minDist = distance(points[i].first, centroids[0]);
            points[i].second = 0;
            
            for (int j = 1; j < K; j++) {
                // Compute distance with jth centroid
                int dist = distance(points[i].first, centroids[j]);
                if (dist < minDist) {
                    minDist = dist;
                    points[i].second = j;
                }
            }
        }

        // Recompute the centroids
        vector<int> pointCount(K, 0); // Number of points alloted to kth centroid
        for (int j = 0; j < K; j++) {
            // Each centroid -> (0,0,0)
            centroids[j][0] = 0;
            centroids[j][1] = 0;
            centroids[j][2] = 0;
        }
        for (int i = 0; i < N; i++) {
            // Add point to corresponding centroid
            int c = points[i].second;
            pointCount[c]++;
            centroids[c][0] += points[i].first[0];
            centroids[c][1] += points[i].first[1];
            centroids[c][2] += points[i].first[2];
        }
        // for (int j = 0; j < K; j++) {
        //     cout << pointCount[j] << " ";
        // }
        // cout << endl;
        // return 0;
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


    // Output the results
    ofstream output;
    output.open("results1.txt");
    output << N << " " << K << endl;
    for (int i = 0; i < N; i++) {
        output << points[i].first[0] << " " <<  points[i].first[1] << " " <<  points[i].first[2] << " " <<  points[i].second << endl;
    }
    output.close();

    return 0;
}