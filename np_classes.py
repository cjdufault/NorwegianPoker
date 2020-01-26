import os
import pygame
import random
import norwegian_poker


class Display:
    def __init__(self, width, height):
        pygame.init()

        # create screen, set video mode
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Norwegian Poker")

        # load assets
        icon = pygame.image.load(os.path.join("assets", "icon.png"))
        pygame.display.set_icon(icon)  # set icon

        # .convert() converts an image's pixel format to SDL's format ahead of time,
        # so it doesn't have to do it every time the image is drawn
        self.background = pygame.image.load(os.path.join("assets", "poker_table.jpg")).convert()
        self.title_image = pygame.image.load(os.path.join("assets", "np_title.png")).convert()
        self.card_back = pygame.image.load(os.path.join("assets", "card_back.png")).convert()
        self.roll_button = pygame.image.load(os.path.join("assets", "roll_button.png"))
        self.disabled_button = pygame.image.load(os.path.join("assets", "disabled_button.png"))

        self.status_bar_active_h = pygame.image.load(os.path.join("assets", "status_bars", "active_h.png")).convert()
        self.status_bar_active_v = pygame.image.load(os.path.join("assets", "status_bars", "active_v.png")).convert()
        self.status_bar_inactive_h = \
            pygame.image.load(os.path.join("assets", "status_bars", "inactive_h.png")).convert()
        self.status_bar_inactive_v = \
            pygame.image.load(os.path.join("assets", "status_bars", "inactive_v.png")).convert()

        self.roll_button_origin = (self.screen_width - 300, self.screen_height - 150)
        self.roll_button_rect = pygame.Rect(self.roll_button_origin[0], self.roll_button_origin[1],
                                            self.roll_button_origin[0] + 100, self.roll_button_origin[1] + 100)

        self.dice_images = [pygame.image.load(os.path.join("assets", "dice", "dice1.png")).convert(),
                            pygame.image.load(os.path.join("assets", "dice", "dice2.png")).convert(),
                            pygame.image.load(os.path.join("assets", "dice", "dice3.png")).convert(),
                            pygame.image.load(os.path.join("assets", "dice", "dice4.png")).convert(),
                            pygame.image.load(os.path.join("assets", "dice", "dice5.png")).convert(),
                            pygame.image.load(os.path.join("assets", "dice", "dice6.png")).convert()]
        self.dice_origins = (((self.screen_width / 2) - 65, (self.screen_height / 2) - 30),
                             ((self.screen_width / 2) + 5, (self.screen_height / 2) - 30))

        self.players = [Player("clubs", ((self.screen_width / 2) - 170, self.screen_height - 202), False, True,
                               ((self.screen_width / 2) - 170, self.screen_height - 15)),
                        Player("diamonds", (20, (self.screen_height / 2) - 235), True, False,
                               (0, (self.screen_height / 2) - 235)),
                        Player("hearts", ((self.screen_width / 2) - 170, 20), False, False,
                               ((self.screen_width / 2) - 170, 0)),
                        Player("spades", (self.screen_width - 150, (self.screen_height / 2) - 235), True, False,
                               (self.screen_width - 15, (self.screen_height / 2) - 235))]

    def intro(self):
        # draw background and title
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title_image, (192, 75))
        pygame.display.update()

        # after mouse click or key press, remove the title image and redraw background
        while True:
            # pygame.event.wait() waits until event is registered, otherwise the program uses literally every cpu cycle
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.screen.blit(self.background, (0, 0))
                pygame.display.update(pygame.Rect((self.screen_width / 2) - 320, (self.screen_height / 2) - 213,
                                                  (self.screen_width / 2) + 320, (self.screen_height / 2) + 213))
                break
        return True

    def deal(self):
        for player in self.players:
            origin = player.get_origin()
            orig_x = origin[0]
            orig_y = origin[1]
            status_bar_origin = player.get_status_bar_origin()
            status_bar_orig_x = status_bar_origin[0]
            status_bar_orig_y = status_bar_origin[1]

            # draw status bar
            if player.get_is_vert():
                status_bar_image = self.status_bar_inactive_v
            else:
                status_bar_image = self.status_bar_inactive_h

            status_bar_rect = player.get_status_bar_rect()
            self.screen.blit(status_bar_image, (status_bar_orig_x, status_bar_orig_y))
            pygame.display.update(status_bar_rect)

            # draw all of the cards
            if player.get_is_vert():
                for i in range(5):
                    self.screen.blit(player.get_card(i + 2).get_image(), (orig_x, orig_y + (i * 96)))
                    self.screen.blit(player.get_card(i + 8).get_image(), (orig_x + 70, orig_y + (i * 96)))
                    pygame.display.update(pygame.Rect(orig_x, orig_y, orig_x + 130, orig_y + 470))
                    pygame.time.wait(100)
            else:
                for i in range(5):
                    self.screen.blit(player.get_card(i + 2).get_image(), (orig_x + (i * 70), orig_y))
                    self.screen.blit(player.get_card(i + 8).get_image(), (orig_x + (i * 70), orig_y + 96))
                    pygame.display.update(pygame.Rect(orig_x, orig_y, orig_x + 340, orig_y + 182))
                    pygame.time.wait(100)

        # draw the dice
        self.draw_die(self.dice_images[random.randint(0, 5)], self.dice_origins[0])
        pygame.time.wait(100)
        self.draw_die(self.dice_images[random.randint(0, 5)], self.dice_origins[1])

    def draw_die(self, image, origin):
        self.screen.blit(image, origin)
        pygame.display.update(pygame.Rect(origin[0], origin[1], origin[0] + 60, origin[1] + 60))

    def roll(self, die_1_result, die_2_result):
        # display a bunch of dice faces. does nothing, just for show
        for i in range(random.randint(10, 20)):
            self.draw_die(self.dice_images[random.randint(0, 5)], self.dice_origins[0])
            pygame.time.wait(50)
            self.draw_die(self.dice_images[random.randint(0, 5)], self.dice_origins[1])
            pygame.time.wait(50)

        # draw the actual results
        self.draw_die(self.dice_images[die_1_result - 1], self.dice_origins[0])
        pygame.time.wait(50)
        self.draw_die(self.dice_images[die_2_result - 1], self.dice_origins[1])

    def flip_card(self, player, dice_roll):
        is_vert = player.get_is_vert()  # get player's orientation
        player_origin = player.get_origin()  # get player's position on board

        # reverse the face shown
        if player.get_card(dice_roll).is_face_up():
            image = self.card_back
        else:
            image = player.get_card(dice_roll).get_image()

        player.flip_card(dice_roll)

        # calculate origins for a given card based on the player's origin and orientation
        if is_vert:
            if dice_roll < 7:
                card_orig_x = player_origin[0]
                card_orig_y = player_origin[1] + (96 * (dice_roll - 2))
            else:
                card_orig_x = player_origin[0] + 70
                card_orig_y = player_origin[1] + (96 * (dice_roll - 8))
            hand_rect = pygame.Rect(player_origin[0], player_origin[1], player_origin[0] + 130, player_origin[1] + 470)
        else:
            if dice_roll < 7:
                card_orig_x = player_origin[0] + (70 * (dice_roll - 2))
                card_orig_y = player_origin[1]
            else:
                card_orig_x = player_origin[0] + (70 * (dice_roll - 8))
                card_orig_y = player_origin[1] + 96
            hand_rect = pygame.Rect(player_origin[0], player_origin[1], player_origin[0] + 340, player_origin[1] + 182)

        # draw the new image
        self.screen.blit(image, (card_orig_x, card_orig_y))
        pygame.display.update(hand_rect)

    def set_roll_button(self, set_enable):
        if set_enable:
            self.screen.blit(self.roll_button, self.roll_button_origin)
            pygame.display.update(self.roll_button_rect)
        else:
            self.screen.blit(self.disabled_button, self.roll_button_origin)
            pygame.display.update(self.roll_button_rect)

    def set_status_bar(self, turn_num, is_active):
        player = self.players[turn_num]
        status_origin = player.get_status_bar_origin()
        status_rect = player.get_status_bar_rect()

        if is_active:
            if player.get_is_vert():
                image = self.status_bar_active_v
            else:
                image = self.status_bar_active_h
        else:
            if player.get_is_vert():
                image = self.status_bar_inactive_v
            else:
                image = self.status_bar_inactive_h

        self.screen.blit(image, status_origin)
        pygame.display.update(status_rect)

    def get_players(self):
        return self.players

    def set_players(self, players):
        self.players = players


class Player:
    def __init__(self, suit, origin, is_vert, is_human, status_bar_origin):
        self.suit = suit  # the suit that the player is playing with
        self.origin = origin    # indicates the location where the player's hand is to be drawn
        self.is_vert = is_vert  # indicates the orientation that the player's hand is to be drawn in
        self.is_human = is_human
        self.status_bar_origin = status_bar_origin

        if is_vert:
            self.status_bar_rect = pygame.Rect(status_bar_origin[0], status_bar_origin[1],
                                               status_bar_origin[0] + 130, status_bar_origin[1] + 470)
        else:
            self.status_bar_rect = pygame.Rect(status_bar_origin[0], status_bar_origin[1],
                                               status_bar_origin[0] + 340, status_bar_origin[1] + 182)

        path = os.path.join("assets", suit)

        # keys indicate dice rolls that correspond to that card
        self.hand = {2: Card("2", path), 3: Card("3", path), 4: Card("4", path), 5: Card("5", path), 6: Card("6", path),
                     8: Card("8", path), 9: Card("9", path), 10: Card("10", path), 11: Card("J", path), 12: Card("Q", path)}

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

    def get_status_bar_rect(self):
        return self.status_bar_rect

    # returns true if all player's cards are face down
    def has_won(self):
        has_won = True

        for card in self.hand:

            # set has_won to false and break if we find any card that's face up
            if self.hand[card].is_face_up():
                has_won = False
                break

        return has_won


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
