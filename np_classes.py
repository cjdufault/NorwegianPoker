import os
import pygame
import random


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
        # so it doesn't have to do it every time the image is drawn; doesn't play well w/ transparency though
        background_image = pygame.image.load(os.path.join("assets", "poker_table.jpg")).convert()
        self.background = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))

        self.title_image = pygame.image.load(os.path.join("assets", "np_title.png")).convert()
        self.two_players_image = pygame.image.load(os.path.join("assets", "player_options", "two_players.png"))
        self.three_players_image = pygame.image.load(os.path.join("assets", "player_options", "three_players.png"))
        self.four_players_image = pygame.image.load(os.path.join("assets", "player_options", "four_players.png"))
        self.card_back = pygame.image.load(os.path.join("assets", "card_back.png")).convert()
        self.roll_button = pygame.image.load(os.path.join("assets", "roll_button.png"))
        self.disabled_button = pygame.image.load(os.path.join("assets", "disabled_button.png"))
        self.clubs_wins = pygame.image.load(os.path.join("assets", "game_over", "clubs.png"))
        self.diamonds_wins = pygame.image.load(os.path.join("assets", "game_over", "diamonds.png"))
        self.hearts_wins = pygame.image.load(os.path.join("assets", "game_over", "hearts.png"))
        self.spades_wins = pygame.image.load(os.path.join("assets", "game_over", "spades.png"))
        self.yes_image = pygame.image.load(os.path.join("assets", "yes.png"))
        self.no_image = pygame.image.load(os.path.join("assets", "no.png"))

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

        self.numbers_images = {2: pygame.image.load(os.path.join("assets", "numbers", "2.png")),
                               3: pygame.image.load(os.path.join("assets", "numbers", "3.png")),
                               4: pygame.image.load(os.path.join("assets", "numbers", "4.png")),
                               5: pygame.image.load(os.path.join("assets", "numbers", "5.png")),
                               6: pygame.image.load(os.path.join("assets", "numbers", "6.png")),
                               7: pygame.image.load(os.path.join("assets", "numbers", "7.png")),
                               8: pygame.image.load(os.path.join("assets", "numbers", "8.png")),
                               9: pygame.image.load(os.path.join("assets", "numbers", "9.png")),
                               10: pygame.image.load(os.path.join("assets", "numbers", "10.png")),
                               11: pygame.image.load(os.path.join("assets", "numbers", "11.png")),
                               12: pygame.image.load(os.path.join("assets", "numbers", "12.png"))}

        # where the sum of the two dice will be displayed
        self.numbers_origin = (self.dice_origins[1][0] + 80, self.dice_origins[1][1] - 10)

        self.players = []

    def intro(self):
        # draw title and background
        self.screen.blit(self.background, (0, 0))
        title_image_rect = self.screen.blit(self.title_image,
                                            ((self.screen_width / 2) - 320, (self.screen_height / 2) - 213))
        pygame.display.update()

        # clear event queue of mouse downs
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)

        # after mouse click or key press, remove the title image and redraw background
        while True:
            # pygame.event.wait() waits until event is registered, otherwise the program uses literally every cpu cycle
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.screen.blit(self.background, (0, 0))
                pygame.display.update(title_image_rect)
                break
        return True

    def game_over(self, winner):
        if winner == "clubs":
            end_image = self.clubs_wins
        elif winner == "diamonds":
            end_image = self.diamonds_wins
        elif winner == "hearts":
            end_image = self.hearts_wins
        else:
            end_image = self.spades_wins

        end_image_origin = ((self.screen_width / 2) - 320, (self.screen_height / 2) - 213)
        end_image_rect = self.screen.blit(end_image, end_image_origin)

        # buttons to select whether to restart the game
        yes_rect = self.screen.blit(self.yes_image, (end_image_origin[0] + 200, end_image_origin[1] + 350))
        no_rect = self.screen.blit(self.no_image, (end_image_origin[0] + 380, end_image_origin[1] + 350))

        pygame.display.update(end_image_rect)
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)

        while True:
            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if yes_rect.collidepoint(mouse_pos):
                    return True
                elif no_rect.collidepoint(mouse_pos):
                    return False
            elif event.type == pygame.QUIT:
                return False

    def num_players(self):
        # buttons used to select number of players
        two_player_rect = self.screen.blit(self.two_players_image,
                                           ((self.screen_width / 2) - 224, (self.screen_height / 2) - 213))
        three_player_rect = self.screen.blit(self.three_players_image,
                                             ((self.screen_width / 2) - 224, (self.screen_height / 2) - 35))
        four_player_rect = self.screen.blit(self.four_players_image,
                                            ((self.screen_width / 2) - 224, (self.screen_height / 2) + 143))
        pygame.display.update(two_player_rect)
        pygame.display.update(three_player_rect)
        pygame.display.update(four_player_rect)

        pygame.event.clear(pygame.MOUSEBUTTONDOWN)

        while True:
            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # define the players list based on the player's selection
                if two_player_rect.collidepoint(mouse_pos):
                    self.players = [
                        Player("clubs", ((self.screen_width / 2) - 170, self.screen_height - 202), False, True,
                               ((self.screen_width / 2) - 170, self.screen_height - 15)),
                        Player("hearts", ((self.screen_width / 2) - 170, 20), False, False,
                               ((self.screen_width / 2) - 170, 0))]

                    self.screen.blit(self.background, (0, 0))
                    pygame.display.update(two_player_rect)
                    pygame.display.update(three_player_rect)
                    pygame.display.update(four_player_rect)
                    return True

                elif three_player_rect.collidepoint(mouse_pos):
                    self.players = [
                        Player("clubs", ((self.screen_width / 2) - 170, self.screen_height - 202), False, True,
                               ((self.screen_width / 2) - 170, self.screen_height - 15)),
                        Player("diamonds", (20, (self.screen_height / 2) - 235), True, False,
                               (0, (self.screen_height / 2) - 235)),
                        Player("spades", (self.screen_width - 150, (self.screen_height / 2) - 235), True, False,
                               (self.screen_width - 15, (self.screen_height / 2) - 235))]

                    self.screen.blit(self.background, (0, 0))
                    pygame.display.update(two_player_rect)
                    pygame.display.update(three_player_rect)
                    pygame.display.update(four_player_rect)
                    return True

                elif four_player_rect.collidepoint(mouse_pos):
                    self.players = [
                        Player("clubs", ((self.screen_width / 2) - 170, self.screen_height - 202), False, True,
                               ((self.screen_width / 2) - 170, self.screen_height - 15)),
                        Player("diamonds", (20, (self.screen_height / 2) - 235), True, False,
                               (0, (self.screen_height / 2) - 235)),
                        Player("hearts", ((self.screen_width / 2) - 170, 20), False, False,
                               ((self.screen_width / 2) - 170, 0)),
                        Player("spades", (self.screen_width - 150, (self.screen_height / 2) - 235), True, False,
                               (self.screen_width - 15, (self.screen_height / 2) - 235))]

                    self.screen.blit(self.background, (0, 0))
                    pygame.display.update(two_player_rect)
                    pygame.display.update(three_player_rect)
                    pygame.display.update(four_player_rect)
                    return True

            elif event.type == pygame.QUIT:
                return False

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

            status_bar_rect = self.screen.blit(status_bar_image, (status_bar_orig_x, status_bar_orig_y))
            pygame.display.update(status_bar_rect)

            # draw all of the cards
            if player.get_is_vert():
                for i in range(5):
                    card_rect_1 = self.screen.blit(player.get_card(i + 2).get_image(), (orig_x, orig_y + (i * 96)))
                    card_rect_2 = self.screen.blit(player.get_card(i + 8).get_image(), (orig_x + 70, orig_y + (i * 96)))
                    pygame.display.update(card_rect_1)
                    pygame.display.update(card_rect_2)
                    pygame.time.wait(100)
            else:
                for i in range(5):
                    card_rect_1 = self.screen.blit(player.get_card(i + 2).get_image(), (orig_x + (i * 70), orig_y))
                    card_rect_2 = self.screen.blit(player.get_card(i + 8).get_image(), (orig_x + (i * 70), orig_y + 96))
                    pygame.display.update(card_rect_1)
                    pygame.display.update(card_rect_2)
                    pygame.time.wait(100)

        # draw the dice
        self.draw_die(self.dice_images[random.randint(0, 5)], self.dice_origins[0])
        pygame.time.wait(100)
        self.draw_die(self.dice_images[random.randint(0, 5)], self.dice_origins[1])

    def draw_die(self, image, origin):
        die_rect = self.screen.blit(image, origin)
        pygame.display.update(die_rect)

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

        dice_sum = die_1_result + die_2_result

        numbers_rect = self.screen.blit(self.numbers_images[dice_sum], self.numbers_origin)
        pygame.display.update(numbers_rect)

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
        else:
            if dice_roll < 7:
                card_orig_x = player_origin[0] + (70 * (dice_roll - 2))
                card_orig_y = player_origin[1]
            else:
                card_orig_x = player_origin[0] + (70 * (dice_roll - 8))
                card_orig_y = player_origin[1] + 96

        # draw the new image
        card_rect = self.screen.blit(image, (card_orig_x, card_orig_y))
        pygame.display.update(card_rect)

    def set_roll_button(self, set_enable):
        if set_enable:
            roll_button_rect = self.screen.blit(self.roll_button, self.roll_button_origin)
        else:
            roll_button_rect = self.screen.blit(self.disabled_button, self.roll_button_origin)
        pygame.display.update(roll_button_rect)

    def set_status_bar(self, turn_num, is_active):
        player = self.players[turn_num]
        status_origin = player.get_status_bar_origin()

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

        status_rect = self.screen.blit(image, status_origin)
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

        path = os.path.join("assets", suit)

        # keys indicate dice rolls that correspond to that card
        self.hand = \
            {2: Card("2", path), 3: Card("3", path), 4: Card("4", path), 5: Card("5", path), 6: Card("6", path),
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
