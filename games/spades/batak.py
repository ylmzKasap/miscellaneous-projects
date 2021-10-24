import os
import random
from playerClass import Player


names = ['Mahmut', 'Mehmet', 'Omer', 'You']
symbols = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}
cards = [
        'A', 'K', 'Q', 'J', '10',
        '9', '8', '7', '6', '5',
        '4', '3', '2',
    ]
cardValues = {card: value for card, value in zip(cards[::-1], range(2, 15))}
turn = 0


def create_players(names):
    players = {}
    for name in names:
        players[name] = Player(name)
    return players


def create_deck():
    deck = [s + c for s in list(symbols.values()) for c in cards]
    random.shuffle(deck)
    return deck


def take_the_bets(deck):
    symbolCount = {'♣': 0, '♦': 0, '♥': 0, '♠': 0}
    symbolStrength = {'♣': 0, '♦': 0, '♥': 0, '♠': 0}
    strongCards = {'A': 1, 'K': 0.80, 'Q': 0.60, 'J': 0.40, '10': 0.20}
    for card in deck:
        cardSymbol = card[0]
        cardName = card[1:]
        symbolCount[cardSymbol] += 1
        if cardName in strongCards:
            symbolStrength[cardSymbol] += strongCards[cardName]
    for symbol, count in symbolCount.items():
        symbolStrength[symbol] += count / 2.5 if count > 4 else 0
    koz = max(symbolStrength.items(), key=lambda x: x[1])[0]
    bet = int(sum(symbolStrength.values()))
    if bet > 13:
        bet = 13
    return koz, bet


def take_player_bet(currentBet, pName):
    while True:
        print("\nEnter your bet or enter 'f' to fold.")
        print(f"Your cards: {', '.join(players[pName].cards)}")
        playerBet = input('>  ').lower().strip()
        if playerBet == 'f':
            return False
        try:
            playerBet = int(playerBet)
        except ValueError:
            os.system('cls')
            print('\nOnly enter a number')
            continue
        if playerBet <= currentBet:
            os.system('cls')
            print(f'\nCurrent bet is {currentBet}. Enter a higher bet or fold.')
            continue
        elif playerBet > 13:
            os.system('cls')
            print('You cannot enter a higher bet than 13.')
            continue
        return playerBet


def take_player_koz(bet, pName):
    os.system('cls')
    while True:
        print(f'\nEveryone folded. Your bet is {bet}. Choose a koz.')
        for shortC, symbol in symbols.items():
            print(f'{symbol}: {shortC}')
        print(f"Your cards: {', '.join(players[pName].cards)}")
        koz = input('>>>').lower().strip()
        if koz not in symbols.keys():
            os.system('cls')
            print(f"\nThere is no such symbol shortcut for '{koz}'.")
            continue
        return symbols[koz]


def pick_card(fCard, winCard, deck):
    global kozThrown
    if winCard is not None:
        # Get last card info and find suitable responses.
        firstCardSymbol = fCard[0]
        winCardSymbol = winCard[0]
        winCardValue = cardValues[winCard[1:]]
        availableCards = [card for card in deck if card.startswith(firstCardSymbol)]

        if availableCards:
            winningCards = []
            losingCards = []
            if firstCardSymbol != winCardSymbol:
                losingCards = availableCards
            else:
                for card in availableCards:
                    if cardValues[card[1:]] > winCardValue:
                        winningCards.append(card)
                    else:
                        losingCards.append(card)
            if len(winningCards) > 0:
                return random.choice(winningCards), True
            else:
                return min(losingCards, key=lambda x: cardValues.get(x[1:])), False
        else:  # No cards with winning symbol.
            availableKoz = [card for card in deck if card.startswith(koz)]
            if availableKoz:
                if not kozThrown:
                    kozThrown = True
                    return min(availableKoz, key=lambda x: cardValues.get(x[1:])), True
                else:
                    winningKoz = []
                    losingKoz = []
                    if winCardSymbol != koz:
                        winningKoz = availableKoz
                    else:
                        for card in availableKoz:
                            if cardValues[card[1:]] > winCardValue:
                                winningKoz.append(card)
                            else:
                                losingKoz.append(card)
                    if winningKoz:
                        return random.choice(winningKoz), True
                    else:
                        return min(losingKoz, key=lambda x: cardValues.get(x[1:])), False
            else:
                return random.choice(deck), False
    else:  # First card being thrown.
        card = random.choice(deck)
        if kozThrown:
            return card, True
        else:
            while card[0] == koz:
                card = random.choice(deck)
            return card, True


def check_input(fCard, wCard, inp, deck):
    """
    Returns 3 values:
    value_1: Input is valid.
    value_2: Input wins.
    value_3: Invalid input message.
    """
    global kozThrown
    if wCard is not None:
        firstCardSymbol = fCard[0]
        winCardSymbol = wCard[0]
        winCardValue = cardValues[wCard[1:]]

        if inp[0] == firstCardSymbol:
            if firstCardSymbol != winCardSymbol:
                # VALID, koz on board, you lose.
                return True, False, None
            elif cardValues[inp[1:]] > winCardValue:
                # VALID, your card beats, you win.
                return True, True, None
            else:
                # Input is smaller than the winning card.
                availableCards = [card for card in deck if card.startswith(firstCardSymbol)]
                winningCards = [card for card in availableCards if cardValues[card[1:]] > winCardValue]
                if len(winningCards) > 0:
                    # You have a stronger card, INVALID.
                    return False, None, 'Invalid input. You have a stronger card.'
                else:
                    # VALID, you can only use a weaker card, you lose.
                    return True, False, None
        else:
            # Input does not match first card's symbol.
            playerHasCard = False
            for card in deck:
                if card[0] == firstCardSymbol:
                    playerHasCard = True
                    break
            if playerHasCard:
                # Player has a card with the same type of first card, INVALID.
                return False, None, f"Invalid input. You have '{firstCardSymbol}'."
            else:
                # Player doesn't have the same card.
                if inp[0] == koz:
                    if winCardSymbol != koz:
                        # VALID, winning card is not koz. You used a koz. You win.
                        kozThrown = True
                        return True, True, None
                    else:
                        # Winning card is a koz.
                        if cardValues[inp[1:]] > winCardValue:
                            # VALID, your koz is bigger. you win.
                            return True, True, None
                        else:
                            # You used a smaller koz, got a bigger one?
                            for card in deck:
                                if card[0] == koz:
                                    if cardValues[card[1:]] > winCardValue:
                                        # You got a bigger one, INVALID.
                                        return False, None, 'You have at least one bigger koz. Use it instead.'
                            # VALID, you don't have a bigger koz, you lose.
                            return True, False, None
                else:
                    # Input is not a koz.
                    playerHasKoz = False
                    for card in deck:
                        if card[0] == koz:
                            playerHasKoz = True
                            break
                    if playerHasKoz:
                        # You must use a koz instead of a random card, INVALID.
                        return False, None, 'You have at least one koz. You must use them instead.'
                    else:
                        # VALID, you don't have a koz, you lose.
                        return True, False, None
    else:
        # First card.
        if kozThrown:
            # VALID, you can start with any card if koz is used before, you win.
            return True, True, None
        else:
            # Koz is not used.
            if inp[0] == koz:
                # You cannot start with a koz if it is not used before, INVALID.
                return False, None, 'Koz has not beet used yet. Throw another card'
            else:
                # VALID, koz is not used, you didn't start with a koz, you win.
                return True, True, None


if __name__ == '__main__':
    players = create_players(names)
    while True:
        deck = create_deck()
        print()

        # Deal the cards.
        deckStart = 0
        for obj in players.values():
            obj.cards = sorted(
                deck[deckStart:deckStart + 13], key=lambda x: (x[0], -cardValues[x[1:]]))
            deckStart += 13

        # Find the bets and the koz for bots.
        for name, obj in players.items():
            if name.lower() != 'you':
                obj.koz, obj.bet = take_the_bets(obj.cards)

        # Take the bets from each player and determine the koz.
        bet = 4
        playersWhoFold = []
        everyBetTaken = False
        while True:
            for i in range(len(names)):
                player = names[(i + turn) % len(names)]
                if player not in playersWhoFold:
                    if everyBetTaken:
                        if len(playersWhoFold) == 3:
                            break
                    if player.lower() == 'you':
                        players[player].bet = take_player_bet(bet, player)
                        if players[player].bet:
                            bet = players[player].bet
                        else:
                            print(f'{player} fold!')
                            players[player].bet = False
                            playersWhoFold.append(player)
                    else:
                        if players[player].bet > bet:
                            bet += 1
                            print(f'{player} bets {bet}!')
                        else:
                            print(f'{player} folds!')
                            players[player].bet = False
                            playersWhoFold.append(player)

            everyBetTaken = True
            if len(playersWhoFold) == 4:
                player = names[turn % len(names)]
                if player.lower() == 'you':
                    koz = take_player_koz(bet, player)
                    players[player].koz = koz
                else:
                    koz = players[player].koz
                os.system('cls')
                print(f'\nEveryone folded. Koz is determined by {player}.')
                print(f'Koz is {koz}.')
                break
            elif len(playersWhoFold) == 3:
                player = [p for p in names if p not in playersWhoFold][0]
                players[player].bet = bet
                if player.lower() == 'you':
                    koz = take_player_koz(bet, player)
                    players[player].koz = koz
                else:
                    koz = players[player].koz
                os.system('cls')
                print(f'\nKoz is set by {player} with the highest bet {bet}.')
                print(f'Koz is {koz}.')
                break
        kozSetter = player
        koz = players[kozSetter].koz
        kozThrown = False

        # Start the turn
        for i in range(13):
            firstCard = None
            firstCardThrown = False
            lastCard = None
            lastWinningCard = None
            winningPlayer = None
            kozOverCard = False
            for name, obj in players.items():
                winning = False
                if name.lower() == 'you':
                    while True:
                        print('\nChoose a suitable card from your deck.')
                        for number, card in enumerate(obj.cards, 1):
                            print(f'{str(number)}) {card}', end=' | ')
                        selectedCard = input('\n>>> ')
                        allowedNumbers = [str(i) for i in range(1, len(obj.cards) + 1)]
                        if selectedCard not in allowedNumbers:
                            os.system('cls')
                            print(f'Invalid input.')
                            continue
                        correctInput, winning, errorMessage = check_input(
                            firstCard, lastWinningCard, obj.cards[int(selectedCard) - 1], players[name].cards)
                        if not correctInput:
                            os.system('cls')
                            print(f'\n{errorMessage}')
                            continue
                        lastCard = obj.cards[int(selectedCard) - 1]
                        del obj.cards[int(selectedCard) - 1]
                        break
                else:
                    lastCard, winning = pick_card(firstCard, lastWinningCard, obj.cards)
                    obj.cards.remove(lastCard)
                if winning:
                    winningPlayer = name
                    lastWinningCard = lastCard
                if not firstCardThrown:
                    firstCard = lastCard
                    firstCardThrown = True

                os.system('cls')
                print(players[name].cards)
                print(f'{name} threw {lastCard}!')
                if winningPlayer is not None:
                    print(f'Current winner: {winningPlayer}')
                if lastWinningCard is not None:
                    print(f'Last winning card: {lastWinningCard}')
                if lastCard is not None:
                    print(f'Last card: {lastCard}')
                print()
                print()

            players[winningPlayer].captures += 1

        for player in names:
            playerBet = players[player].bet
            if player == kozSetter:
                if players[player].captures < playerBet:
                    players[player].add_score(-playerBet)
                else:
                    players[player].add_score(players[player].captures)
            else:
                players[player].add_score(players[player].captures)

        # Reset the turn.
        for player in names:
            players[player].cards = []
            players[player].bet = 0
            players[player].koz = None
            players[player].captures = 0
        turn += 1
