import os

from . import card

class Player:
    def __init__(self, suit, origin, is_vert, is_human, status_bar_origin):
        self.suit = suit  # the suit that the player is playing with
        self.origin = origin    # indicates the location where the player's hand is to be drawn
        self.is_vert = is_vert  # indicates the orientation that the player's hand is to be drawn in
        self.is_human = is_human
        self.status_bar_origin = status_bar_origin

        path = os.path.join("assets", suit)

        # keys indicate dice rolls that correspond to that card
        self.hand = \
            {2: card.Card("2", path), 3: card.Card("3", path), 4: card.Card("4", path), 5: card.Card("5", path), 6: card.Card("6", path),
             8: card.Card("8", path), 9: card.Card("9", path), 10: card.Card("10", path), 11: card.Card("J", path), 12: card.Card("Q", path)}

    def flip_card(self, dice_roll):
        self.hand[dice_roll].flip()

    def get_card(self, dice_roll):
        return self.hand[dice_roll]

    def get_is_vert(self):
        return self.is_vert

    def get_is_human(self):
        return self.is_human

    def get_origin(self):
        return self.origin

    def get_hand(self):
        return self.hand

    def get_suit(self):
        return self.suit

    def get_status_bar_origin(self):
        return self.status_bar_origin

    # returns true if all player's cards are face down
    def has_won(self):
        has_won = True

        for card in self.hand:

            # set has_won to false and break if we find any card that's face up
            if self.hand[card].is_face_up():
                has_won = False
                break

        return has_won
