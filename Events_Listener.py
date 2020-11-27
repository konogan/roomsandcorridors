# encoding: utf-8

import sys
import pygame


def check_events(game):
    # respond to events
    # delegate to differnet module
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game(game)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_buttons(game, mouse_x, mouse_y)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_buttons_hover(game, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown(event, game)
        elif event.type == pygame.KEYUP:
            check_keyup(event, game)


def check_keydown(event, game):
    if event.key == pygame.K_ESCAPE:
        if game.stats.game_active:
            pause_game(game)
        else:
            play_game(game)


def check_keyup(event, game):
    if event.key == pygame.K_RIGHT:
        game.world.move_player_intent((1,0))
    if event.key == pygame.K_LEFT:
        game.world.move_player_intent((-1,0))
    if event.key == pygame.K_UP:
        game.world.move_player_intent((0,-1))
    if event.key == pygame.K_DOWN:
        game.world.move_player_intent((0,1))
    if event.key == pygame.K_n:
        new_game(game)
    if event.key == pygame.K_l:
        load_game(game)
    if event.key == pygame.K_p:
        pause_game(game)
    if event.key == pygame.K_q:
        quit_game(game)


def check_buttons(game, mouse_x, mouse_y):
    for button in game.main_menu.buttons:
        button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked:
            if button.id == 'play':
                play_game(game)
            if button.id == 'load':
                load_game(game)
            if button.id == 'new':
                new_game(game)
            if button.id == 'quit':
                if not game.stats.game_active:
                    quit_game(game)


def check_buttons_hover(game, mouse_x, mouse_y):
    for button in game.main_menu.buttons:
        button_hover = button.rect.collidepoint(mouse_x, mouse_y)
        if button_hover:
            button.hover = True
        else:
            button.hover = False


def play_game(game):
    game.stats.game_active = True


def load_game(game):
    if game.save_exist:
        game.load()
        game.stats.game_active = True


def new_game(game):
    game.new()
    game.stats.game_active = True


def pause_game(game):
    game.stats.game_active = False


def quit_game(game):
    game.stats.game_active = False
    # save ?
    sys.exit()
