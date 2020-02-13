import pygame
import np_classes
import random

turn = 0    # counter to indicate whose turn it is.
running = True
restart = True

window_width = 1024
window_height = 576
display = np_classes.Display(window_width, window_height)


def main():
    global running
    global restart

    while restart:
        restart = False
        running = display.intro()

        if running:  # checks to make sure player hasn't tried to quit while title screen is displayed
            running = display.num_players()

        if running:
            display.deal()
            display.set_status_bar(0, True)

        # start the main game
        while running:
            do_turn()


def do_turn():
    global turn
    global running
    player = display.get_players()[turn]

    dice_rolled = False  # will be assigned true if a dice roll has occurred
    result = 0
    dice_roll = ()

    human = player.get_is_human()

    # for computer players
    if not human:
        wait(500)

        listen_for_quit()
        if running:
            # do dice roll
            dice_roll = roll()
            result = dice_roll[0] + dice_roll[1]
            dice_rolled = True

        wait(500)

    # for human players
    else:
        display.set_roll_button(True)

        # clear all mouse clicks, so clicks from other turns aren't registered
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        event = pygame.event.wait()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if display.roll_button_rect.collidepoint(mouse_pos):  # if the mouse is over the button when clicked
                display.set_roll_button(False)

                # do dice roll
                listen_for_quit()
                if running:
                    dice_roll = roll()
                    result = dice_roll[0] + dice_roll[1]
                    dice_rolled = True

        elif event.type == pygame.QUIT:
            running = False

    # flip any cards that should be flipped
    if dice_rolled and result != 7:

        # check if player has card face up, if yes, flip it
        if player.get_card(result).is_face_up():
            display.flip_card(player, result)

            # if player has card face up and rolls doubles, it's their turn again, so we leave the turn variable
            # untouched. otherwise, we go to the next player's turn.
            if not dice_roll[0] == dice_roll[1]:
                turn = increment_turn(turn, len(display.players))

        # if player has card face down
        else:
            other_player_has_card_face_up = False  # will be true if another player has card face up

            for i in range(len(display.players)):
                turn = increment_turn(turn, len(display.players))

                wait(300)

                if not other_player_has_card_face_up:
                    next_player_has_card = display.players[turn].get_card(result).is_face_up()

                    # if another player has the card face up, flip their card, and now it's their turn
                    if next_player_has_card:
                        display.flip_card(display.players[turn], result)
                        other_player_has_card_face_up = True

                        wait(500)
                        break

            if not other_player_has_card_face_up:
                display.flip_card(player, result)

                wait(500)
                turn = increment_turn(turn, len(display.players))

    # there are no sevens in this game, so we just go to the next turn
    elif dice_rolled and result == 7:
        turn = increment_turn(turn, len(display.players))

        wait(500)

    # tests if the game has ended
    for p in display.players:
        if p.has_won():

            # pause for long enough for the player to see the game is over
            wait(1000)
            game_over(p.get_suit())


def roll():
    die_1_result = random.randint(1, 6)
    die_2_result = random.randint(1, 6)

    display.roll(die_1_result, die_2_result)
    return die_1_result, die_2_result


# increments the turn counter, and loops around to 0 if it's the last player's turn
def increment_turn(current_turn, num_players):
    if current_turn < num_players - 1:
        next_turn = current_turn + 1
    else:
        next_turn = 0

    # deactivate the current player's status bar, and activate the next players
    display.set_status_bar(current_turn, False)
    display.set_status_bar(next_turn, True)
    return next_turn


def game_over(winner):
    global running
    global restart
    global display
    global turn

    running = False

    restart = display.game_over(winner)  # show end screen and ask for restart
    if restart:

        # reset display and turn counter
        display = np_classes.Display(window_width, window_height)
        turn = 0


# checks if any QUIT events are in the event queue
def listen_for_quit():
    global running

    quit_events = pygame.event.get(pygame.QUIT)
    if len(quit_events) > 0:
        running = False


# waits for the given number of milliseconds so long as there has been no QUIT event
def wait(time):
    listen_for_quit()
    if running:
        pygame.time.wait(time)


if __name__ == '__main__':
    main()
