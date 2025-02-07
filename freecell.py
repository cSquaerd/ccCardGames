from cards import Suit, Card, Foundation, Tableau, colorCardString
import random

NUM_FOUNDATIONS = 4
NUM_FREECELLS = 4
NUM_TABLEAUS = 8
NUM_CARDS = 52

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

