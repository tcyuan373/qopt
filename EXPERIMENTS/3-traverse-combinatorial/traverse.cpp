#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cstring>
#include <strings.h>

#include "framework.h"
#include "functions1d.h"
#include "sat.h"
#include "knapsack.h"


int main() {
#if 0
	if (false) {
		// schemata generator

		long int i, bound;
		int len = 15;
		char buf[len + 1];
		memset(buf, '\0', len + 1);
		bound = pow(3, len);
		for (i = 0; i < bound; i++) {
			dec2ternary(buf, i, len);
			int o = order(buf, len);
			if (o > 3 || o < 2) {
				continue;
			}
			int dl = deflenth(buf, len);
			if (dl > 2) {
				continue;
			}
			printf("%5d %s %2d %2d\n", i, buf, o, dl);
		}
		return 0;
	}

	if (true) {
		// traversal

		KnapsackProblem *k1 = new KnapsackProblem("../../problems/knapsack/knapsack-25.txt");
		// SAT *k1 = new SAT("../../problems/sat/random-25.cnf");
		//Functions1DProblem *k1 = new Functions1DProblem(3);

		int chromlen = 25;
		char buf[chromlen + 1];
		memset(buf, '\0', chromlen + 1);
		float *mem = new float[int(pow(2,chromlen))];
		long int topbound = pow(2,chromlen);
		for (long int i = 0; i < topbound; i++) {
			dec2bin(buf, i, chromlen);
			k1->repairer(buf, chromlen);
			float val = k1->evaluator(buf, chromlen);
			mem[i] = val;
			//printf("%5d %s %f\n", i, buf, val);
		}
		FILE *F = fopen("/tmp/k25-space", "w");
		fwrite(mem, sizeof(float), int(pow(2,chromlen)), F);
		fclose(F);
		return 0;
	}


#endif

	if (true) {
		// sorting (ranking)

		int chromlen = 15;
		long int best100[100]; // tablica, ktora ma zawierac ID tysiaca najlepszych rozwiazan
		float *mem = new float[int(pow(2,chromlen))];

		FILE *F = fopen("/var/tmp/sat15-space", "r");
		fread(mem, sizeof(float), int(pow(2, chromlen)), F);
		// printf("-> %f\n", mem[31743]);
		fclose(F);

		// poczatkowo do tablicy wrzucamy 100 pierwszych wartosci (ich ID)
		for (long int j = 0; j < 100; j++) {
			best100[j] = j;
		}

		for (long int i = 100; i < int(pow(2, chromlen)); i++) {
			// 1) znajdz w ktory element tablicy best100 wskazuje na najgorsza wartosc
			int worst_idx = 0;
			for (long int k = 1; k < 100; k++) {
				if (mem[best100[k]] < mem[best100[worst_idx]]) {
					worst_idx = k;
				}
			}
			// 2) sprawdz, czy wartosc i jest wieksza niz najgorsza ze wszystkich w best100
			if (mem[i] > mem[best100[worst_idx]]) {
				best100[worst_idx] = i;
			}
			continue;

			for (long int j = 0; j < 100; j++) {
				if (mem[i] > mem[best100[j]]) {
					worst_idx = 0;
					for (long int k = 1; k < 100; k++) {
						if (mem[best100[k]] < mem[best100[worst_idx]]) {
							worst_idx = k;
						}
					}
					best100[worst_idx] = i;
					break;
				}
			}
		}
		for (long int j = 0; j < 100; j++) {
			printf("%ld\n", best100[j]);
		}
		return 0;
	}

#if 0

	long int i;
	int chromlen = 25;
	char buf[chromlen + 1];
	char best[chromlen + 1];
	memset(buf, '\0', chromlen + 1);
	memset(best, '\0', chromlen + 1);
	//SAT *s3 = new SAT("../../contrib/SPY-1.2/formula.tmp.cnf");
	SAT *s3 = new SAT("../../problems/sat/random-20.cnf");
	int max = -1;
	printf("%d\n", s3->numclause);
	float *mem = new float[int(pow(2,chromlen))];
	long int topbound = pow(2,chromlen);
	for (i = 0; i < topbound; i++) {
		dec2bin(buf, i, chromlen);
		int val = s3->evaluator(buf, chromlen);
		mem[i] = val;
		if (val > max) {
			max = val;
			memcpy(best, buf, chromlen);
			// break;
		}
		//printf("%5d %s   ", i, buf);
		//printf("%d\n", val);
	}
	int occurences = 0;
	for (i = 0; i < topbound; i++) {
		if (mem[i] == max) {
			occurences++;
		}
	}
	fprintf(stderr, "max: %d\n", max);
	fprintf(stderr, "occurences: %d\n", occurences);
	fprintf(stderr, "%s   \n", best);
	//printf("aa\n");
#endif
}

