#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/sysctl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

double cost(double X_train[], double y_train[], double w, double b, size_t len_X){
    double cost = 0;
	double x;
	double y;
    for(size_t i = 0; i < len_X; i++){
        x = X_train[i];
        y = y_train[i];
        cost += y*log(1/(1+exp(-w*x-b))) + (1-y)*log(1 - 1/(1+exp(-w*x-b)));
    }
    return ((double)-1/(double)len_X)*cost;
}

// Return 1 means move uphill
// Return 0 means remain the same
int move_uphill(double delta_E, double T){
    if((double)rand()/(double)RAND_MAX < exp(delta_E/T))
        return 1;
    else
        return 0;
}

void simulated_annealing(double w_b[], double X_train[], double y_train[],
    size_t iterations, size_t len_X)
{
    w_b[0] = (double)rand()/(double)RAND_MAX;
    w_b[1] = (double)rand()/(double)RAND_MAX;
    double T = 1;
    double d = 0.99;
    for(size_t i = 0; i < iterations; i++){
        T = T * d;
        if(T == 0)
            return;
        double new_w = (double)rand()/(double)RAND_MAX;
        double new_b = (double)rand()/(double)RAND_MAX;
        double delta_E = cost(X_train, y_train, w_b[0], w_b[1], len_X) -
            cost(X_train, y_train, new_w, new_b, len_X);
        if(delta_E > 0){
            w_b[0] = new_w;
            w_b[1] = new_b;
        }
        else{
            if(move_uphill(delta_E, T) == 1){
                w_b[0] = new_w;
                w_b[1] = new_b;
            }
        }
    }

    return;
}

void predict(double predicted_labels[], double w_b[], double X[], size_t len_X){
    double w = w_b[0];
    double b = w_b[1];
    double x;
    size_t i;
    for(i = 0; i < len_X; i++){
        x = X[i];
        if(1/(1+exp(-w*x-b)) >= 0.5)
            predicted_labels[i] = 1;
        else
            predicted_labels[i] = 0;
    }

    return;
}

double calc_acc(double predicted_labels[], double labels[], size_t len_labels){
    int total = 0;
    for(size_t i = 0; i < len_labels; i++){
        total += (predicted_labels[i] == labels[i]) ? (1) : (0);
    }
    return (double)total/(double)len_labels;
}

int log_reg(){
	FILE *fp;
	char *line;
	size_t len = 0;
	ssize_t read = 0;

	fp = fopen("bitcoin_clean_cpp.csv", "r");
	if(fp == NULL)
		return EXIT_FAILURE;
	
	//get first line
	read = getline(&line, &len, fp);

	int num_days = -30; //offset due to no labels in last 30 rows
	while((read = getline(&line, &len, fp)) != -1){\
		num_days++;
	}
	fclose(fp);

	int train_size = floor(0.85*num_days);
	int test_size = num_days-train_size;
	double X[train_size];
	double y[train_size];
	double X_test[test_size];
	double y_test[test_size];

	fp = fopen("bitcoin_clean_cpp.csv", "r");

	read = getline(&line, &len, fp);

	char *token;
	int i = 0;
	while((read = getline(&line, &len, fp)) != -1 && i < num_days){
		if(i < train_size){
			//get timestamp
			token = strtok(line, ",");
			//get weighted price
			token = strtok(NULL, ",");
			X[i] = atof(token);
			//get labels
			token = strtok(NULL, "\n");
			y[i] = atof(token);
		}
		else{
			//get timestamp
            token = strtok(line, ",");
            //get weighted price
            token = strtok(NULL, ",");
            X_test[i-train_size] = atof(token);
            //get labels
            token = strtok(NULL, "\n");
            y_test[i-train_size] = atof(token);
		}

		i++;
	}

	fclose(fp);
    if(line)
        free(line);

	double w_b[2];
	size_t iterations = 1000;
	simulated_annealing(w_b, X, y, iterations, (size_t)train_size);

	double predicted_labels[train_size];

	predict(predicted_labels, w_b, X, (size_t)train_size);
	double train_acc = calc_acc(predicted_labels, y, (size_t)train_size);
	
	predict(predicted_labels, w_b, X_test, (size_t)test_size);
	double test_acc = calc_acc(predicted_labels, y_test, (size_t)test_size);

	printf("training accuracy = %lf\n", train_acc);
	printf("testing accuracy = %lf\n", test_acc);

	return EXIT_SUCCESS;
}
