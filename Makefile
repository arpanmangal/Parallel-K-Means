ssequential: 
	g++ -std=c++11 -fopenmp -o seq kmeans1.cpp

sequential:
	g++ -std=c++11 -fopenmp -o sequential lab1_sequential.cpp main_sequential.c lab1_io.c

seqDebug:
	g++ -std=c++11 -g -fopenmp -o sequential lab1_sequential.cpp main_sequential.c lab1_io.c

omp:
	g++ -std=c++11 -fopenmp -o omp lab1_omp.cpp main_omp.c lab1_io.c

openmp:
	g++ -std=c++11 -fopenmp -o openmp kmeans2.cpp

clean: 
	rm -rf sequential omp *.out