import os
import pygame
import np_classes
import random


def main():
    pygame.init()
    running = True

    # create screen, set video mode
    screen_width = 1024
    screen_height = 576
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Norwegian Poker")

    # load assets
    icon = pygame.image.load(os.path.join("assets", "icon.png"))
    pygame.display.set_icon(icon)   # set icon

    # .convert() converts an image's pixel format to SDL's format ahead of time,
    # so it doesn't have to do it every time the image is drawn
    background = pygame.image.load(os.path.join("assets", "poker_table.jpg")).convert()
    title_image = pygame.image.load(os.path.join("assets", "np_title.png")).convert()
    card_back = pygame.image.load(os.path.join("assets", "card_back.png")).convert()

    dice_images = [pygame.image.load(os.path.join("assets", "dice", "dice1.png")).convert(),
                   pygame.image.load(os.path.join("assets", "dice", "dice2.png")).convert(),
                   pygame.image.load(os.path.join("assets", "dice", "dice3.png")).convert(),
                   pygame.image.load(os.path.join("assets", "dice", "dice4.png")).convert(),
                   pygame.image.load(os.path.join("assets", "dice", "dice5.png")).convert(),
                   pygame.image.load(os.path.join("assets", "dice", "dice6.png")).convert()]
    dice_origins = (((screen_width / 2) - 65, (screen_height / 2) - 30),
                    ((screen_width / 2) + 65, (screen_height / 2) - 30))

    # draw background and title
    screen.blit(background, (0, 0))
    screen.blit(title_image, (192, 75))
    pygame.display.update()

    # after mouse click or key press, remove the title image and redraw background
    while True:
        # pygame.event.wait() waits until an event is registered, otherwise the program uses literally every cpu cycle
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            screen.blit(background, (0, 0))
            pygame.display.update(pygame.Rect(192, 75, 832, 501))
            break

    if running:  # checks to make sure player hasn't tried to quit while title screen is displayed
        player1 = np_classes.Player("clubs", ((screen_width / 2) - 170, screen_height - 202), False, True)
        player2 = np_classes.Player("diamonds", (20, (screen_height / 2) - 235), True, False)
        player3 = np_classes.Player("hearts", ((screen_width / 2) - 170, 20), False, False)
        player4 = np_classes.Player("spades", (screen_width - 150, (screen_height / 2) - 235), True, False)

        # draw cards and dice
        deal(screen, [player1, player2, player3, player4])
        draw_die(screen, dice_images[random.randint(0, 5)], dice_origins[0])
        pygame.time.wait(100)
        draw_die(screen, dice_images[random.randint(0, 5)], dice_origins[1])

    # counter to indicate whose turn it is.
    turn = 1

    # start the main game
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
        # TODO: add listeners for different actions


def deal(screen, players):
    for player in players:
        origin = player.get_origin()
        orig_x = origin[0]
        orig_y = origin[1]

        # draw all of the cards
        if player.get_is_vert():
            for i in range(5):
                screen.blit(player.get_card(i + 2).get_image(), (orig_x, orig_y + (i * 96)))
                screen.blit(player.get_card(i + 8).get_image(), (orig_x + 70, orig_y + (i * 96)))
                pygame.display.update(pygame.Rect(orig_x, orig_y, orig_x + 130, orig_y + 470))
                pygame.time.wait(100)
        else:
            for i in range(5):
                screen.blit(player.get_card(i + 2).get_image(), (orig_x + (i * 70), orig_y))
                screen.blit(player.get_card(i + 8).get_image(), (orig_x + (i * 70), orig_y + 96))
                pygame.display.update(pygame.Rect(orig_x, orig_y, orig_x + 340, orig_y + 182))
                pygame.time.wait(100)


def draw_die(screen, image, origin):
    screen.blit(image, origin)
    pygame.display.update(pygame.Rect(origin[0], origin[1], origin[0] + 60, origin[1] + 60))


def roll(screen, dice_images, dice_origins):
    die_1_result = random.randint(1, 6)
    die_2_result = random.randint(1, 6)

    # display a bunch of dice faces. does nothing, just for show
    for i in range(random.randint(10, 20)):
        draw_die(screen, dice_images[random.randint(0, 5)], dice_origins[0])
        pygame.time.wait(50)
        draw_die(screen, dice_images[random.randint(0, 5)], dice_origins[1])
        pygame.time.wait(50)

    # draw and return the actual results
    draw_die(screen, dice_images[die_1_result - 1], dice_origins[0])
    pygame.time.wait(50)
    draw_die(screen, dice_images[die_2_result - 1], dice_origins[1])
    return die_1_result, die_2_result


def flip_card(screen, player, dice_roll, card_back):
    is_vert = player.get_is_vert()
    player_origin = player.get_origin()

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

    screen.blit(card_back, (card_orig_x, card_orig_y))
    pygame.display.update(hand_rect)


# increments the turn counter, and loops around to 1 if it's the last player's turn
def increment_turn(current_turn, num_players):
    if current_turn != num_players:
        next_turn = current_turn + 1
    else:
        next_turn = 1
    return next_turn


if __name__ == '__main__':
    main()