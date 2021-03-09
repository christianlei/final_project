package main

import (
	"strings"
	"fmt"
)

type Day struct {
	Timestamp string
	AveragePrice float64
	Bitcoins []Bitcoin 
	Label float64
	NumberOfBitcoin int
}

func newDay(timestamp string) Day {
	AveragePrice := 0.0
	bitcoins := make([]Bitcoin, 0)
	label := -1.0
	NumberOfBitcoin := 0
	d := Day { timestamp, AveragePrice, bitcoins, label, NumberOfBitcoin }
	return d
}

func addBitcoin(day Day, bitcoin Bitcoin) Day {
	day.Bitcoins = append(day.Bitcoins, bitcoin)
	day.NumberOfBitcoin = len(day.Bitcoins)
	return day 
}

func calculateAverageWeightedPrice(day Day) Day {
	var totalPrice float64 = 0.0
	for _, bitcoin := range day.Bitcoins {
		totalPrice += bitcoin.WeightPrice
	}
	day.AveragePrice = totalPrice / float64(day.NumberOfBitcoin)
	return day
}

func dayToString(day Day) string {
	var sb strings.Builder
	sb.WriteString(day.Timestamp)
	sb.WriteString(",")
	sb.WriteString(fmt.Sprintf("%f", day.AveragePrice))
	if (day.Label != -1) {
		sb.WriteString(",")
		sb.WriteString(fmt.Sprintf("%f",day.Label))
	}

	sb.WriteString("\n")
	return sb.String()
}