from enum import Enum, IntEnum

class Suit(Enum):
	HEARTS = "\u2665"
	DIAMONDS = "\u2666"
	SPADES = "\u2660"
	CLUBS = "\u2663"

	def __str__(self) -> str:
		return self.value

class Rank(IntEnum):
	ACE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	SIX = 6
	SEVEN = 7
	EIGHT = 8
	NINE = 9
	TEN = 10
	JACK = 11
	QUEEN = 12
	KING = 13

	def __str__(self) -> str:
		return (
			"{:d}".format(self) if 2 <= self <= 10
			else "A" if self == 1 
			else "J" if self == 11
			else "Q" if self == 12
			else "K" if self == 13
			else ""
		)

class Card:
	suitTranslator = {
		"HEARTS": Suit.HEARTS,
		"H": Suit.HEARTS,
		"DIAMONDS": Suit.DIAMONDS,
		"D": Suit.DIAMONDS,
		"SPADES": Suit.SPADES,
		"S": Suit.SPADES,
		"CLUBS": Suit.CLUBS,
		"C": Suit.CLUBS
	}

	def __init__(self, rank_or_id : int, suit : str = None):
		if suit is None:
			rank = ((rank_or_id - 1) % 13) + 1
			suit = "HDSC"[(rank_or_id - 1) // 13]
		else:
			rank = rank_or_id

		try:
			self.rank = Rank(rank)
			self.suit = Suit(self.suitTranslator[suit.upper()])
		except KeyError:
			self.rank = None
			self.suit = None

	def __str__(self) -> str:
		return str(self.rank) + str(self.suit)

	def __repr__(self) -> str:
		return self.__str__()

	def getColor(self) -> str:
		return (
			"RED" if self.suit == Suit.HEARTS or self.suit == Suit.DIAMONDS
			else "BLACK" if self.suit == Suit.SPADES or self.suit == Suit.CLUBS
			else ""
		)
	
	def canPlacePatience(self, other : "Card") -> bool:
		return other.rank - self.rank == 1 and other.getColor() != self.getColor()

	def canPlaceFoundation(self, other : "Card") -> bool:
		return self.rank - other.rank == 1 and other.suit == self.suit

def colorCardString(card : Card) -> str:
		PREFIX = "\x1B[107;"
		MIDFIX = "m "
		SUFFIX = " \x1B[0m"

		colorTranslator = {
			"RED": "91",
			"BLACK": "30"
		}

		return PREFIX + colorTranslator[card.getColor()] + MIDFIX + str(card) + SUFFIX

class Foundation:
	def __init__(self):
		self.cards = []

	def isEmpty(self) -> bool:
		return len(self.cards) == 0
	
	def getTopCard(self) -> Card:
		if self.isEmpty():
			return None
	
		return self.cards[-1]

	def pushCard(self, card : Card):
		self.cards.append(card)

	def popCard(self) -> Card:
		return self.cards.pop()

	def __str__(self) -> str:
		return colorCardString(self.getTopCard())

class Tableau(Foundation):
	def __init__(self, cards : list = []):
		self.cards = cards

	def getStackIndex(self) -> int:
		if self.isEmpty():
			return -1

		i = len(self.cards) - 1

		for j in range(i - 1, -1, -1):
			if not self.cards[j + 1].canPlacePatience(self.cards[j]):
				break

			i = j

		return i

	def getStackSize(self) -> int:
		if self.isEmpty():
			return 0

		return len(self.cards) - self.getStackIndex()

	def __str__(self) -> str:
		return '\n'.join(map(lambda c : colorCardString(c), self.cards))

