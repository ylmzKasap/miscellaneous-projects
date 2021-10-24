class Player:
    def __init__(self, name):
        self._name = name
        self._score = 0
        self._scores = []
        self.cards = []
        self.bet = 0
        self.koz = None
        self.captures = 0

    def add_score(self, points):
        self._score += points
        self._scores.append(points)