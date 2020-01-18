import pygame


class Player:
    def __init__(self, suit):
        self.suit = suit  # the suit that the player is playing with
        path = "assets/" + suit
        self.hand = [Card("A", path), Card("2", path), Card("3", path), Card("4", path), Card("5", path),
                     Card("6", path), Card("8", path), Card("9", path), Card("10", path), Card("J", path),
                     Card("Q", path)]

    def flip_card(self, dice_roll):
        self.hand[dice_roll - 1].flip()


class Card:
    def __init__(self, card_name, image_path):
        self.card_name = card_name
        self.face_image = pygame.image.load(image_path + card_name + ".png").convert()
        self.back_image = pygame.image.load("assets/card_back.png").convert()
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
