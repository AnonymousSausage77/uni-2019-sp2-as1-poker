#
# File : burja018_poker.py
# Author : John Bures
# Email ID : burja018
# Description : Assignment 1 -> 5 dice poker
# This is my own work as defined by the
# University's Academic Misconduct Policy.
#

import dice
import random

# size of the poker hand being played with
HAND_SIZE = 5
# number of faces on the dice used
DICE_FACES = 6
# smallest face on the dice
MIN_FACE = 1
# constant to represent an empty number
EMPTY = 0
# constant which represents a draw when figuring out who won
DRAW = None

# a list of each of the hands in order of their rank. The index of their position in this
# list correlates to how strong the hand is compared to any other hand.
# Therefore, ONE_PAIR with an index of 1, is weaker than FULL_HOUSE with an index of 3
HAND_RANK = ["Nothing Special", "One Pair", "Two Pair", "Three of a Kind", "Full House", "Four of a Kind",
			 "Five of a Kind"]

# indexes of the different hands in HAND_RANK
NOTHING = 0
ONE_PAIR = 1
TWO_PAIR = 2
THREE_OF_A_KIND = 3
FULL_HOUSE = 4
FOUR_OF_A_KIND = 5
FIVE_OF_A_KIND = 6

# indexes of different face frequencies
PAIRS_INDEX = 1
TRIPLES_INDEX = 2
QUADS_INDEX = 3
FIVES_OF_A_KIND_INDEX = 4


# Class to represent the various players playing.
# If this game of poker were to be scaled to host more players, new PokerPlayer objects could be created
# each holding their own unique hand and name variables, and handling their own functions.
class PokerPlayer(object):
	# constructor
	# 	name:	the string representation of the player's name
	def __init__(self, name):
		# sets the name of player, e.g. 'dealer', or 'player'
		self.__name = name
		# sets the the player's current hand, all players start without a hand
		self.__hand = None

	# displays a text representation of the player's hand using the dice.py
	def printToConsole(self):
		print(self.__name, "'s hand:", sep="")
		dice.display_hand(self.__hand, HAND_SIZE)
		print()

	# setter method for assigning the player a new hand
	# 	hand:	a list of dice integers to be set as the player's new hand
	def setHand(self, hand):
		self.__hand = hand

	# used to refer to the player's rank
	@property
	def rank(self):
		return rankHand(self.__hand)

	# displays the player's name in a 'win' message to the console
	def displayWinBanner(self):
		print("\n**", self.__name, "wins! **\n")

	# prints this player's hand rank text to the console, in the form: 'player_name' has 'hand_rank_string'
	def displayPlayersRank(self):
		print("--", self.__name, "has", end=' ')
		displayRank(self.rank)

	# compares this instance's hand against another player instance hand
	# displays the winner to the console, and returns the winner
	# 	anotherPlayer:	reference to another PokerPlayer object whose
	#					hand is to be compared against this instance hand
	def compareHandAgainst(self, anotherPlayer):
		# determines if this hand is better in which case return this instance
		if self.rank > anotherPlayer.rank:
			self.displayWinBanner()
			return self
		# if the other player is better, return them
		elif self.rank < anotherPlayer.rank:
			anotherPlayer.displayWinBanner()
			return anotherPlayer
		# if neither player is better, return nothing as DRAW
		else:
			print("\n** Draw! **\n")
			return DRAW


# Displays my UNI details.
def displayDetails():
	print("File\t\t: burja018_poker.py")
	print("Author\t\t: John Bures")
	print("Stud ID\t\t: 110258941")
	print("Email ID\t: burja018")
	print("This is my own work as defined by the\nUniversity's Academic Misconduct Policy.")


# Rolls a dice with a number of sides: creating a random integer between 1 and 6 inclusive,
# and then returns that number
def rollDie():
	return random.randint(MIN_FACE, DICE_FACES)


# generates a number of dice roll results and returns them as a list
# 	maxDice:	number of dice to be dealt in the hand, by default this is set as 5
def dealHand(maxDice=HAND_SIZE):
	return [rollDie() for index in range(maxDice)]


# takes a hand and ranks that hand from 0 to 6, 6 being a five of a kind, and 0 being nothing
# 	hand:		a player's hand - a list of integers, each representing the result of a dice roll
# 	maxDice:	the number of dice in each player's hand, should be the same as len(maxDice), default set to 5
def rankHand(hand, maxDice=HAND_SIZE):
	# a list of the number of each die face in the hand
	countedFaces = countFaces(hand)
	# a list of frequencies of different die faces
	countedPatterns = countPatterns(countedFaces, maxDice)

	# ranks the hand depending on how many patterns are within tha than,
	# this can be expressed as the following equasion:
    # if full house: 1+ 3*1 + 5*0 + 6*0
    # returns 4

    # if pair: 1 + 3*0 + 5*0 + 6*0
    # returns 1

    # if twopair: 2 + 3 + 5*0 + 6*0
    # returns 2

    # if five of a kind: 0 + 3*0 + 5*0 + 6*1
    # returns 6
	return countedPatterns[PAIRS_INDEX] \
		   + THREE_OF_A_KIND * countedPatterns[TRIPLES_INDEX] \
		   + FOUR_OF_A_KIND * countedPatterns[QUADS_INDEX] \
		   + FIVE_OF_A_KIND * countedPatterns[FIVES_OF_A_KIND_INDEX]


# Counts the frequency of each dice roll in a hand
# and puts that into a list, where the index represents the
# 'dice roll' in question, and the value represents the how many
# times that dice roll came up in a hand
# 	hand:	list of dice rolls that a player has in their hand
def countFaces(hand):
	# list of the frequency of each face that appeared in the hand
	faceFrequencies = [EMPTY] * DICE_FACES
	for faceValue in hand:
		faceFrequencies[faceValue - 1] += 1
	return faceFrequencies


# Goes through the frequency of each dice roll, and records
# the number of times each frequency of dice roll comes up.
# Therefore, if there was a pair of Three's,
# a pair of Sixes and a single Four, then:
# patterns[1] = 2   -> representing the two pairs
# patterns[0] = 1   -> representing the single four
# 	faceFrequencies:	list of the frequency of each face that appeared in the hand
# 	handSize:			the number of dice in the hand, should be the same as len(hand), by default 5
def countPatterns(faceFrequencies, handSize=HAND_SIZE):
	# list of the number of times each face frequency appeared
	patterns = [EMPTY] * handSize
	for diceFreq in faceFrequencies:
		if diceFreq > EMPTY:
			patterns[diceFreq - 1] += 1
	return patterns

# prints the string representation of a hand's rank to the screen
# 	rank:	integer representing the rank of a hand, eg. 4 represents a full house
def displayRank(rank):
	print(HAND_RANK[rank])


# prompts the user to play again.
# isFirstGame:	true if the player is playing the game for the first time
# 	yes:			input string required for the player intends to play again
# 	no:			input string required for the player to end the game
def promptPlayAgain(isFirstGame, yes="y", no="n"):
	# their current decision, none represents that the player has not yet
	# entered a valid input, otherwise, if true, the game will continue,
	# and if false, the game will end
	decision = None
	# keep asking player until a decision is made
	while decision is None:
		# user's string input, yet to be tested for validity
		choice = input(("\nWould you like to play dice poker" if isFirstGame else "\nPlay again") + " ["+yes+"|"+no+"]? ")
		# if the user does not enter a valid option, decision will remain none
		if choice != yes and choice != no:
			print("Please enter either ", yes, " or ", no, ".", sep="\'")
		else:
			# if the player's input matches yes, decision will be set to true, else false
			decision = choice == yes
	print()
	return decision

# runs a single round of the game, taking the two players that are playing
# Gives each player a hand, prints that hand, ranks them, and returns the winner
# 	player1: a PokerPlayer object
# 	player2: a PokerPlayer object
def doRound(player1, player2):
	# generates new hands
	player1.setHand(dealHand())
	player2.setHand(dealHand())

	print()  # adds a blank line

	# prints those hands to console
	player1.printToConsole()
	player2.printToConsole()

	# ranks those hands
	player1.displayPlayersRank()
	player2.displayPlayersRank()

	# returns which player wins
	return player1.compareHandAgainst(player2)


# uses the scoreboard to count the number of games played
# 	scoreboard:	a dictionary that holds a mapping of PokerPlayer's to their respective scores
def countGames(scoreboard):
	# the number of games played in total
	totalGames = 0
	for player, wins in scoreboard.items():
		totalGames += wins
	return totalGames


# displays a summery of the game to the screen based on the scoreboard
# 	scoreboard:	a dictionary of PokerPlayer objects to their scores
# 	user:			the PokerPlayer that the user represents, in this case 'player'
def displaySummary(scoreboard, user):
	# works out logistics for the games using the scoreboard
	# find the total number of games
	totalGames = countGames(scoreboard)
	# finds the total number of draws
	draws = scoreboard[DRAW]
	# finds the total number of wins
	wins = scoreboard[user]
	# finds the total numebr of losses
	losses = totalGames - (wins + draws)

	# do not print the game summary if the player has not played
	# breaking out of the function instead
	if totalGames == 0:
		print("\nNo worries... another time perhaps... :)\n")
		return

	# prints the game summery
	print("\nGame Summary\n============")
	print("You played", totalGames, "games")
	print("\t|--> Games won:", wins)
	print("\t|--> Games lost:", losses)
	print("\t|--> Games drawn:", draws)
	print("\nThanks for playing!")

# main entry point function for the game - the game starts here
def playGame():
	# displays my details to the screen
	displayDetails()

	# generates players and their hands
	user = PokerPlayer("Player")
	dealer = PokerPlayer("Dealer")

	# dictionary which tracks wins and draws,
	# binding the PokerPlayer objects to their respective scores
	scoreboard = {user: 0, dealer: 0, DRAW: 0}

	# keeps playing until the user says 'n'
	while promptPlayAgain(isFirstGame=countGames(scoreboard) == 0):

		# plays a round and assigns winner as the PokerPlayer object that wins
		winner = doRound(user, dealer)
		# increases the player's score on the scoreboard
		scoreboard[winner] += 1

	# once the game is over, displays wins and losses
	displaySummary(scoreboard, user)


# entry point
playGame()
