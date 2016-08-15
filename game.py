# Thanks to MillionthVector for the sprites
import os
import random
import pygame
import sys
import ctypes
import mysql.connector
from pygame.locals import *

from option import Option

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

# insert high score record
def insertPlayerRecord(name, total_kills, total_deaths, blue_kills, green_kills, red_kills, purple_kills, shots_fired, shots_hit, accuracy):
    # establish connection to the server
    connection = mysql.connector.connect(user = config.USER, password = config.PASSWORD, host = config.HOST, database = config.DATABASE)

    cursor = connection.cursor(buffered = True)

    # insert player with name, and score
    addPlayer = ("INSERT INTO high_scores "
           "(name, total_kills, total_deaths, blue_kills, green_kills, red_kills, purple_kills, shots_fired, shots_hit, accuracy)"
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    dataPlayer = (name, total_kills, total_deaths, blue_kills, green_kills, red_kills, purple_kills, shots_fired, shots_hit, accuracy)

    cursor.execute(addPlayer, dataPlayer)
    connection.commit()

    # close the connection to the database
    cursor.close()
    connection.close()

def drawMainMenu(DISPLAYSURF):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        for option in mainMenuOptions:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                #sound_hover_menu_item.play()
                if event.type == MOUSEBUTTONUP:
                    # play sound
                    sound_select_menu_item.play()

                    if option.text == "PLAY":
                        DISPLAYSURF.fill((0,0,0))
                        return False
                    if option.text == "SETTINGS":
                        DISPLAYSURF.fill((0,0,0))
                        return False
                    if option.text == "QUIT":
                        pygame.quit()
                        sys.exit()
            else:
                option.hovered = False
            option.draw()

    pygame.display.update()
    return True

def drawPlayAgainMenu(DISPLAYSURF):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        for option in playAgainMenuOptions:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                #sound_hover_menu_item.play()
                if event.type == MOUSEBUTTONUP:
                    # play sound
                    sound_select_menu_item.play()

                    if option.text == "YES":
                        os.execl(sys.executable, sys.executable, *sys.argv)
                        return False
                    if option.text == "NO":
                        pygame.quit()
                        sys.exit()
            else:
                option.hovered = False
            option.draw()

    pygame.display.update()
    return True

def drawStatsMenu(DISPLAYSURF):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # center the text
    center = config.display_y // 2

    killsText = font.render("Kills: " + str(statistics.total_kills), True, WHITE, BLACK)
    killsRect = (100, center - 200)
    DISPLAYSURF.blit(killsText, killsRect)

    deathsText = font.render("Deaths: " + str(statistics.total_deaths), True, WHITE, BLACK)
    deathsRect = (100, center - 150)
    DISPLAYSURF.blit(deathsText, deathsRect)

    blueKillsText = font.render("Blue Kills: " + str(statistics.blue_kills), True, WHITE, BLACK)
    blueKillsRect = (100, center - 100)
    DISPLAYSURF.blit(blueKillsText, blueKillsRect)

    greenKillsText = font.render("Green Kills: " + str(statistics.green_kills), True, WHITE, BLACK)
    greenKillsRect = (100, center - 50)
    DISPLAYSURF.blit(greenKillsText, greenKillsRect)

    redKillsText = font.render("Red Kills: " + str(statistics.red_kills), True, WHITE, BLACK)
    redKillsRect = (100, center)
    DISPLAYSURF.blit(redKillsText, redKillsRect)

    purpleKillsText = font.render("Purple Kills: " + str(statistics.purple_kills), True, WHITE, BLACK)
    purpleKillsRect = (100, center + 50)
    DISPLAYSURF.blit(purpleKillsText, purpleKillsRect)

    shotsFiredText = font.render("Shots Fired: " + str(int(statistics.shots_fired)), True, WHITE, BLACK)
    shotsFiredRect = (100, center + 100)
    DISPLAYSURF.blit(shotsFiredText, shotsFiredRect)

    shotsHitText = font.render("Shots Hit: " + str(int(statistics.shots_hit)), True, WHITE, BLACK)
    shotsHitRect = (100, center + 150)
    DISPLAYSURF.blit(shotsHitText, shotsHitRect)

    accuracyText = font.render("Accuracy: " + str(statistics.accuracy), True, WHITE, BLACK)
    accuracyRect = (100, center + 200)
    DISPLAYSURF.blit(accuracyText, accuracyRect)

    pygame.display.update()

def collisionDetection(game, erase_color, enemies, projectiles, character):
    for enemy in enemies:
        # player and enemies
        if abs(enemy.x_coordinate - character.x_coordinate) <= character.size and abs(enemy.y_coordinate - character.y_coordinate) <= character.size:

            # play sound
            sound_death.play()

            # update stats
            statistics.total_deaths += 1

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

                # play sound
                sound_enemy_hit.play()

                if projectile in projectile.getProjectileList():
                    projectile.remove(game, erase_color)
                # update statistics
                statistics.total_kills += 1
                statistics.shots_hit += 1
                if type(enemy) is BlueEnemy:
                    statistics.blue_kills += 1
                if type(enemy) is GreenEnemy:
                    statistics.green_kills += 1
                if type(enemy) is RedEnemy:
                    statistics.red_kills += 1
                if type(enemy) is PurpleEnemy:
                    statistics.purple_kills += 1

                # upgrade ship
                if statistics.total_kills % 50 == 0 and int(my_character.ship_rank) < 4:
                    my_character.ship_rank = str(int(my_character.ship_rank) + 1)

                    # play sound
                    sound_ship_upgrade.play()

# events
def eventBlueCorner():
    # generate random corner
    corner = randint(1, 4)
    # generate a random number based on difficulty
    blues_generated = random.uniform(config.difficulty, config.difficulty * 2)
    while blues_generated > 0:
        # initialize each blue enemy in a random location based on corner
        # top left
        if corner == 1:
            new_blue_x = randint(0, 100)
            new_blue_y = randint(0, 100)
        # top right
        if corner == 2:
            new_blue_x = randint(config.display_x - 100, config.display_x)
            new_blue_y = randint(0, 100)
        # bottom left
        if corner == 3:
            new_blue_x = randint(0, 100)
            new_blue_y = randint(config.display_y - 100, config.display_y)
        if corner == 4:
        # bottom right
            new_blue_x = randint(config.display_x - 100, config.display_x)
            new_blue_y = randint(config.display_y - 100, config.display_y)

        new_blue_enemy = BlueEnemy(new_blue_x, new_blue_y)
        blues_generated -= 1



pygame.init()

config = Config()
statistics = Statistics()

fpsClock = pygame.time.Clock()
fpsClock.tick(config.FPS)

user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
config.display_x = screenSize[0]
config.display_y = screenSize[1]

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
my_character = Character(config.display_x//2, config.display_y//2, "Basic", ("red", "1", ""))

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

# purple enemy init
purple_enemy = PurpleEnemy(0, 0)

# initialize mouse position
mouse_x = 0
mouse_y = 0


# attempt ship rotate to cursor
space_ship = pygame.image.load("images/ships/blue/1/-north.png").convert_alpha()

# set menu booleans
intro = True
playAgainMenu = True

# set font
font = pygame.font.Font(None, 40)

# set up the text for score
scoreText = font.render("Score: ", True, WHITE, BLACK)
textRect = scoreText.get_rect()

# set up the text for stats
killsText = font.render("Kills: ", True, WHITE, BLACK)
killsRect = killsText.get_rect()

deathsText = font.render("Deaths: ", True, WHITE, BLACK)
deathsRect = deathsText.get_rect()

blueKillsText = font.render("Blue Kills: ", True, WHITE, BLACK)
blueKillsRect = blueKillsText.get_rect()

greenKillsText = font.render("Green Kills: ", True, WHITE, BLACK)
greenKillsRect = greenKillsText.get_rect()

redKillsText = font.render("Red Kills: ", True, WHITE, BLACK)
redKillsRect = redKillsText.get_rect()

purpleKillsText = font.render("Purple Kills: ", True, WHITE, BLACK)
purpleKillsRect = purpleKillsText.get_rect()

shotsFiredText = font.render("Shots Fired: ", True, WHITE, BLACK)
shotsFiredRect = shotsFiredText.get_rect()

shotsHitText = font.render("Shots Hit: ", True, WHITE, BLACK)
shotsHitRect = shotsHitText.get_rect()

accuracyText = font.render("Accuracy: ", True, WHITE, BLACK)
accuracyRect = accuracyText.get_rect()

# set main menu options
mainMenuOptions = [Option(DISPLAYSURF, BLUE, font, "PLAY", (config.display_x // 2 - 40, config.display_y // 2 - 100)), Option(DISPLAYSURF, BLUE, font, "SETTINGS", (config.display_x // 2 - 80, config.display_y // 2)),
           Option(DISPLAYSURF, BLUE, font, "QUIT", (config.display_x // 2 - 40, config.display_y // 2 + 100))]

# set up sounds
pygame.mixer.init(frequency=22050, size=-16, channels=8, buffer=4096)

pygame.mixer.music.load("audio/background_music.wav")
pygame.mixer.music.play(-1)

sound_select_menu_item = pygame.mixer.Sound("audio/select_menu_item.wav")
sound_hover_menu_item = pygame.mixer.Sound("audio/hover_menu_item.wav")
sound_shoot = pygame.mixer.Sound("audio/laser_shot.wav")
sound_enemy_hit = pygame.mixer.Sound("audio/enemy_hit.wav")
sound_death = pygame.mixer.Sound("audio/death.wav")
sound_ship_upgrade = pygame.mixer.Sound("audio/ship_upgrade.wav")

while True:
    #draw the main menu
    while intro:
        intro = drawMainMenu(DISPLAYSURF)

    # set the game_state
    game_state = [my_character, proj.getProjectileList()]

    # draw the text's background rectangle onto the surface
    pygame.draw.rect(DISPLAYSURF, WHITE, (textRect.left, textRect.top, textRect.width, textRect.height))

    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos

        # shoot on mouse click
        if event.type == MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            my_character.shoot(DISPLAYSURF, WHITE, BLACK, my_character, mouse_x, mouse_y)

            # play sound
            sound_shoot.play()

            # update stats
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
        blues_generated = random.uniform(config.difficulty, config.difficulty + 1)
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
        greens_generated = random.uniform(config.difficulty, config.difficulty + 1)
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
        purples_generated = random.uniform(config.difficulty, config.difficulty + 1)
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

    # generate new events
    if config.event_spawn_speed_count == config.event_spawn_speed:
        eventBlueCorner()
        config.event_spawn_speed_count = 0
    else:
        config.event_spawn_speed_count += 1

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
        # add player to the database
        insertPlayerRecord(statistics.name, statistics.total_kills, statistics.total_deaths, statistics.blue_kills, statistics.green_kills, statistics.red_kills, statistics.purple_kills, statistics.shots_fired, statistics.shots_hit, statistics.accuracy)

        # clear the display and show the play again menu
        DISPLAYSURF.fill((0,0,0))
        playAgainMenuOptions = [Option(DISPLAYSURF, WHITE, font, "PLAY AGAIN?", (config.display_x // 2 - 100, config.display_y // 2 - 100)), Option(DISPLAYSURF, BLUE, font, "YES", (config.display_x // 2 - 30, config.display_y // 2)),
           Option(DISPLAYSURF, BLUE, font, "NO", (config.display_x // 2 - 20, config.display_y // 2 + 100))]
        while(playAgainMenu):
            playAgainMenu = drawPlayAgainMenu(DISPLAYSURF)
            drawStatsMenu(DISPLAYSURF)

    # update statistics
    if statistics.shots_fired != 0:
        statistics.accuracy = statistics.shots_hit / statistics.shots_fired
        statistics.accuracy = round(statistics.accuracy, 2)

    # slowly step the difficulty up
    config.difficulty += config.difficulty_scaler

    # draw the score onto the surface
    scoreText = font.render("Score: " + str(statistics.total_kills), True, WHITE, BLACK)
    textRect = scoreText.get_rect()
    DISPLAYSURF.blit(scoreText, textRect)

    pygame.display.update()
