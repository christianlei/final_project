#include "data_cleaner_manual.h"
#include "log_reg.h"
#include <time.h>

int main(){
	clock_t start, end, intermediate;
	start = clock();
	data_cleaner_manual();
	intermediate = clock();
	log_reg();
	end = clock();
	printf("total runtime = %f\n", ((double)(end-start))/CLOCKS_PER_SEC);
	printf("data cleaner runtime = %f\n", ((double)(intermediate-start))/CLOCKS_PER_SEC);
	printf("log reg runtime = %f\n", ((double)(end-intermediate))/CLOCKS_PER_SEC);
	return EXIT_SUCCESS;
}
