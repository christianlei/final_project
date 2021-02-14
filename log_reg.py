import math
import random
import pandas as pd
import numpy as  np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def Cost(X_train, y_train, w, b):
	res = 0
	for i in range(len(X_train)):
		y = y_train[i]
		x = X_train[i]
		res += y*np.log(1/(1+math.exp(-w*x-b))) + (1-y)*np.log(1 - 1/(1+math.exp(-w*x-b)))
	return (-1/len(X_train))*res

def move_uphill(delta_E, T):
	return (random.random() < math.exp(delta_E/max(T, 0.000001)))

def simulatedAnnealing(X_train, y_train, iterations):
	curr_w = random.random()
	curr_b = random.random()
	current = (curr_w, curr_b)
	T = 1
	d = 0.99
	for i in range(iterations):
		T = T*d
		if T == 0:
			return current
		new_w = random.random()
		new_b = random.random()
		new = (new_w, new_b)
		delta_E = Cost(X_train, y_train, curr_w, curr_b) - Cost(X_train, y_train, new_w, new_b)
		if delta_E > 0:
			current = new
		else:
			if move_uphill(delta_E, T):
				# up hill bad direction
				current = new
			else:
				# stay the same
				current = current
	return current

def predict(model, X):
	predicted_list = []
	w = model[0]
	b = model[1]
	for i in range(len(X)):
		x = X[i]
		predicted_class = 1 if ( 1/(1+math.exp(-w*x-b)) >= 0 ) else 0
		predicted_list.append(predicted_class)
	return predicted_list

def calc_acc(predicted_labels, labels):
	total = 0
	for i in range(len(labels)):
		total += 1 if (predicted_labels[i] == labels[i]) else 0
	return total/(len(labels))

def main():
	df = pd.read_csv('bitcoin.csv')
	labels = df[['labels']]
	#print(labels)
	df.drop(['Unnamed: 0', 'Timestamp', 'labels'], axis=1, inplace=True)

	clip = math.floor((0.8)*len(df))
	cutoff = len(df)-30
	features_train = df.iloc[:clip, :].values
	labels_train = labels.iloc[:clip, :].values
	features_test = df.iloc[clip:cutoff, :].values
	labels_test = labels.iloc[clip:cutoff, :].values

	scaler = StandardScaler()
	scaler = scaler.fit(features_train)

	features_train_scaled = scaler.transform(features_train)
	features_test_scaled = scaler.transform(features_test)

	X_train = []
	y_train = []
	for i in range(len(features_train_scaled)):
		X_train.append(features_train_scaled[i, :])
		y_train.append(labels_train[i, :])

	X_train, y_train = np.array(X_train), np.array(y_train)

	X_test = []
	y_test = []
	for i in range(len(features_test_scaled)):
		X_test.append(features_test_scaled[i, :])
		y_test.append(labels_test[i, :])

	X_test, y_test = np.array(X_test), np.array(y_test)

	#Pseudo
	iterations = 1000
	model = simulatedAnnealing(X_train, y_train, iterations)
	predicted_labels = predict(model, X_test) #returns list of predicted labels
	model_acc = calc_acc(predicted_labels, y_test)
	print(model_acc)

	"""
	default_model = defaultLogisticRegression(X_train, y_train)
	default_res = predict(X_test, y_test)

	print(model_res)
	print(default_res)
	"""

if __name__ == '__main__':
	main() 