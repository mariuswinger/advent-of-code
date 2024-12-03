package main

import (
	"aoc/internal"
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
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

func CardValue(c string) int64 {
	if internal.IsInt(c) {
		return internal.StrToInt(c)
	}
	switch c {
	case "T":
		return 10
	case "J":
		return 11
	case "Q":
		return 12
	case "K":
		return 13
	case "A":
		return 14
	default:
		return 0
	}
}

// Each card has a rank and numeric value for that rank
type Card struct {
	rank  string
	value int64
}

func (c Card) String() string {
	return fmt.Sprintf("'%v'", c.rank)
}

// Hand consists of 5 cards and the bid amount for that hand
type Hand struct {
	cards         map[int]Card
	highCardOrder int64
	typeOrder     int64
	bid           int64
}

func (h Hand) String() string {
	cards := ""
	for _, v := range h.cards {
		cards += strings.Trim(v.String(), "'")
	}
	return fmt.Sprintf("{ cards='%s', highCardOrder=%v, typeOrder=%v, bid=%v }", cards, h.highCardOrder, h.typeOrder, h.bid)
}

// PRIMARY ORDER: 5 of a kind -> 4 of a kind -> full house -> 3 of a kind -> two pairs -> one pair -> high card
// SECONDARY ORDER: compare high cards in order from 0->4
func (h Hand) Order() int64 {
	return h.highCardOrder + h.typeOrder
}

func HandCardCount(cards map[int]Card) map[Card]int {
	handCardCount := map[Card]int{}
	for _, v := range cards {
		_, ok := handCardCount[v]
		if ok {
			handCardCount[v] = handCardCount[v] + 1
		} else {
			handCardCount[v] = 1
		}
	}
	return handCardCount
}

func HighCardOrder(cards map[int]Card) int64 {
	order := int64(0)
	for i, v := range cards {
		order += v.value * int64(math.Pow(10, float64(8-2*i)))
	}
	return order
}

func HandTypeOrder(cards map[int]Card) int64 {
	handCardCount := HandCardCount(cards)
	handCardCountList := []int64{}
	for _, v := range handCardCount {
		handCardCountList = append(handCardCountList, int64(v))
	}
	handCardCountSet := internal.FromSlice(handCardCountList)

	if handCardCountSet.Has(5) {
		return 60000000000
	} else if handCardCountSet.Has(4) {
		return 50000000000
	} else if handCardCountSet.Has(3) {
		if handCardCountSet.Has(2) {
			return 40000000000
		} else {
			return 30000000000
		}
	} else if handCardCountSet.Has(2) {
		// At least one pair
		pairCount := 0
		for _, i := range handCardCountList {
			if i == 2 {
				pairCount += 1
			}
		}
		if pairCount == 2 {
			return 20000000000
		}
		return 10000000000
	} else {
		return 0
	}
}

func HandFromInputLine(l []string) Hand {
	ranks := strings.Split(l[0], "")
	bid := internal.StrToInt(l[1])
	cards := map[int]Card{
		0: {rank: ranks[0], value: CardValue(ranks[0])},
		1: {rank: ranks[1], value: CardValue(ranks[1])},
		2: {rank: ranks[2], value: CardValue(ranks[2])},
		3: {rank: ranks[3], value: CardValue(ranks[3])},
		4: {rank: ranks[4], value: CardValue(ranks[4])},
	}
	handsTypeOrder := HandTypeOrder(cards)
	return Hand{cards: cards, bid: bid, typeOrder: handsTypeOrder, highCardOrder: HighCardOrder(cards)}
}

func InputDataFromFile(filename string) []Hand {
	f, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)

	hands := []Hand{}
	for scanner.Scan() {
		line := strings.Fields(scanner.Text())
		hands = append(hands, HandFromInputLine(line))
	}
	return hands
}

// Game has rank based on the order of the hands in the game, from 1 to the number of hands
type Game struct {
	hands map[int]Hand
}

func (g Game) TotalWinnings() int64 {
	totalWinnings := int64(0)
	for k, v := range g.hands {
		totalWinnings += int64(k) * v.bid
	}
	return totalWinnings
}

func SolvePart1() int64 {
	hands := InputDataFromFile("data/day7.txt")

	// sort hands by rank:
	sort.Slice(hands, func(i, j int) bool { return hands[i].Order() < hands[j].Order() })
	gameMap := map[int]Hand{}
	for i, hand := range hands {
		gameMap[i+1] = hand
	}
	game := Game{hands: gameMap}
	return game.TotalWinnings()
}

//	func SolvePart2() int64 {
//		races := InputDataFromFile("data/day6.txt")
//		times := []string{}
//		records := []string{}
//		for _, race := range races {
//			times = append(times, internal.IntToStr(race.time))
//			records = append(records, internal.IntToStr(race.record))
//		}
//		race := Race{time: internal.StrToInt(strings.Join(times, "")), record: internal.StrToInt(strings.Join(records, ""))}
//		waysToWin := race.WaysToWinCount()
//		return waysToWin
//	}
func main() {
	fmt.Printf("Solution for day7 part 1: %d\n", SolvePart1())
	// fmt.Printf("Solution for day5 part 2: %d\n", SolvePart2())
}
