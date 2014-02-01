def BlackJack(a, b, c):
    cards = [a, b, c]
    addCards = []
    aceCount = 0
    for card in cards:
        if card == "Ace":
            aceCount = aceCount + 1
            addCards.append(11)
        elif card == "Jack":
            addCards.append(10)
        elif card == "Queen":
            addCards.append(10)
        elif card == "King":
            addCards.append(10)
        else:
            addCards.append(int(card))

    x = 0
    if x <= 21:
        print "Valid"
    else:
        x = x - (aceCount * 10)
        if x <= 21:
            print "Valid"
        else:
            print "Invalid"