import os
import pygame

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

    def is_face_up(self):
        return self.face_up

    def get_image(self):
        return self.image