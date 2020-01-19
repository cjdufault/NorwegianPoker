import pygame
import time


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
        mouse_or_key_pressed = pygame.event.wait()
        if mouse_or_key_pressed.type == pygame.KEYDOWN or mouse_or_key_pressed.type == pygame.MOUSEBUTTONDOWN:
            screen.blit(background, (0, 0))
            title_rect = pygame.Rect(192, 75, 832, 501)
            pygame.display.update(title_rect)
            intro_done = True

    running = True

    while running:
        event = pygame.event.wait()
        print(str(event.type) + " - " + pygame.event.event_name(event.type))
        if event.type == pygame.QUIT:
            running = False
        # TODO: add listeners for different actions


if __name__ == '__main__':
    main()