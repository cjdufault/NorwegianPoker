import os

import pygame


class Player:
    def __init__(self, suit, origin, is_vert, is_human):
        self.suit = suit  # the suit that the player is playing with
        self.origin = origin    # indicates the location where the player's hand is to be drawn
        self.is_vert = is_vert  # indicates the orientation that the player's hand is to be drawn in
        self.is_human = is_human

        path = os.path.join("assets", suit)
        self.hand = {2: Card("2", path), 3: Card("3", path), 4: Card("4", path), 5: Card("5", path), 6: Card("6", path),
                     8: Card("8", path), 9: Card("9", path), 10: Card("10", path), 11: Card("J", path), 12: Card("Q", path)}

    def flip_card(self, dice_roll):
        self.hand[dice_roll].flip()

    def get_card(self, card_int):
        return self.hand[card_int]

    def get_hand(self):
        return self.hand

    def get_origin(self):
        return self.origin

    def get_is_vert(self):
        return self.is_vert

    def get_is_human(self):
        return self.is_human


class Card:
    def __init__(self, card_name, image_path):
        self.card_name = card_name
        self.image = pygame.image.load(os.path.join(image_path, card_name + ".png")).convert()
        self.face_up = True

    def flip(self):
        if self.face_up:
            self.face_up = False
        else:
            self.face_up = True

    def get_face_up(self):
        if self.face_up:
            return True

    def get_image(self):
        return self.image
