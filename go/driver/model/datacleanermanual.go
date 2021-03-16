package model

import (
	"os"
	"bufio"
	"strings"
	// "fmt"
	"io"
	"strconv"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func DataCleanerManual() {
	var firstDay = false
	var parseHeader = false
	var sb strings.Builder
	var day Day
	var inputFileName = "bitcoin_raw.csv"
	var outputFileName = "bitcoin_clean_go.csv"
	var firstDateToParse = 1325376000
	var thirtyDayBuffer []Day = make([]Day, 0)

	inFile, err := os.Open(inputFileName)
	check(err)

	outFile, err := os.Create(outputFileName)
	check(err)

	reader := bufio.NewReader(inFile)
	var line string
	for {
		line, err = reader.ReadString('\n')
		if err != nil {
            if err == io.EOF {
                break
            }
		}
		line = line[:len(line)-1]
		rowSlice := strings.Split(line, ",")

		if !parseHeader {
			sb.WriteString(rowSlice[0])
			sb.WriteString(",")
			sb.WriteString(rowSlice[7])
			sb.WriteString(",label")
			sb.WriteString("\n")
			parseHeader = true
			_, err := outFile.WriteString(sb.String())
			check(err)
			sb.Reset()
			continue
		}

		if !firstDay {
			dayValue, err := strconv.Atoi(rowSlice[0])
			check(err)
			if (contains(rowSlice, "NaN") || (dayValue < firstDateToParse)) {
				continue
			}
			bitcoin := NewBitcoin(rowSlice[0], rowSlice[7])
			day = newDay(bitcoin.Timestamp)
			day = addBitcoin(day, bitcoin)

			if err != nil {
				panic (err)
			}
			firstDay = true
			continue
		}

		if contains(rowSlice, "NaN") {
			continue
		}
		bitcoin := NewBitcoin(rowSlice[0], rowSlice[7])
		if bitcoin.Timestamp != day.Timestamp {
			var returnedDay Day
			day = calculateAverageWeightedPrice(day)
			returnedDay, thirtyDayBuffer = addAndRetrieveDay(day, thirtyDayBuffer)
			if returnedDay.Timestamp != "" {
				if returnedDay.AveragePrice <= day.AveragePrice {
					returnedDay.Label = 1.0
				} else {
					returnedDay.Label = 0.0
				}
			}
			if returnedDay.Timestamp != "" {
				_, err := outFile.WriteString(dayToString(returnedDay))
				check(err)
			}
			day = newDay(bitcoin.Timestamp)
		}
		day = addBitcoin(day, bitcoin)
	}
	day = calculateAverageWeightedPrice(day)
	thirtyDayBuffer = append(thirtyDayBuffer, day)
	returnedDay, thirtyDayBuffer := retrieveDay(thirtyDayBuffer)
	for (returnedDay.Timestamp != "") {
		_, err := outFile.WriteString(dayToString(returnedDay))
		check(err)
		returnedDay, thirtyDayBuffer = retrieveDay(thirtyDayBuffer)
	}
}

func addAndRetrieveDay(day Day, thirtyDayBuffer []Day) (Day, []Day) {
	thirtyOne := 31
	thirtyDayBuffer = append(thirtyDayBuffer, day)
	var dayToReturn = newDay("")
	if len(thirtyDayBuffer) == thirtyOne {
		dayToReturn, thirtyDayBuffer = thirtyDayBuffer[0], thirtyDayBuffer[1:]
	}
	return dayToReturn, thirtyDayBuffer
}

func retrieveDay(thirtyDayBuffer []Day) (Day, []Day) {
	var dayToReturn = newDay("")
	if len(thirtyDayBuffer) != 1 {
		dayToReturn, thirtyDayBuffer = thirtyDayBuffer[0], thirtyDayBuffer[1:]
	}
	return dayToReturn, thirtyDayBuffer
}

func contains(s []string, str string) bool {
	for _, v := range s {
		if v == str {
			return true
		}
	}

	return false
}