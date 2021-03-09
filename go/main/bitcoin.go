package main

import (
	"time"
	"strconv"
)

type Bitcoin struct {

	Timestamp string
	WeightPrice float64

}

func NewBitcoin(timeStamp string, weightPrice string) Bitcoin {
	timeStampInt, err := strconv.ParseInt(timeStamp, 10, 64)
	check(err)
	var timestampUnformatted = time.Unix(timeStampInt, 0).UTC()
	var timestampFormatted = timestampUnformatted.Format("2006-01-02")
	weightPriceFloat, err := strconv.ParseFloat(weightPrice, 64)
	e := Bitcoin {timestampFormatted, weightPriceFloat}
	return e
}