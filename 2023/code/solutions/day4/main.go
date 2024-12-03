package main

import (
	"aoc/internal"
	"bufio"
	"fmt"
	"math"
	"os"
	"strings"
)

func Splitter(c rune) bool {
	return c == ':' || c == '|'
}

func SolvePart1() int64 {
	f, err := os.Open("data/day4.txt")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	var totalPoints int64 = 0
	scanner := bufio.NewScanner(f)

	for scanner.Scan() {
		line := strings.FieldsFunc(scanner.Text(), Splitter)
		winningNumbers := []int64{}
		for _, n := range strings.Fields(line[1]) {
			winningNumbers = append(winningNumbers, internal.StrToInt(strings.Trim(n, " ")))
		}
		winningNumberSet := internal.FromSlice(winningNumbers)
		cardNumbers := []int64{}
		for _, n := range strings.Fields(line[2]) {
			cardNumbers = append(cardNumbers, internal.StrToInt(n))
		}
		cardNumberSet := internal.FromSlice(cardNumbers)
		commonNumberSet := winningNumberSet.Intersect(cardNumberSet)
		commonNumberCount := commonNumberSet.Length()
		if commonNumberCount >= 1 {
			cardPoints := int64(math.Pow(2, float64(commonNumberSet.Length()-1)))
			totalPoints += cardPoints
		}

	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}
	return totalPoints
}

func SolvePart2() int64 {
	f, err := os.Open("data/day4.txt")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	cardCountMap := map[int64]int64{}
	for i := range [213]int64{} {
		cardCountMap[int64(i+1)] = 1
	}
	scanner := bufio.NewScanner(f)
	var lineCount int64 = 1
	for scanner.Scan() {
		line := strings.FieldsFunc(scanner.Text(), Splitter)
		winningNumbers := []int64{}
		for _, n := range strings.Fields(line[1]) {
			winningNumbers = append(winningNumbers, internal.StrToInt(strings.Trim(n, " ")))
		}
		winningNumberSet := internal.FromSlice(winningNumbers)
		cardNumbers := []int64{}
		for _, n := range strings.Fields(line[2]) {
			cardNumbers = append(cardNumbers, internal.StrToInt(n))
		}
		cardNumberSet := internal.FromSlice(cardNumbers)
		commonNumberSet := winningNumberSet.Intersect(cardNumberSet)
		commonNumberCount := commonNumberSet.Length()
		for i := int64(0); i < commonNumberCount; i++ {
			cardCountMap[int64(lineCount+1+i)] += cardCountMap[lineCount]
		}
		lineCount += 1
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}
	var totalCardCount int64 = 0
	for _, v := range cardCountMap {
		totalCardCount += v
	}
	return totalCardCount
}

func main() {
	fmt.Printf("Solution for day4 part 1: %d\n", SolvePart1())
	fmt.Printf("Solution for day4 part 2: %d\n", SolvePart2())
}
