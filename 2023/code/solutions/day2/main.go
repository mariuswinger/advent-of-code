package main

import (
	"aoc/internal"
	"fmt"
	"regexp"
	"strings"
)

const (
	maxRed   = 12
	maxGreen = 13
	maxBlue  = 14
)

type Round struct {
	red   int64
	green int64
	blue  int64
}

func (r Round) isValid() bool {
	return r.red <= maxRed && r.green <= maxGreen && r.blue <= maxBlue
}

func (r Round) power() int64 {
	return r.red * r.green * r.blue
}

type Game struct {
	id     int64
	rounds []Round
}

func (g Game) isValid() bool {
	for _, round := range g.rounds {
		if !round.isValid() {
			return false
		}
	}
	return true
}

func (g Game) minimumRequired() Round {
	var minRed, minGreen, minBlue int64 = 0, 0, 0
	for _, round := range g.rounds {
		if round.red > minRed {
			minRed = round.red
		}
		if round.green > minGreen {
			minGreen = round.green
		}
		if round.blue > minBlue {
			minBlue = round.blue
		}
	}
	return Round{
		red:   minRed,
		green: minGreen,
		blue:  minBlue,
	}
}

func ParseInput() [100]Game {
	allGameStrings := internal.ReadInput("day2.txt")
	var games [100]Game
	for i, gameString := range allGameStrings {
		games[i] = GameFromInputString(gameString)
	}
	return games
}

func GameFromInputString(gameString string) Game {
	gameIDString := strings.Split(gameString, ":")[0]
	gameRoundsString := strings.Split(gameString, ":")[1]
	gameID := internal.StrToInt(strings.Split(gameIDString, " ")[1])
	var gameRounds []Round
	for _, gameString := range strings.Split(gameRoundsString, ";") {
		gameRounds = append(gameRounds, RoundFromInputString(gameString))
	}
	return Game{
		id:     gameID,
		rounds: gameRounds,
	}
}

func RoundFromInputString(roundString string) Round {
	round := new(Round)
	re := regexp.MustCompile("(\\d+) (\\w+)")
	matches := re.FindAllStringSubmatch(roundString, -1)
	for _, match := range matches {
		count := match[1]
		color := match[2]
		switch color {
		case "red":
			round.red = internal.StrToInt(count)
		case "green":
			round.green = internal.StrToInt(count)
		case "blue":
			round.blue = internal.StrToInt(count)
		}
	}
	return *round
}

func SolvePart1() int64 {
	allGames := ParseInput()
	var gameIdSum int64 = 0
	for _, game := range allGames {
		if game.isValid() {
			gameIdSum += game.id
		}
	}
	return gameIdSum
}

func SolvePart2() int64 {
	allGames := ParseInput()
	var gamePowerSum int64 = 0
	for _, game := range allGames {
		gamePowerSum += game.minimumRequired().power()
	}
	return gamePowerSum
}

func main() {
	fmt.Printf("Solution for part 1: %d\n", SolvePart1())
	fmt.Printf("Solution for part 2: %d\n", SolvePart2())
}
