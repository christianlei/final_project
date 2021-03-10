package main

import (
	"driver/model"
	"fmt"
	"time"
)

func main(){
	start := time.Now()
	var data_clean int  = 1 + 1
	mid := time.Since(start)
	model.Log_reg()
	end := time.Since(start)
	fmt.Println("data cleaning runtime =", mid, data_clean)
	fmt.Println("log reg runtime =", end-mid)
}