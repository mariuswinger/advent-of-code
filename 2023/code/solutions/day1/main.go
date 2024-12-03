package main

import (
	"aoc/internal"
	"fmt"
	"strconv"
	"strings"
)

func ParseWord(word string) string {
	newString := strings.ReplaceAll(word, "one", "one1one")
	newString2 := strings.ReplaceAll(newString, "two", "two2two")
	newString3 := strings.ReplaceAll(newString2, "three", "three3three")
	newString4 := strings.ReplaceAll(newString3, "four", "four4four")
	newString5 := strings.ReplaceAll(newString4, "five", "five5five")
	newString6 := strings.ReplaceAll(newString5, "six", "six6six")
	newString7 := strings.ReplaceAll(newString6, "seven", "seven7seven")
	newString8 := strings.ReplaceAll(newString7, "eight", "eight8eight")
	newString9 := strings.ReplaceAll(newString8, "nine", "nine9nine")
	return newString9
}

func GetWordDigit(word string) int64 {
	var firstDigit int64 = -1
	var lastDigit int64 = 0
	for _, c := range word {
		if v, err := strconv.ParseInt(string(c), 10, 64); err == nil {
			if firstDigit == -1 {
				firstDigit = int64(v)
			}
			lastDigit = int64(v)
		}
	}
	return 10*firstDigit + lastDigit
}

func ParseInput() []string {
	return internal.ReadInput("day1.txt")
}

func SolvePart1() int64 {
	allStrings := ParseInput()
	var calibrationSum int64 = 0
	for _, word := range allStrings {
		wordDigit := GetWordDigit(word)
		if wordDigit > 0 {
			calibrationSum += wordDigit
		}
	}
	return calibrationSum
}

func SolvePart2() int64 {
	allStrings := ParseInput()
	var calibrationSum int64 = 0
	for _, word := range allStrings {
		wordDigit := GetWordDigit(ParseWord(word))
		if wordDigit > 0 {
			calibrationSum += wordDigit
		}
	}
	return calibrationSum
}

func main() {
	fmt.Printf("Solution for part 1: %d\n", SolvePart1())
	fmt.Printf("Solution for part 2: %d\n", SolvePart2())
}
