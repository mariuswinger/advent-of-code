package internal

import (
	"os"
	"strconv"
	"strings"
)

func ReadInput(filename string) []string {
	filepath := "data/" + filename
	stringData := FileToString(filepath)
	rowCount := strings.Count(stringData, "\n")
	if stringData[len(stringData)-1] != '\n' {
		rowCount += 1
	}
	return strings.SplitN(stringData, "\n", rowCount)
}

func FileToString(filepath string) string {
	data, err := os.ReadFile(filepath)
	if err != nil {
		panic(err)
	}
	return string(data)
}

func StrToInt(numberString string) int64 {
	num, err := strconv.ParseInt(numberString, 10, 64)
	if err != nil {
		panic(err)
	}
	return num
}

func IntToStr(integer int64) string {
	return strconv.Itoa(int(integer))
}
