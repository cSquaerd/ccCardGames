from cards import Suit, Card, Foundation, Tableau, colorCardString
from enum import Enum
import random

NUM_FOUNDATIONS = 4
NUM_FREECELLS = 4
NUM_TABLEAUS = 8
NUM_CARDS = 52

class Target(Enum):
	TABLEAU = 'T'
	FREECELL = 'F'
	FOUNDATION = 'D'

class Move:
	def __init__(self, targetChar : str, id : str):
		self.target = Target(targetChar)
		self.id = id

	def __str__(self) -> str:
		return "{:s}:{:s}".format(self.target.name, self.id)

	def __repr__(self) -> str:
		return str(self)

	def getID(self):
		if self.target == Target.FOUNDATION:
			return self.id

		return int(self.id)

class SuperMove(Move):
	def __init__(self, targetChar : str, id : str, stackSize : int):
		super().__init__(targetChar, id)
		self.size = stackSize

	def __str__(self) -> str:
		return "{:s}:{:s},{:d}".format(self.target.name, self.id, self.size)

def decodeMoveString(m : str) -> tuple:
	try:
		source, destination = m.upper().split(';')
	except ValueError:
		return (None, None)

	# Move strings must be present for both source and destination targets
	if len(source) == 0 or len(destination) == 0:
		return (None, None)

	# Foundation targets must use letters for IDs, while others must use numbers for IDs
	elif (source[0] == Target.FOUNDATION.value and not source[1].isalpha()) \
		or (destination[0] == Target.FOUNDATION.value and not destination[1].isalpha()) \
		or (source[0] != Target.FOUNDATION.value and source[1].isalpha()) \
		or (destination[0] != Target.FOUNDATION.value and destination[1].isalpha()):
		return (None, None)

	if ',' in source:
		if source[0] != Target.TABLEAU.value:
			return (None, None)

		return (SuperMove(source[0], source[1], int(source.split(',')[1])), Move(destination[0], destination[1]))

	return (Move(source[0], source[1]), Move(destination[0], destination[1]))

class Freecell:
	def __init__(self):
		self.moves = []
		self.foundations = {suit: Foundation() for suit in Suit}
		self.freecells = [None for n in range(NUM_FREECELLS)]
		self.tableaus = [Tableau() for n in range(NUM_TABLEAUS)]
		self.initialized = False

	def __str__(self) -> str:
		freecells = "Freecells: {:s}{:s}{:s}{:s}".format(*[colorCardString(c) for c in self.freecells])
		foundations = "Foundations: {:s}{:s}{:s}{:s}".format(*[colorCardString(self.foundations[s].getTopCard()) for s in Suit])
		
		tableaus = ""
		n = 1
		for t in self.tableaus:
			tableaus += "Tableau #{:d}: {:s}\n".format(n, str(t))
			n += 1

		return '\n'.join([freecells, foundations, tableaus])

	def reset(self):
		for s in Suit:
			self.foundations[s].reset()

		for i in range(NUM_FREECELLS):
			self.freecells[i] = None

		for t in self.tableaus:
			t.reset()
		
		self.initialized = False

	def deal(self):
		if self.initialized:
			return

		ids = list(range(1, NUM_CARDS + 1))
		random.shuffle(ids)

		n = 0
		for id in ids:
			card = Card(id)
			print(card, n, n % NUM_TABLEAUS)
			self.tableaus[n % NUM_TABLEAUS].pushCard(card)
			n += 1

		self.initialized = True

	def canMove(self, moveString : str) -> bool:
		source, destination = decodeMoveString(moveString)

		if source is None or destination is None:
			return False

		if isinstance(source, SuperMove):
			# Determine if the stack is valid by the indicated size
			actualStackSize = self.tableaus[source.getID() - 1].getStackSize()
			if source.size > actualStackSize:
				return False
			elif destination.target != Target.TABLEAU:
				return False

			movingCard = self.tableaus[source.getID() - 1].cards[-source.size]

		else:
			if source.target == Target.TABLEAU:
				movingCard = self.tableaus[source.getID() - 1].getTopCard()
			elif source.target == Target.FREECELL:
				movingCard = self.freecells[source.getID() - 1]
			else:
				movingCard = self.foundations[Card.suitTranslator[source.getID()]].getTopCard()

		if destination.target == Target.TABLEAU:
			landingCard = self.tableaus[destination.getID() - 1].getTopCard()
		elif destination.target == Target.FREECELL:
			landingCard = self.freecells[destination.getID() - 1]
		else:
			suit = Card.suitTranslator[destination.getID()]
			landingCard = self.foundations[suit].getTopCard()

			return movingCard.suit == suit and movingCard.canPlaceFoundation(landingCard)

		return movingCard.canPlacePatience(landingCard)

