sequential: 
	g++ -std=c++11 -fopenmp -o seq kmeans1.cpp

openmp:
	g++ -std=c++11 -fopenmp -o openmp kmeans2.cpp

clean: 
	rm -rf seq