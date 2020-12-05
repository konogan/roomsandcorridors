# encoding: utf-8
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import sys
import pygame
from Constants import States, Direction


def check_events(game):
    # respond to events
    # delegate to differnet module
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game(game)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_click(game, mouse_x, mouse_y)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            game.world.set_mouse(mouse_x, mouse_y)
            check_buttons_hover(game, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, game)
        elif event.type == pygame.KEYUP:
            check_keyup(event, game)


def check_keydown(event, game):
    if event.key == pygame.K_ESCAPE:
        if game.state == States.PLAY:
            pause_game(game)
        else:
            play_game(game)


def check_keyup(event, game):
    if event.key == pygame.K_i:
        game.switch_inventory()
    
    if game.state == States.PLAY:
        if event.key == pygame.K_RIGHT:
            game.new_turn()
            game.world.move_player_intent(Direction.EAST)
        if event.key == pygame.K_LEFT:
            game.new_turn()
            game.world.move_player_intent(Direction.WEST)
        if event.key == pygame.K_UP:
            game.new_turn()
            game.world.move_player_intent(Direction.NORTH)
        if event.key == pygame.K_DOWN:
            game.new_turn()
            game.world.move_player_intent(Direction.SOUTH)
        if event.key == pygame.K_o:
            game.world.player_open_door()
        if event.key == pygame.K_c:
            game.world.player_close_door()
        if event.key == pygame.K_p:
            game.world.player_pick_item()
        if event.key == pygame.K_g:
            game.switch_debug()

    if game.state == States.MENU:
        if event.key == pygame.K_n:
            new_game(game)
        if event.key == pygame.K_l:
            load_game(game)
        if event.key == pygame.K_p:
            pause_game(game)
        if event.key == pygame.K_q:
            quit_game(game)


def check_click(game, mouse_x, mouse_y):
    game.world.set_mouse(mouse_x, mouse_y)
    if game.state == States.PLAY:
        game.world.mouse_clicked()


def check_buttons(game, mouse_x, mouse_y):
    game.world.set_mouse(mouse_x, mouse_y)
    for button in game.main_menu.buttons:
        button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
        if game.state == States.MENU:
            if button_clicked:
                if button.id == 'play':
                    play_game(game)
                if button.id == 'load':
                    load_game(game)
                if button.id == 'new':
                    new_game(game)
                if button.id == 'quit':
                    quit_game(game)


def check_buttons_hover(game, mouse_x, mouse_y):
    if game.state == States.MENU:
        for button in game.main_menu.buttons:
            button_hover = button.rect.collidepoint(mouse_x, mouse_y)
            if button_hover:
                button.hover = True
            else:
                button.hover = False


def play_game(game):
    game.state = States.PLAY


def load_game(game):
    game.state = States.LOAD
    if game.save_exist:
        game.load()


def new_game(game):
    game.new()


def pause_game(game):
    game.state = States.MENU


def quit_game(game):
    if game.state == States.MENU:
        sys.exit()
    else:
        game.state = States.MENU
