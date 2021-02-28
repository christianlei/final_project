#include "data_cleaner_manual.h"
#include "log_reg.h"
#include <time.h>

int main(){
	clock_t start, end;
	start = clock();
	data_cleaner_manual();
	log_reg();
	end = clock();
	printf("runtime = %f\n", ((double)(end-start))/CLOCKS_PER_SEC);

	return EXIT_SUCCESS;
}
