package model;

import java.io.*;
import java.lang.Math;
import java.util.Scanner;

public class LogReg{
	public static double cost(double X_train[], double y_train[],
		double w, double b, int len_X)
	{
		double cost = 0;
		double x;
		double y;
		for(int i = 0; i < len_X; i++){
			x = X_train[i];
			y = y_train[i];
			cost += y*Math.log(1/(1+Math.exp(-w*x))) +
				(1-y)*Math.log(1 - 1/(1+Math.exp(-w*x)));
		}
		return ((double)-1/(double)len_X)*cost;
	}

	// Return 1 means move uphill
	// Return 0 means remain the same
	public static int move_uphill(double delta_E, double T){
		if(Math.random() < Math.exp(-delta_E/T)){
			return 1;
		}
		else{
			return 0;
		}
	}

	public static void simulated_annealing(double w_b[], double X_train[],
		double y_train[], int iterations, int len_X)
	{
		w_b[0] = Math.random();
		w_b[1] = Math.random();
		double T = 1;
		double d = 0.99;
		double new_w;
		double new_b;
		double delta_E;
		for(int i = 0; i < iterations; i++){
			T = T * d;
			if(T == 0)
				return;
			new_w = Math.random();
			new_b = Math.random();
			delta_E = cost(X_train, y_train, w_b[0], w_b[1], len_X) -
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

	public static void predict(double predicted_labels[], double w_b[],
		double X[], int len_X)
	{
		double w = w_b[0];
		double b = w_b[1];
		double x;
		for(int i = 0; i < len_X; i++){
			x = X[i];
			if((1/(1+Math.exp(-w*x)) >= 0.5))
				predicted_labels[i] = 1;
			else
				predicted_labels[i] = 0;
			//System.out.println(1/(1+Math.exp(-w*x)));
			//System.out.println(predicted_labels[i]);
		}
		return;
	}

	public static double calc_acc(double predicted_labels[], double labels[],
		int len_labels)
	{
		int total = 0;
		for(int i = 0; i < len_labels; i++){
			total += (predicted_labels[i] == labels[i]) ? (1) : (0);
		}
		return (double)total/(double)len_labels;
	}

	public static void log_reg(){
		try{
			FileInputStream fis = new FileInputStream("bitcoin_clean_java.csv");
			Scanner sc = new Scanner(fis);
			String line;
			int num_days = -30;

			line = sc.nextLine();
			while(sc.hasNextLine()){
				line = sc.nextLine();
				num_days++;
			}

			fis.close();
			sc.close();

			fis = new FileInputStream("bitcoin_clean_java.csv");
			sc = new Scanner(fis);

			int train_size = (int)Math.floor(0.85*(double)num_days);
			int test_size = num_days - train_size;
			double X[] = new double[train_size];
			double y[] = new double[train_size];
			double X_test[] = new double[test_size];
			double y_test[] = new double[test_size];
			String tokens[] = new String[3];
			line = sc.nextLine();
			int i = 0;
			while(sc.hasNextLine() && i < num_days){
				line = sc.nextLine();
				tokens = line.split(",");
				if(i < train_size){
					X[i] = Double.parseDouble(tokens[1]);
					y[i] = Double.parseDouble(tokens[2]);
				}
				else{
					X_test[i-train_size] = Double.parseDouble(tokens[1]);
					y_test[i-train_size] = Double.parseDouble(tokens[2]);
				}

				i++;
			}

			double w_b[] = new double[2];
			int iterations = 1000;
			simulated_annealing(w_b, X, y, iterations, train_size);
			
			double predicted_labels[] = new double[train_size];
			predict(predicted_labels, w_b, X, train_size);
			
			double train_acc = calc_acc(predicted_labels, y, train_size);

			predict(predicted_labels, w_b, X_test, test_size);
			double test_acc = calc_acc(predicted_labels, y_test, test_size);
			
			System.out.println("training accuracy = "+train_acc);
			System.out.println("testing accuracy = "+test_acc);
		}
		catch(IOException e){
			e.printStackTrace();
		}

		/*
		double X[] = {-1, 2, -1, 2, -1, 2, -1, 2, -1, 2};
		double y[] = {0, 1, 0, 1, 0, 1, 0, 1, 0, 1};
		double w_b[] = new double[2];
		int iterations = 1000;
		int len_X = 10;

		simulated_annealing(w_b, X, y, iterations, len_X);

		double predicted_labels[] = new double[len_X];

		predict(predicted_labels, w_b, X, len_X);
		double accuracy = calc_acc(predicted_labels, y, len_X);
		
		System.out.println("accuracy = "+accuracy);
		*/

		return;
	}

}
