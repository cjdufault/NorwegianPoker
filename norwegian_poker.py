import pygame
import np_classes
import random

turn = 0    # counter to indicate whose turn it is.
running = True
display = np_classes.Display(1024, 576)


def main():
    global running
    global display

    running = display.intro()

    # TODO: ask the player how many players they want to play with (2-4) and implement gameplay w/ varying #s of players

    if running:  # checks to make sure player hasn't tried to quit while title screen is displayed
        display.deal()
        display.set_status_bar(0, True)

    # start the main game
    while running:
        do_turn()


def do_turn():
    global turn
    global running
    global display
    player = display.get_players()[turn]

    dice_rolled = False  # will be assigned true if a dice roll has occurred
    result = 0
    dice_roll = ()

    human = player.get_is_human()

    # for computer players
    if not human:
        listen_for_quit()

        if running:
            # do dice roll
            dice_roll = roll()
            result = dice_roll[0] + dice_roll[1]
            dice_rolled = True

        listen_for_quit()
        if running:
            pygame.time.wait(1000)

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

                listen_for_quit()
                if running:
                    pygame.time.wait(1000)

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

                listen_for_quit()
                if running:
                    pygame.time.wait(300)

                if not other_player_has_card_face_up:
                    next_player_has_card = display.players[turn].get_card(result).is_face_up()

                    # if another player has the card face up, flip their card, and now it's their turn
                    if next_player_has_card:
                        display.flip_card(display.players[turn], result)
                        other_player_has_card_face_up = True

                        listen_for_quit()
                        if running:
                            pygame.time.wait(750)
                        break

            if not other_player_has_card_face_up:
                display.flip_card(player, result)

                listen_for_quit()
                if running:
                    pygame.time.wait(1000)
                    turn = increment_turn(turn, len(display.players))

        listen_for_quit()
        if running:
            pygame.time.wait(1000)

    # there are no sevens in this game, so we just go to the next turn
    elif dice_rolled and result == 7:
        turn = increment_turn(turn, len(display.players))

        listen_for_quit()
        if running:
            pygame.time.wait(1000)

    # tests if the game has ended
    for p in display.players:
        if p.has_won():
            print(p.get_suit() + " has won")  # TODO: replace with an actual end of game screen or something
            running = False


def roll():
    global display

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


# checks if any quit events are in the event queue
def listen_for_quit():
    global running

    quit_events = pygame.event.get(pygame.QUIT)
    if len(quit_events) > 0:
        running = False


if __name__ == '__main__':
    main()
