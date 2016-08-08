# Thanks to MillionthVector for the sprites
import os
import pygame
import sys
from pygame.locals import *
from option import Option

import random
from random import randint

from config import Config
from statistics import Statistics

from character import Character
from projectile import Projectile
from basic_projectile import BasicProjectile
from piercing_projectile import PiercingProjectile

from enemy import Enemy
from blue_enemy import BlueEnemy
from green_enemy import GreenEnemy
from red_enemy import RedEnemy
from purple_enemy import PurpleEnemy

def drawMenu(DISPLAYSURF):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                if event.type == MOUSEBUTTONUP:
                    if option.text == "PLAY":
                        DISPLAYSURF.fill((0,0,0))
                        return False
                    if option.text == "SETTINGS":
                        DISPLAYSURF.fill((0,0,0))
                        return False
                    if option.text == "QUIT":
                        pygame.quit()
                        quit()
            else:
                option.hovered = False
            option.draw()

    pygame.display.update()
    return True

def collisionDetection(game, erase_color, enemies, projectiles, character):
    for enemy in enemies:
        # player and enemies
        if abs(enemy.x_coordinate - character.x_coordinate) <= character.size and abs(enemy.y_coordinate - character.y_coordinate) <= character.size:
            statistics.deaths += 1
            if int(my_character.ship_rank) > 1:
                my_character.ship_rank = str(int(my_character.ship_rank) - 1)
                enemy.gotHit(game, erase_color)
                return False
            else:
                return True

        # projectiles and enemies
        for projectile in projectiles:
            if abs(enemy.x_coordinate - projectile.x_coordinate) <= enemy.size and abs(enemy.y_coordinate - projectile.y_coordinate) <= enemy.size:
                enemy.gotHit(game, erase_color)
                if not projectile in projectile.getPiercingProjectileList():
                    projectile.remove(game, erase_color)
                statistics.total_kills += 1
                statistics.shots_hit += 1
                # upgrade ship
                if statistics.total_kills % 10 == 0 and int(my_character.ship_rank) < 4:
                    my_character.ship_rank = str(int(my_character.ship_rank) + 1)

pygame.init()

config = Config()
statistics = Statistics()

fpsClock = pygame.time.Clock()
fpsClock.tick(config.FPS)

# create the display surface
DISPLAYSURF = pygame.display
DISPLAYSURF = pygame.display.set_mode((config.display_x, config.display_y), pygame.FULLSCREEN)

# set the game name
pygame.display.set_caption(config.game_name)

# set the game icon
icon = pygame.image.load(config.game_icon)
pygame.display.set_icon(icon)
pygame.display.set_caption(config.game_name, config.game_icon)

# set the mouse to be invisible
# pygame.mouse.set_visible(False)

# colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)
PURPLE = (160, 32, 240)

# set background color
background_color = BLACK
DISPLAYSURF.fill(background_color)

# player init coordinates
my_character = Character(config.display_x//2, config.display_y//2, "1", ("red", "1", ""))

# player projectile
proj = BasicProjectile(my_character)

# enemy init
enemy = Enemy()

# blue enemy init
blue_enemy = BlueEnemy(0, 0)

# green enemy init
green_enemy = GreenEnemy(0, 0)

# red enemy init
red_enemy = RedEnemy(0, 0)

# red enemy init
purple_enemy = PurpleEnemy(0, 0)

mouse_x = 0
mouse_y = 0

# set up fonts
basicFont = pygame.font.SysFont(None, 30)
# set up the text for the menu
menuText = basicFont.render("Welcome to " + config.game_name + "! Pick a ship.", True, WHITE, BLACK)
menuRect = menuText.get_rect()

# set up the text for score
text = basicFont.render("Score: ", True, WHITE, BLACK)
textRect = text.get_rect()

# attempt ship rotate to cursor
#mousec = pygame.image.load(mouse_c).convert_alpha()
space_ship = pygame.image.load("images/ships/blue/1/-north.png").convert_alpha()

intro = True

menu_font = pygame.font.Font(None, 40)
options = [Option(DISPLAYSURF, BLUE, menu_font, "PLAY", (config.display_x // 2 - 40, config.display_y // 2 - 100)), Option(DISPLAYSURF, BLUE, menu_font, "SETTINGS", (config.display_x // 2 - 80, config.display_y // 2)),
           Option(DISPLAYSURF, BLUE, menu_font, "QUIT", (config.display_x // 2 - 40, config.display_y // 2 + 100))]

while True:
    #draw the main menu
    while intro:
        intro = drawMenu(DISPLAYSURF)

    # set the game_state
    game_state = [my_character, proj.getProjectileList()]

    # draw the text's background rectangle onto the surface
    pygame.draw.rect(DISPLAYSURF, WHITE, (textRect.left, textRect.top, textRect.width, textRect.height))

    # draw the text onto the surface
    text = basicFont.render("Score: " + str(statistics.total_kills), True, WHITE, BLACK)
    DISPLAYSURF.blit(text, textRect)

    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos

        # shoot on mouse click
        if event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            my_character.shoot(DISPLAYSURF, WHITE, BLACK, my_character, mouse_x, mouse_y)
            statistics.shots_fired += 1

        # quit on exit
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # draw my character
    my_character.drawCharacter(DISPLAYSURF, RED, background_color, mouse_x, mouse_y)

    # checking pressed keys for movement
    keys = pygame.key.get_pressed()
    # check legal moves
    legal_moves = my_character.getLegalMoves(config)
    if my_character.speed_count == my_character.speed:
        if "UP" in legal_moves:
            if keys[pygame.K_w]:
                my_character.y_coordinate -= 1
        if "DOWN" in legal_moves:
            if keys[pygame.K_s]:
                my_character.y_coordinate += 1
        if "RIGHT" in legal_moves:
            if keys[pygame.K_d]:
                my_character.x_coordinate += 1
        if "LEFT" in legal_moves:
            if keys[pygame.K_a]:
                my_character.x_coordinate -= 1
        my_character.speed_count = 0
    my_character.speed_count += 1

    # generate new blue enemies
    if blue_enemy.spawn_speed_count == blue_enemy.spawn_speed:
        # generate a random number based on difficulty
        blues_generated = random.uniform(config.difficulty // 2.0, config.difficulty)
        while blues_generated > 0:
            # initialize each blue enemy in a random location
            new_blue_x = randint(0, config.display_x)
            new_blue_y = randint(0, config.display_y)
            # if it is too close to the player, dont spawn
            if not (abs(new_blue_x - my_character.x_coordinate) <= (my_character.size + config.spawn_buffer) and abs(new_blue_y - my_character.y_coordinate) <= (my_character.size + config.spawn_buffer)):
                new_blue_enemy = BlueEnemy(new_blue_x, new_blue_y)
                blues_generated -= 1
        blue_enemy.spawn_speed_count = 0
    blue_enemy.spawn_speed_count += 1

    # generate new green enemies
    if green_enemy.spawn_speed_count == green_enemy.spawn_speed:
        # generate a random number based on difficulty
        greens_generated = random.uniform(config.difficulty // 2.0, config.difficulty)
        while greens_generated > 0:
            # initialize each green enemy in a random location
            new_green_x = randint(0, config.display_x)
            new_green_y = randint(0, config.display_y)
            # if it is too close to the player, dont spawn
            if not (abs(new_green_x - my_character.x_coordinate) <= (my_character.size + config.spawn_buffer) and abs(new_green_y - my_character.y_coordinate) <= (my_character.size + config.spawn_buffer)):
                new_green_enemy = GreenEnemy(new_green_x, new_green_y)
                greens_generated -= 1
        green_enemy.spawn_speed_count = 0
    green_enemy.spawn_speed_count += 1

    # generate new red enemies
    if red_enemy.spawn_speed_count == red_enemy.spawn_speed:
        # generate a random number based on difficulty
        reds_generated = random.uniform(0, 1)
        while reds_generated > 0:
            # initialize each red enemy in a random location
            new_red_x = randint(0, config.display_x)
            new_red_y = randint(0, config.display_y)
            # if it is too close to the player, dont spawn (also, dont let it spawn longer than 50px)
            if not ((abs(new_red_x - my_character.x_coordinate) <= (my_character.size + config.spawn_buffer)) and (abs(new_red_y - my_character.y_coordinate) <= (my_character.size + config.spawn_buffer))):
                new_red_enemy = RedEnemy(new_red_x, new_red_y)
                reds_generated -= 1
        red_enemy.spawn_speed_count = 0
    red_enemy.spawn_speed_count += 1

    # generate new purple enemies
    if purple_enemy.spawn_speed_count == purple_enemy.spawn_speed:
        # generate a random number based on difficulty
        purples_generated = random.uniform(config.difficulty // 2.0, config.difficulty)
        while purples_generated > 0:
            # initialize each purple enemy in a random location
            new_purple_x = randint(0, config.display_x)
            new_purple_y = randint(0, config.display_y)
            # if it is too close to the player, dont spawn
            if not (abs(new_purple_x - my_character.x_coordinate) <= (my_character.size + config.spawn_buffer) and abs(new_purple_y - my_character.y_coordinate) <= (my_character.size + config.spawn_buffer)):
                new_purple_enemy = PurpleEnemy(new_purple_x, new_purple_y)
                purples_generated -= 1
        purple_enemy.spawn_speed_count = 0
    purple_enemy.spawn_speed_count += 1

    # draw in any blue enemies
    for enemy in blue_enemy.getBlueEnemyList():
        enemy.drawBlueEnemy(DISPLAYSURF, BLUE, background_color)

    # draw in any green enemies
    for enemy in green_enemy.getGreenEnemyList():
        enemy.drawGreenEnemy(DISPLAYSURF, GREEN, background_color)

    # draw in any red enemies
    for enemy in red_enemy.getRedEnemyList():
        enemy.drawRedEnemy(DISPLAYSURF, RED, background_color)

    # draw in any purple enemies
    for enemy in purple_enemy.getPurpleEnemyList():
        enemy.drawPurpleEnemy(DISPLAYSURF, PURPLE, background_color)

    # draw in any projectiles
    for projectile in proj.getProjectileList():
        projectile.drawProjectile(DISPLAYSURF, WHITE, background_color)

    # set all blue enemies in motion
    for enemy in blue_enemy.getBlueEnemyList():
            enemy.move(my_character)

    # set all green enemies in motion
    for enemy in green_enemy.getGreenEnemyList():
            enemy.move(my_character)

    # set all red enemies in motion
    for enemy in red_enemy.getRedEnemyList():
            enemy.move(my_character)

    # set all purple enemies in motion
    for enemy in purple_enemy.getPurpleEnemyList():
            enemy.move(game_state)

    # set all projectiles in motion
    for projectile in proj.getProjectileList():
        if (-20 < projectile.x_coordinate < config.display_x + 20) and (-20 < projectile.y_coordinate < config.display_y + 20):
            projectile.move(mouse_x, mouse_y)
        else:
            projectile.remove(DISPLAYSURF, BLACK)

    # check for any collisions
    if collisionDetection(DISPLAYSURF, BLACK, enemy.getEnemyList(), proj.projectile_list, my_character) == True:
        print "FINAL SCORE: ", statistics.total_kills
        print "Replay? (y/n)"
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        os.execl(sys.executable, sys.executable, *sys.argv)
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()

    # update statistics
    if statistics.shots_fired != 0:
        statistics.accuracy = statistics.shots_hit / statistics.shots_fired

    # slowly step the difficulty up
    config.difficulty += config.difficulty_scaler

    pygame.display.update()
