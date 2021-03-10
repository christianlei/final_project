package model

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"time"
	"math"
	"math/rand"
	"strings"
	"strconv"
)

const num_day = 3254
const train_size = 2765
const test_size = 489

func cost(X_train []float64, y_train []float64, w float64, b float64) float64{
	var res float64 = 0
	var i int
	var x float64
	var y float64
	var e float64
	len_X := len(X_train)
	for i = 0; i < len_X; i++ {
		x = X_train[i]
		y = y_train[i]
		if math.Exp(-w * x - b) > 0.000001{
			e = math.Exp(-w * x - b)
		}else{
			e = 0.000001
		}
		res += y * math.Log(1/(1+e)) + (1 - y) * math.Log(1 - 1 / (1 + e))
	}
	return (-1.0/float64(len_X))*res
}

func move_uphill(delta_E float64, T float64) bool{
	var t float64
	if T < 0.000001{
		t = 0.000001
	}else{
		t = T
	}
	return rand.Float64() < math.Exp(delta_E/t)
}

func simulatedAnnealing(w_b []float64, X_train []float64, y_train []float64, iterations int){
	w_b[0] = rand.Float64()
	w_b[1] = rand.Float64()
	var T float64 = 1.0
	var d float64 = 0.99
	var new_w float64
	var new_b float64
	var delta_E float64
	var i int
	for i = 0; i < iterations; i++{
		T = T * d
		new_w = rand.Float64()
		new_b = rand.Float64()
		delta_E = cost(X_train, y_train, w_b[0], w_b[1]) - cost(X_train, y_train, new_w, new_b)
		if delta_E > 0{
			w_b[0] = new_w
			w_b[1] = new_b
		}else{
			if move_uphill(delta_E, T){
				w_b[0] = new_w
				w_b[1] = new_b
			}
		}
	}
}

func predict(w_b []float64, predicted []float64, X []float64, len_X int){
	var x float64
	var i int
	for i = 0; i < len_X; i++{
		x = X[i]
		if 1.0/(1+math.Exp(-w_b[0]*x-w_b[1])) >= 0.5{
			predicted[i] = 1.0
		}else{
			predicted[i] = 0.0
		}
	}
}

func calc_acc(predicted []float64, labels []float64, len_labels int) float64{
	var total int = 0
	var i int
	for i = 0; i < len_labels; i++{
		if predicted[i] == labels[i]{
			total += 1
		}
	}
	return float64(total)/float64(len_labels)
}

func Log_reg(){
	file, err := os.Open("bitcoin_clean_go.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	X_train := make([]float64, train_size)
	y_train := make([]float64, train_size)
	X_test := make([]float64, test_size)
	y_test := make([]float64, test_size)

	var i int = 0
	scanner := bufio.NewScanner(file)
	scanner.Scan()
	for scanner.Scan() {
		col := strings.Split(scanner.Text(), ",")
		if i >= num_day{
			break
		}
		if i < train_size{
			X_train[i], err = strconv.ParseFloat(col[1], 64)
			y_train[i], err = strconv.ParseFloat(col[2], 64)
		}else{
			X_test[i-train_size], err = strconv.ParseFloat(col[1], 64)
			y_test[i-train_size], err = strconv.ParseFloat(col[2], 64)
		}
		i++
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	w_b := make([]float64, 2)
	var iterations int  = 1000
	rand.Seed(time.Now().Unix())
	simulatedAnnealing(w_b, X_train, y_train, iterations)
	predicted := make([]float64, train_size)
	predict(w_b, predicted, X_train, train_size)
	var train_acc float64 = calc_acc(predicted, y_train, train_size)
	predict(w_b, predicted, X_test, test_size)
	var test_acc float64 = calc_acc(predicted, y_test, test_size)
	fmt.Println("training accuracy =", train_acc)
	fmt.Println("testing accuracy =", test_acc)
}