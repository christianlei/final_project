package main

import (
	"driver/model"
	"fmt"
	"time"
)

func main(){
	start := time.Now()
	model.DataCleanerManual()
	mid := time.Since(start)
	model.Log_reg()
	end := time.Since(start)
	fmt.Println("data cleaning runtime =", mid)
	fmt.Println("log reg runtime =", end-mid)
}