
#include "myrqiea2.h"


void MyRQIEA2::run() {
	t = 0;
	int tmax = 5000;
	initialize();
	observe(); //
	evaluate(); //
	storebest(); //
	while (t < tmax) {
		printf("Generation %d\n", t);
		printf("bestval: %f\n", bestval);
		t++;
		observe();
		evaluate();
		storebest();
		update();
	}
}

#define Qij (Q + i * (5 * (chromlen/2)) + (5 * j))
#define Pij (P + i * (chromlen) + (2 * j))

void MyRQIEA2::initialize() {
	for (int i = 0; i < popsize; i++) {
		for (int j = 0; j < chromlen / 2; j++) {
			Qij[0] = 2. * M_PI * rand() / RAND_MAX - M_PI; // location
			Qij[1] = 2. * M_PI * rand() / RAND_MAX - M_PI; // location
			Qij[2] = 2. * M_PI * rand() / RAND_MAX; // orientation
			Qij[3] = 1. * rand() / RAND_MAX; // scale X
			Qij[4] = 1. * rand() / RAND_MAX; // scale Y
		}
	}
}

void MyRQIEA2::observe() {
	for (int i = 0; i < popsize; i++) {
		for (int j = 0; j < chromlen / 2; j++) {
			double u = 10. * Qij[3] * box_muller();
			double v = 10. * Qij[4] * box_muller();
			double theta = Qij[2] / (M_PI * 2) * 180 * M_PI / 180;
			double u2 = u * cos(theta) - v * sin(theta);
			double v2 = u * sin(theta) + v * cos(theta);
			u = u2;
			v = v2;
			u += Qij[0] * 100. / (M_PI * 2);
			v += Qij[1] * 100. / (M_PI * 2);
			Pij[0] = u;
			Pij[1] = v;
		}
	}
}

void MyRQIEA2::storebest() {
}

void MyRQIEA2::evaluate() {
}

void MyRQIEA2::update() {
}

/*
#include "cec2005.h"
#include "cec2013.h"
int main() {
	srand(time(0));
	srand(2);//time(0));
	int dim = 10;
	int popsize = 20;
	RQIEA *rQIEA = new RQIEA(dim, popsize);
	for (int i = 0; i < dim; i++) {
		rQIEA->bounds[i][0] = -100;
		rQIEA->bounds[i][1] = 100;
	}

	Problem<double,double> *fun = new CEC2013(1);
	// double x[2] = {-39.3, 58.8};
	// double val = fun->evaluator(x, 2);
	// printf("-> %f\n", val);
	// return 0;
	rQIEA->problem = fun;
	rQIEA->run();
	printf("Final bestval: %f\n", rQIEA->bestval);
	printf("Final best: ");
	for (int i = 0; i < dim; i++) {
		printf("%f, ", rQIEA->best[i]);
	}
	printf("\n");
}
*/
