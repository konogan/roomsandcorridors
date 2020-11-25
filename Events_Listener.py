# encoding: utf-8

import sys
import pygame

def check_events(settings, screen, stats, mainmenu,  world):
    # respond to events
    # delegate to differnet module
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Merci de save')
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_buttons(mainmenu,stats,mouse_x, mouse_y,world)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_buttons_hover(mainmenu,stats,mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown(event,stats, settings, screen, world)
        elif event.type == pygame.KEYUP:
            check_keyup(event,stats, settings, screen, world)

  
def check_keydown(event,stats, settings, screen, world):
    if event.key == pygame.K_ESCAPE:
        if stats.game_active:
            stats.game_active = False
        else :
            stats.game_active = True
    if event.key == pygame.K_RIGHT:
        print("Right down")
    if event.key == pygame.K_LEFT:
        print("Left down")

def check_keyup(event,stats, settings, screen, world):
    if event.key == pygame.K_RIGHT:
        print("Right up")
    if event.key == pygame.K_LEFT:
        print("Left up")
    if event.key == pygame.K_n:
        world.init()
    if event.key == pygame.K_p:
        stats.game_active = True
    if event.key == pygame.K_q:
        if not stats.game_active:
            sys.exit()

def check_buttons(mainmenu,stats, mouse_x, mouse_y, world):
    for button in mainmenu.buttons:
        button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked:
            if button.id == 'play':
                stats.game_active = True
            if button.id == 'new':
                world.init()
                stats.game_active = True
            if button.id == 'quit':
                sys.exit()
        
def check_buttons_hover(mainmenu,stats, mouse_x, mouse_y):
    for button in mainmenu.buttons:
        button_hover = button.rect.collidepoint(mouse_x, mouse_y)
        if button_hover:
            button.hover = True
        else :
            button.hover = False
            
