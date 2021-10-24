import unittest

import batak


class TestClass(unittest.TestCase):
    def setUp(self):
        names = ['Mahmut', 'Mehmet', 'Omer', 'You']
        self.p = batak.create_players(names)
        self.deck = batak.create_deck()

        while len(self.deck) > 0:
            for obj in self.p.values():
                obj.cards.append(self.deck.pop())

    def test_valid_deck(self):
        self.assertEqual(len(
            set(self.p['Mahmut'].cards)
            | set(self.p['Mehmet'].cards)
            | set(self.p['Omer'].cards)
            | set(self.p['You'].cards)
        ), 52)


if __name__ == '__main__':
    unittest.main()
