class Card:
    # Define the suits
    DIAMONDS = 1
    CLUBS = 2
    HEARTS = 3
    SPADES = 4
    SUITS = {
        CLUBS: 'Clubs',
        HEARTS: 'Hearts',
        DIAMONDS: 'Diamonds',
        SPADES: 'Spades'
    }

    # Define the names of special cards
    VALUES = {
        1: 'Ace',
        11: 'Jack',
        12: 'Queen',
        13: 'King'
    }

    def __init__(self, suit, value):
        # Save the suit and card value
        self.suit = suit
        self.value = value

    def __cmp__(self, other):
        # Compare the card with another card
        # (return <0 if we are smaller, >0 if
        # we are large, 0 if we are the same)
        if self.suit < other.suit:
            return -1
        elif self.suit > other.suit:
            return 1
        elif self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        else:
            return 0

    def __str__(self):
        # Return a string description of ourself
        if self.value in self.VALUES:
            buf = self.VALUES[self.value]
        else:
            buf = str(self.value)
        buf = buf + ' of ' + self.SUITS[self.suit]

        return buf
