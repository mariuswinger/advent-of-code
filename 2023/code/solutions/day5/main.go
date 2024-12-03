package main

import (
	"aoc/internal"
	"bufio"
	"errors"
	"fmt"
	"os"
	"slices"
	"strings"
	"sync"
	"time"
)

type Range struct {
	// INC-INC
	start int64
	end   int64
}

func (r Range) Contains(i int64) bool {
	return r.start <= i && i <= r.end
}

type SourceToDestMap struct {
	// maps Source -> Dest
	mapping map[Range]Range
}

func (stdm SourceToDestMap) MapSourceToDest(i int64) int64 {
	for source, dest := range stdm.mapping {
		if source.Contains(i) {
			offset := i - source.start
			return dest.start + offset
		}
	}
	return i
}

type InputData struct {
	seedNumbers            []int64
	seedSoilMap            SourceToDestMap
	soilFertilizerMap      SourceToDestMap
	fertilizerWaterMap     SourceToDestMap
	waterLightMap          SourceToDestMap
	lightTemperatureMap    SourceToDestMap
	temperatureHumidityMap SourceToDestMap
	humidityLocationMap    SourceToDestMap
}

func (d InputData) MapSeedsToLocation(n int64) int64 {
	soilNumber := d.seedSoilMap.MapSourceToDest(n)
	fertilizerNumber := d.soilFertilizerMap.MapSourceToDest(soilNumber)
	waterNumber := d.fertilizerWaterMap.MapSourceToDest(fertilizerNumber)
	lightNumber := d.waterLightMap.MapSourceToDest(waterNumber)
	temperatureNumber := d.lightTemperatureMap.MapSourceToDest(lightNumber)
	humidityNumber := d.temperatureHumidityMap.MapSourceToDest(temperatureNumber)
	locationNumber := d.humidityLocationMap.MapSourceToDest(humidityNumber)
	return locationNumber
}

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

func InputDataFromFile(filename string) InputData {
	f, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	scanner.Scan()
	seedsLine := strings.FieldsFunc(scanner.Text(), Splitter)
	seeds := StringToIntList(seedsLine[1])
	// Empty line right after seeds:
	scanner.Scan()

	inputDataMap := map[string]SourceToDestMap{}
	for scanner.Scan() {
		header := strings.FieldsFunc(scanner.Text(), Splitter)[0]
		if !strings.Contains(header, "map") {
			panic(errors.New("Something wrong happened while parsing file."))
		}
		mapping := map[Range]Range{}
		for scanner.Scan() {
			line := scanner.Text()
			if len(line) == 0 {
				break
			}
			rangeList := StringToIntList(line)
			sourceRange := Range{start: rangeList[1], end: rangeList[1] + rangeList[2] - 1}
			destRange := Range{start: rangeList[0], end: rangeList[0] + rangeList[2] - 1}
			mapping[sourceRange] = destRange
		}
		inputDataMap[header] = SourceToDestMap{mapping: mapping}
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}
	return InputData{
		seedNumbers:            seeds,
		seedSoilMap:            inputDataMap["seed-to-soil map"],
		soilFertilizerMap:      inputDataMap["soil-to-fertilizer map"],
		fertilizerWaterMap:     inputDataMap["fertilizer-to-water map"],
		waterLightMap:          inputDataMap["water-to-light map"],
		lightTemperatureMap:    inputDataMap["light-to-temperature map"],
		temperatureHumidityMap: inputDataMap["temperature-to-humidity map"],
		humidityLocationMap:    inputDataMap["humidity-to-location map"],
	}
}

func SolvePart1() int64 {
	inputData := InputDataFromFile("data/day5.txt")
	mappedSeeds := []int64{}
	for _, n := range inputData.seedNumbers {
		mappedSeeds = append(mappedSeeds, inputData.MapSeedsToLocation(n))
	}
	return slices.Min(mappedSeeds)
}

func (i InputData) MapSeedRange(minMappedSeedRange chan int64, seedRange Range, wg *sync.WaitGroup) {
	seedCount := seedRange.end - seedRange.start + 1
	seedRangeId := "seedRange_" + internal.IntToStr(seedCount)
	fmt.Fprintf(os.Stderr, "DEBUGPRINT[14]: main.go:150: %s=%+v\n", seedRangeId, seedRange)
	fmt.Fprintf(os.Stderr, "DEBUGPRINT[14]: main.go:150: %s count: %+v\n", seedRangeId, seedCount)
	defer wg.Done()
	mappedSeeds := []int64{}
	start := time.Now()
	// This is horribly performance. Should probably split up ranges and/or work in reverse
	for n := seedRange.start; n <= seedRange.end; n++ {
		mappedSeeds = append(mappedSeeds, i.MapSeedsToLocation(n))
	}
	elapsed := time.Since(start)
	fmt.Fprintf(os.Stderr, "DEBUGPRINT[14]: main.go:150: %s elapsed seconds: %+v\n", seedRangeId, elapsed.Seconds())
	fmt.Fprintf(os.Stderr, "DEBUGPRINT[14]: main.go:150: %s time per seed: %+v\n", seedRangeId, elapsed.Seconds()/float64(seedCount))
	minMappedSeedRange <- slices.Min(mappedSeeds)
}

func SolvePart2() int64 {
	inputData := InputDataFromFile("data/day5.txt")

	seedRanges := []Range{}
	for i, n := range inputData.seedNumbers {
		if i%2 == 1 {
			continue
		}
		seedRanges = append(seedRanges, Range{start: n, end: n + inputData.seedNumbers[i+1] - 1})
	}

	minMappedSeedRange := make(chan int64, len(seedRanges))
	var wg sync.WaitGroup
	for _, seedRange := range seedRanges {
		wg.Add(1)
		go inputData.MapSeedRange(minMappedSeedRange, seedRange, &wg)
	}
	wg.Wait()
	close(minMappedSeedRange)

	minLocationRangeNumbers := []int64{}
	for val := range minMappedSeedRange {
		minLocationRangeNumbers = append(minLocationRangeNumbers, val)
	}

	return slices.Min(minLocationRangeNumbers)
}

func main() {
	fmt.Printf("Solution for day5 part 1: %d\n", SolvePart1())
	fmt.Printf("Solution for day5 part 2: %d\n", SolvePart2())
}
