# encoding: utf-8

import sys
import pygame

def check_events(game):
    # respond to events
    # delegate to differnet module
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Merci de save')
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_buttons(game,mouse_x, mouse_y)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_buttons_hover(game,mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown(event,game)
        elif event.type == pygame.KEYUP:
            check_keyup(event,game)

  
def check_keydown(event,game):
    if event.key == pygame.K_ESCAPE:
        if game.stats.game_active:
            game.stats.game_active = False
        else :
            game.stats.game_active = True
    if event.key == pygame.K_RIGHT:
        print("Right down")
    if event.key == pygame.K_LEFT:
        print("Left down")

def check_keyup(event,game):
    if event.key == pygame.K_RIGHT:
        print("Right up")
    if event.key == pygame.K_LEFT:
        print("Left up")
    if event.key == pygame.K_n:
        game.new()
    if event.key == pygame.K_p:
        game.stats.game_active = True
    if event.key == pygame.K_q:
        if not game.stats.game_active:
            sys.exit()

def check_buttons(game, mouse_x, mouse_y):
    for button in game.main_menu.buttons:
        button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked:
            if button.id == 'play':
                game.stats.game_active = True
            if button.id == 'new':
                game.new()
                game.stats.game_active = True
            if button.id == 'quit':
                sys.exit()
        
def check_buttons_hover(game, mouse_x, mouse_y):
    for button in game.main_menu.buttons:
        button_hover = button.rect.collidepoint(mouse_x, mouse_y)
        if button_hover:
            button.hover = True
        else :
            button.hover = False
            
