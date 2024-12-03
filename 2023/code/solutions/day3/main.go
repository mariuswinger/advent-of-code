package main

import (
	"aoc/internal"
	"errors"
	"fmt"
	"regexp"
)

type Index struct {
	x int64
	y int64
}

type PartIndex struct {
	xStart int64
	xEnd   int64
	y      int64
}

type Size struct {
	x int64
	y int64
}

type Schematic struct {
	rows    []string
	partMap map[PartIndex]int64
	size    Size
}

func CreateSchematic(input []string) Schematic {
	re := regexp.MustCompile("(\\d+)")
	var partMap map[PartIndex]int64
	partMap = make(map[PartIndex]int64)
	for yIndex, row := range input {
		rowMatches := re.FindAllStringIndex(row, -1)
		for _, match := range rowMatches {
			partIndex := PartIndex{
				xStart: int64(match[0]),
				xEnd:   int64(match[1]),
				y:      int64(yIndex),
			}
			partMap[partIndex] = internal.StrToInt(row[partIndex.xStart:partIndex.xEnd])
		}
	}
	return Schematic{
		rows:    input,
		partMap: partMap,
		size: Size{
			x: int64(len(input[0])),
			y: int64(len(input)),
		},
	}
}

func (s Schematic) onLeftEdge(p PartIndex) bool {
	return p.xStart == 0
}

func (s Schematic) onRightEdge(p PartIndex) bool {
	return p.xEnd == s.size.x
}

type Adjacent struct {
	values map[Index]string
}

func (a Adjacent) Concatenate() string {
	str := ""
	for _, v := range a.values {
		str += v
	}
	return str
}

func (a Adjacent) ContainsSymbol() bool {
	re := regexp.MustCompile("[^0-9.]")
	matches := re.FindAllString(a.Concatenate(), -1)
	if matches != nil {
		return true
	}
	return false
}

func (a Adjacent) GetGearIndex() (Index, error) {
	for k, v := range a.values {
		if v == "*" {
			return k, nil
		}
	}
	return Index{}, errors.New("No gear")
}

func (a Adjacent) SetLeftAdjacent(s Schematic, p PartIndex) Adjacent {
	value := "."
	currentIndex := Index{x: p.xStart - 1, y: p.y}
	if !s.onLeftEdge(p) {
		value = string(s.rows[currentIndex.y][currentIndex.x])
	}
	a.values[currentIndex] = value
	return a
}

func (a Adjacent) SetRightAdjacent(s Schematic, p PartIndex) Adjacent {
	value := "."
	currentIndex := Index{x: p.xEnd, y: p.y}
	if !s.onRightEdge(p) {
		value = string(s.rows[currentIndex.y][currentIndex.x])
	}
	a.values[currentIndex] = value
	return a
}

func (a Adjacent) SetAbove(s Schematic, p PartIndex) Adjacent {
	yIndex := p.y - 1
	for i := p.xStart - 1; i < p.xEnd+1; i++ {
		currentIndex := Index{x: i, y: yIndex}
		if i < 0 || yIndex < 0 || i == s.size.x {
			a.values[currentIndex] = "."
		} else {
			a.values[Index{x: i, y: yIndex}] = string(s.rows[yIndex][i])
		}
	}
	return a
}

func (a Adjacent) SetBelow(s Schematic, p PartIndex) Adjacent {
	yIndex := p.y + 1
	for i := p.xStart - 1; i < p.xEnd+1; i++ {
		currentIndex := Index{x: i, y: yIndex}
		if i < 0 || yIndex == s.size.y || i == s.size.x {
			a.values[currentIndex] = "."
		} else {
			a.values[Index{x: i, y: yIndex}] = string(s.rows[yIndex][i])
		}
	}
	return a
}

func (s Schematic) GetAdjacent(p PartIndex) Adjacent {
	adjacentValues := map[Index]string{}
	adjacent := Adjacent{values: adjacentValues}
	return adjacent.SetLeftAdjacent(s, p).SetRightAdjacent(s, p).SetAbove(s, p).SetBelow(s, p)
}

func SolvePart1() int64 {
	inputArray := internal.ReadInput("day3.txt")
	schematic := CreateSchematic(inputArray)
	var partNumberSum int64 = 0
	for index, partNumber := range schematic.partMap {
		adjacent := schematic.GetAdjacent(index)
		if adjacent.ContainsSymbol() {
			partNumberSum += partNumber
		}
	}
	return partNumberSum
}

func SolvePart2() int64 {
	inputArray := internal.ReadInput("day3.txt")
	schematic := CreateSchematic(inputArray)
	gearMap := map[Index][]PartIndex{}
	for index := range schematic.partMap {
		adjacent := schematic.GetAdjacent(index)
		gearIndex, notFound := adjacent.GetGearIndex()
		if notFound == nil {
			if _, ok := gearMap[gearIndex]; ok {
				gearMap[gearIndex] = append(gearMap[gearIndex], index)
			} else {
				gearMap[gearIndex] = []PartIndex{index}
			}
		}
	}
	var gearRatioSum int64 = 0
	for _, v := range gearMap {
		if len(v) == 2 {
			gearRatioSum += schematic.partMap[v[0]] * schematic.partMap[v[1]]
		}
	}
	return gearRatioSum
}

func main() {
	fmt.Printf("Solution for part 1: %d\n", SolvePart1())
	fmt.Printf("Solution for part 2: %d\n", SolvePart2())
}
