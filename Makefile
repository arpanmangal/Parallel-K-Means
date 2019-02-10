sequential:
	g++ -std=c++11 -fopenmp -o sequential lab1_sequential.cpp main_sequential.c lab1_io.c

seqDebug:
	g++ -std=c++11 -g -fopenmp -o sequential lab1_sequential.cpp main_sequential.c lab1_io.c

omp:
	g++ -std=c++11 -fopenmp -o omp lab1_omp.cpp main_omp.c lab1_io.c

pthread:
	g++ -std=c++11 -fopenmp -lpthread -o pthread lab1_pthread.cpp main_pthread.c lab1_io.c

clean: 
	rm -rf sequential omp pthread *.out