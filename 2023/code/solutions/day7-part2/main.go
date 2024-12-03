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
		return 1
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

var Joker = Card{rank: "J", value: 1}

func (c Card) String() string {
	return fmt.Sprintf("'%v'", c.rank)
}

// Hand consists of 5 cards and the bid amount for that hand
type Hand struct {
	cards         map[int]Card
	jokerCount    int
	highCardOrder int64
	typeOrder     int64
	bid           int64
}

func (h Hand) String() string {
	cards := ""
	for i := 0; i < 5; i++ {
		cards += strings.Trim(h.cards[i].String(), "'")
	}
	return fmt.Sprintf("{ cards='%s', jokerCount=%v, highCardOrder=%v, typeOrder=%v, bid=%v }", cards, h.jokerCount, h.highCardOrder, h.typeOrder, h.bid)
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

const (
	FiveOfAKind  int64 = 6
	FourOfAKind        = 5
	FullHouse          = 4
	ThreeOfAKind       = 3
	TwoPairs           = 2
	OnePair            = 1
	HighCard           = 0
)

func HandTypeOrder(cards map[int]Card) int64 {
	handCardCount := HandCardCount(cards)
	jokerCount := handCardCount[Joker]
	nonJokerCardCountList := []int64{}
	for card, v := range handCardCount {
		if card.value != 1 {
			nonJokerCardCountList = append(nonJokerCardCountList, int64(v))
		}
	}
	nonJokerCardCountSet := internal.FromSlice(nonJokerCardCountList)

	if nonJokerCardCountSet.Has(5) {
		return FiveOfAKind
	} else if nonJokerCardCountSet.Has(4) {
		// XXXX|B -> 4 of a kind
		// XXXX|J -> 5 of a kind
		if jokerCount == 1 {
			return FiveOfAKind
		}
		return FourOfAKind
	} else if nonJokerCardCountSet.Has(3) {
		// XXX|BC -> 3 of a kind
		// XXX|BB -> house
		// XXX|JJ -> 5 of a kind
		// XXX|JB -> four of a kind
		if jokerCount == 1 {
			return FourOfAKind
		} else if jokerCount == 2 {
			return FiveOfAKind
		} else {
			if nonJokerCardCountSet.Has(2) {
				return FullHouse
			} else {
				return ThreeOfAKind
			}
		}
	} else if nonJokerCardCountSet.Has(2) {
		// At least one pair
		pairCount := 0
		for _, i := range nonJokerCardCountList {
			if i == 2 {
				pairCount += 1
			}
		}
		if pairCount == 2 {
			if jokerCount == 1 {
				return FullHouse
			}
			return TwoPairs
		}
		// 1 pair:
		if jokerCount == 3 {
			return FiveOfAKind
		} else if jokerCount == 2 {
			return FourOfAKind
		} else if jokerCount == 1 {
			return ThreeOfAKind
		}
		return OnePair

	} else if jokerCount == 5 {
		return FiveOfAKind
	} else if jokerCount == 4 {
		return FiveOfAKind
	} else if jokerCount == 3 {
		return FourOfAKind
	} else if jokerCount == 2 {
		return ThreeOfAKind
	} else if jokerCount == 1 {
		return OnePair
	}
	return HighCard
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
	handsTypeOrder := HandTypeOrder(cards) * int64(math.Pow(10, 10))
	return Hand{cards: cards, jokerCount: strings.Count(strings.Join(ranks, ""), "J"), bid: bid, typeOrder: handsTypeOrder, highCardOrder: HighCardOrder(cards)}
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

func SolvePart2() int64 {
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

func main() {
	fmt.Printf("Solution for day7 part 2: %d\n", SolvePart2())
}
