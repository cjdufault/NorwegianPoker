import os

import pygame


class Player:
    def __init__(self, suit, origin, vert_bool):
        self.suit = suit  # the suit that the player is playing with
        self.origin = origin    # indicates the location where the player's hand is to be drawn
        self.vert_bool = vert_bool  # indicates the orientation that the player's hand is to be drawn in

        path = os.path.join("assets", suit)
        self.hand = {1: Card("A", path), 2: Card("2", path), 3: Card("3", path), 4 : Card("4", path), 5: Card("5", path),
                     6: Card("6", path), 8: Card("8", path), 9: Card("9", path), 10: Card("10", path), 11: Card("J", path),
                     12: Card("Q", path)}

    def flip_card(self, dice_roll):
        self.hand[dice_roll].flip()

    def get_card(self, card_int):
        return self.hand[card_int]

    def get_origin(self):
        return self.origin

    def get_vert_bool(self):
        return self.vert_bool


class Card:
    def __init__(self, card_name, image_path):
        self.card_name = card_name
        self.face_image = pygame.image.load(os.path.join(image_path, card_name + ".png")).convert()
        self.back_image = pygame.image.load(os.path.join("assets", "card_back.png")).convert()
        self.face_up = True

    def get_current_image(self):
        if self.face_up:
            return self.face_image
        else:
            return self.back_image

    def flip(self):
        if self.face_up:
            self.face_up = False
        else:
            self.face_up = True
