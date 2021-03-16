import math
import random
import numpy as np


def Cost(X_train, y_train, w, b):
    res = 0
    for i in range(len(X_train)):
        y = y_train[i]
        x = X_train[i]
        res += y * np.log(1 / (1 + max(math.exp(-w * x - b), 0.000001))) + (1 - y) * np.log(
        	1 - 1 / (1 + max(math.exp(-w * x - b), 0.000001)))
    return (-1 / len(X_train)) * res


def move_uphill(delta_E, T):
    return random.random() < math.exp(delta_E / max(T, 0.000001))


def simulatedAnnealing(X_train, y_train, iterations):
    curr_w = random.random()
    curr_b = random.random()
    current = (curr_w, curr_b)
    T = 1
    d = 0.99
    for i in range(iterations):
        T = T * d
        if T == 0:
            return current
        new_w = random.random()
        new_b = random.random()
        new = (new_w, new_b)
        delta_E = Cost(X_train, y_train, curr_w, curr_b) - Cost(
            X_train, y_train, new_w, new_b
        )
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
        predicted_class = 0
        if (1 / (1 + math.exp(-w * x - b)) >= 0.5):
        	predicted_class = 1
        else:
        	predicted_class = 0
        predicted_list.append(predicted_class)
    return predicted_list


def calc_acc(predicted_labels, labels):
    total = 0
    for i in range(len(labels)):
        total += 1 if (predicted_labels[i] == labels[i]) else 0
    return total / (len(labels))


def log_reg():
    file = open("bitcoin_clean_python.csv", "r")
    Lines = file.readlines()
    col = []

    # remove first line which has column names
    Lines.remove(Lines[0])

    clip = math.floor((0.85) * (len(Lines)-30))
    begin = 0
    cutoff = len(Lines) - 30

    X_train = []
    y_train = []
    X_test = []
    y_test = []

    i = 0
    while(i < cutoff):
    	col = (Lines[i].strip()).split(",")
    	if(i < clip):
    		X_train.append(float(col[1]))
    		y_train.append(float(col[2]))
    	else:
    		X_test.append(float(col[1]))
    		y_test.append(float(col[2]))
    	i += 1

    iterations = 1000
    model = simulatedAnnealing(X_train, y_train, iterations)
    predicted_labels = predict(model, X_train)# returns list of predicted labels
    train_acc = calc_acc(predicted_labels, y_train)
    predicted_labels = predict(model, X_test)
    test_acc = calc_acc(predicted_labels, y_test)
    print("training accuracy =", train_acc)
    print("testing accuracy =", test_acc)