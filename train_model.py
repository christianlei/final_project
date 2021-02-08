import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras import optimizers
import sys

num_layers = [2, 3, 3, 5, 5,
              4, 5, 4, 5, 6,
              5, 5, 7, 5, 5]

drop = [[0.37, 0.55, 0.00, 0.00, 0.00, 0.00, 0.00],
        [0.22, 0.22, 0.50, 0.00, 0.00, 0.00, 0.00],
        [0.25, 0.25, 0.60, 0.00, 0.00, 0.00, 0.00],
        [0.30, 0.30, 0.30, 0.25, 0.50, 0.00, 0.00],	
        [0.20, 0.20, 0.20, 0.25, 0.50, 0.00, 0.00],	
        [0.15, 0.15, 0.15, 0.00, 0.00, 0.00, 0.00],
        [0.15, 0.15, 0.15, 0.15, 0.00, 0.00, 0.00],	 
        [0.15, 0.15, 0.15, 0.00, 0.00, 0.00, 0.00],	 
        [0.15, 0.15, 0.15, 0.15, 0.00, 0.00, 0.00],	 
        [0.15, 0.15, 0.15, 0.15, 0.15, 0.00, 0.00],
        [0.10, 0.10, 0.10, 0.10, 0.20, 0.10, 0.10],
        [0.10, 0.10, 0.10, 0.10, 0.20, 0.10, 0.10],
        [0.10, 0.10, 0.10, 0.10, 0.20, 0.10, 0.10],
        [0.10, 0.10, 0.10, 0.10, 0.20, 0.10, 0.10],	  
        [0.10, 0.10, 0.10, 0.10, 0.20, 0.10, 0.10]]

neurons = [[90, 7],
           [60, 50, 40], 
           [65, 50, 50],
           [90, 90, 90, 50, 50],
           [60, 55, 55, 40, 40],
           [50, 50, 50, 50],
           [25, 25, 25, 25, 25],
           [25, 25, 25, 25],
           [50, 50, 50, 50, 50],
           [70, 70, 70, 70, 70, 70],
           [50, 60, 70, 50, 40],
           [50, 60, 70, 50, 40],
           [50, 60, 70, 50, 40, 20, 20],
           [50, 60, 70, 50, 40],
           [50, 60, 70, 50, 40]]

test_results = []

df = pd.read_csv('bitcoin.csv')
labels = df[['labels']]
df.drop(['Unnamed: 0', 'Timestamp', 'labels'], axis=1, inplace=True)
#labels.drop(['Unnamed: 0', 'Timestamp'], axis = 1, inplace=True)

sys.stdout = open("BitcoinResults.txt","w+")
fd = open("Test.txt", "w+")
# f = open(market[ind]+"Results.txt","w+")
print("Bitcoin Trials:*******************************************\n")

# Split train test data by %80. Split training data and validation by %30.
clip = math.floor((0.8)*len(df))
features_train = df.iloc[:clip, :].values
labels_train = labels.iloc[:clip, :].values
features_test = df.iloc[clip:, :].values
labels_test = labels.iloc[clip:, :].values

scaler = StandardScaler()
scaler = scaler.fit(features_train)

features_train_scaled = scaler.transform(features_train)
features_test_scaled = scaler.transform(features_test)

# Define LSTM step size.
step_size = 60
validation_clip = math.floor((0.72)*len(features_train))

X_train = []
y_train = []
for i in range(step_size, validation_clip):
	X_train.append(features_train_scaled[i-step_size:i, :])
	y_train.append(labels_train[i, :])

X_train, y_train = np.array(X_train), np.array(y_train)
#y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1], 1))

X_val = []
y_val = []
for i in range(validation_clip, len(features_train)):
	X_val.append(features_train_scaled[i-step_size:i, :])
	y_val.append(labels_train[i, :])

X_val, y_val = np.array(X_val), np.array(y_val)
#y_val = np.reshape(y_val, (y_val.shape[0], y_val.shape[1], 1))

X_test = []
y_test = []
for i in range(step_size, len(features_test)):
	X_test.append(features_test_scaled[i-step_size:i, :])
	y_test.append(labels_test[i, :])

X_test, y_test = np.array(X_test), np.array(y_test)
#y_test = np.reshape(y_test, (y_test.shape[0], y_test.shape[1], 1))

sgd = optimizers.SGD(lr=0.01, clipvalue=1)

for j in range(1):
	layers = num_layers[j]
	neur   = neurons[j]
	dr     = drop[j]

	regressor = Sequential()

	regressor.add(LSTM(units = neur[0], return_sequences = True,
		input_shape = (X_train.shape[1], X_train.shape[2])))
	regressor.add(Dropout(dr[0]))

	for i in range(1, layers):
		if(i == layers-1):
			regressor.add(LSTM(units = neur[i], return_sequences = False))
		else:
			regressor.add(LSTM(units = neur[i], return_sequences = True))
		regressor.add(Dropout(dr[i]))
	
	regressor.add(Dense(units = 1, activation = 'sigmoid'))

	regressor.compile(optimizer = 'sgd', loss = 'binary_crossentropy',
		metrics = ['accuracy'])


	sys.stdout = sys.__stdout__
	history = regressor.fit(X_train, y_train, epochs = 120,
		batch_size = 32, validation_data = (X_val, y_val), shuffle = False)

	train_loss, train_acc = regressor.evaluate(X_train, y_train)
	test_loss, test_acc = regressor.evaluate(X_test, y_test)
	print('Success', file=fd)

	test_results.append(test_acc)

	sys.stdout = open("BitcoinResults.txt","a")
	print('Model', j+1, ':', 'Training set accuracy:', train_acc)
	print('Model', j+1, ':', 'Test set accuracy:', test_acc)
	print('\n')

	plt.plot(history.history['acc'], label='train')
	plt.plot(history.history['val_acc'], label='val')
	plt.legend()
	plt.title('Binary Crossentropy: Train vs. Val')
	plt.xlabel('epoch')
	plt.ylabel('accuracy')
	plt.savefig('BitcoinModel'+str(j+1)+'.png', bbox_inches='tight')

	regressor = None

print('Success', file=fd)
"""
avg_test_results = []
for i in range(15):
	sum = 0
	for j in range(len(test_results)):
		sum = sum + test_results[j][i]
	sum = sum/3
	avg_test_results.append(sum)

sys.stdout = open("avgResults.txt","w+")
for i in range(15):
	print("Model", i+1, " ", avg_test_results[i], "\n")

print("\n")
print("Top Results:\n")
avg_test_results.sort()
avg_test_results.reverse()
for i in range(3):
	print(avg_test_results[i], "\n")
"""