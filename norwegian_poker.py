import os

import pygame
import time
import np_classes


def main():
    pygame.init()

    # create screen, set video mode
    screen = pygame.display.set_mode((1024, 576))
    pygame.display.set_caption("Norwegian Poker")

    # load assets
    background = pygame.image.load("assets/poker_table.jpg").convert()
    title_image = pygame.image.load("assets/np_title.png").convert()

    # draw assets
    screen.blit(background, (0, 0))
    screen.blit(title_image, (192, 75))
    pygame.display.update()

    intro_done = False

    # after mouse click or key press, remove the title image and redraw background
    while not intro_done:
        # pygame.event.wait() waits until an event is registered, otherwise the program uses literally every cpu cycle
        mouse_or_key_pressed = pygame.event.wait()
        if mouse_or_key_pressed.type == pygame.KEYDOWN or mouse_or_key_pressed.type == pygame.MOUSEBUTTONDOWN:
            screen.blit(background, (0, 0))
            title_rect = pygame.Rect(192, 75, 832, 501)
            pygame.display.update(title_rect)
            intro_done = True

    player1 = np_classes.Player("clubs", (307, 374), False)
    player2 = np_classes.Player("diamonds", (, ), True)
    player3 = np_classes.Player("hearts", (307, 20), False)
    player4 = np_classes.Player("spades", (, ), True)

    running = True

    while running:
        deal(screen, [player1, player2, player3, player4])

        event = pygame.event.wait()
        # print(str(event.type) + " - " + pygame.event.event_name(event.type))
        if event.type == pygame.QUIT:
            running = False
        # TODO: add listeners for different actions


def deal(screen, players):
    testimage = pygame.image.load("assets/clubs/2.png")
    screen.blit(testimage, (0, 0))
    pygame.display.update()


if __name__ == '__main__':
    main()