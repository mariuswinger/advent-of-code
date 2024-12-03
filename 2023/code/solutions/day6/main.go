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
	return c == ':'
}

func StringToIntList(s string) []int64 {
	out := []int64{}
	for _, n := range strings.Fields(s) {
		out = append(out, internal.StrToInt(strings.Trim(n, " ")))
	}
	return out
}

func InputDataFromFile(filename string) []Race {
	f, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	scanner.Scan()
	timesLine := strings.FieldsFunc(scanner.Text(), Splitter)
	times := StringToIntList(timesLine[1])

	scanner.Scan()
	recordsLine := strings.FieldsFunc(scanner.Text(), Splitter)
	records := StringToIntList(recordsLine[1])

	return []Race{
		{time: times[0], record: records[0]},
		{time: times[1], record: records[1]},
		{time: times[2], record: records[2]},
		{time: times[3], record: records[3]},
	}
}

type Race struct {
	time   int64
	record int64
}

func (r Race) TravelledDistance(time int64) int64 {
	// Travelled distance is total distance T minus charging time C times speed C: (T-C)*C
	return (r.time - time) * time
}

func TimesBinarySearch(times []int64, race Race) []int64 {
	listLength := len(times)
	if listLength == 1 {
		return times
	}
	halfLength := int64(math.Floor(float64((listLength + 1) / 2)))
	left := times[:halfLength]
	right := times[halfLength:]
	leftMaxTravelledDistance := race.TravelledDistance(left[len(left)-1])
	if leftMaxTravelledDistance <= race.record {
		return TimesBinarySearch(right, race)
	} else {
		return TimesBinarySearch(left, race)
	}
}

func (r Race) WaysToWinCount() int64 {
	timesToCheck := []int64{}
	for i := int64(1); i <= int64(math.Ceil(float64((r.time+1)/2))); i++ {
		timesToCheck = append(timesToCheck, i)
	}
	firstTimeToBeatRecord := TimesBinarySearch(timesToCheck, r)[0]
	// Add 1 since charging time of 0 counts:
	return r.time + 1 - 2*firstTimeToBeatRecord
}

func SolvePart1() int64 {
	races := InputDataFromFile("data/day6.txt")
	totalWaysToWin := int64(1)
	for _, race := range races {
		waysToWinRace := race.WaysToWinCount()
		totalWaysToWin *= waysToWinRace
	}
	return totalWaysToWin
}

func SolvePart2() int64 {
	races := InputDataFromFile("data/day6.txt")
	times := []string{}
	records := []string{}
	for _, race := range races {
		times = append(times, internal.IntToStr(race.time))
		records = append(records, internal.IntToStr(race.record))
	}
	race := Race{time: internal.StrToInt(strings.Join(times, "")), record: internal.StrToInt(strings.Join(records, ""))}
	waysToWin := race.WaysToWinCount()
	return waysToWin
}

func main() {
	fmt.Printf("Solution for day6 part 1: %d\n", SolvePart1())
	fmt.Printf("Solution for day6 part 2: %d\n", SolvePart2())
}
