#!/usr/bin/python

import pygame
import sys
from pygame.locals import *

from enemy import Enemy

from random import randint

class PurpleEnemy(object, Enemy):
    size = 30
    x_coordinate = 0
    y_coordinate = 0
    old_x_coordinate = 0
    old_y_coordinate = 0
    spawn_speed = 1200
    spawn_speed_count = 0
    speed = 40
    speed_count = 0
    dodge_speed = 2
    dodge_speed_count = 0

    def __init__(self, x_start, y_start):
        Enemy.__init__(self)
        if Enemy.purple_enemy_count == -1:
            Enemy.purple_enemy_count += 1
            return
        self.x_coordinate = x_start
        self.y_coordinate = y_start
        self.old_x_coordinate = x_start
        self.old_y_coordinate = y_start
        Enemy.enemy_count += 1
        Enemy.enemy_list.append(self)
        Enemy.purple_enemy_count += 1
        Enemy.purple_enemy_list.append(self)

    def drawPurpleEnemy(self, game, color, erase_color):
        # erase our old character position and draw the new one
        old_purple_enemy = pygame.gfxdraw.aacircle(game, self.old_x_coordinate, self.old_y_coordinate, self.size + 1, erase_color)
        old_purple_enemy = pygame.gfxdraw.filled_circle(game, self.old_x_coordinate, self.old_y_coordinate, self.size + 1, erase_color)

        purple_enemy = pygame.gfxdraw.aacircle(game, self.x_coordinate, self.y_coordinate, self.size, color)
        #purple_enemy = pygame.gfxdraw.filled_circle(game, self.x_coordinate, self.y_coordinate, self.size, color)

        # set old position to be current for next redraw
        self.old_x_coordinate = self.x_coordinate
        self.old_y_coordinate = self.y_coordinate

        return

    def gotHit(self, game, erase_color):
        hit_old_purple_enemy = pygame.gfxdraw.aacircle(game, self.old_x_coordinate, self.old_y_coordinate, self.size + 1, erase_color)
        hit_old_purple_enemy = pygame.gfxdraw.filled_circle(game, self.old_x_coordinate, self.old_y_coordinate, self.size + 1, erase_color)

        hit_purple_enemy = pygame.gfxdraw.aacircle(game, self.x_coordinate, self.y_coordinate, self.size, erase_color)
        # prevent "x not in list" error
        if self in Enemy.enemy_list:
            Enemy.enemy_list.remove(self)
        if self in Enemy.purple_enemy_list:
            Enemy.purple_enemy_list.remove(self)
        return

    def move(self, game_state):
        character = game_state[0]
        projectiles = game_state[1]

        if self.speed_count == self.speed:
            if self.x_coordinate - character.x_coordinate > 0:
                self.x_coordinate -= 1
            else:
                self.x_coordinate += 1

            if self.y_coordinate - character.y_coordinate > 0:
                self.y_coordinate -= 1
            else:
                self.y_coordinate += 1

            if self.x_coordinate - character.x_coordinate > 0:
                self.x_coordinate -= 1
            else:
                self.x_coordinate += 1

            if self.y_coordinate - character.y_coordinate > 0:
                self.y_coordinate -= 1
            else:
                self.y_coordinate += 1

            self.speed_count = 0
        self.speed_count += 1

        if self.dodge_speed_count == self.dodge_speed:
            for projectile in projectiles:
                # if ((self.x_coordinate - projectile.x_coordinate) == 0) and (abs(self.y_coordinate - projectile.y_coordinate) <= (self.size * 3)) and (projectile.direction == "NORTH" or projectile.direction == "SOUTH"):
                #     direction = randint(0, 1)
                #     print "NORTHSOUTH", direction
                #     if direction == 0:
                #         self.x_coordinate += 1
                #     if direction == 1:
                #         self.x_coordinate -= 1
                #
                # if ((self.y_coordinate - projectile.y_coordinate) == 0) and (abs(self.x_coordinate - projectile.x_coordinate) <= (self.size * 3)) and (projectile.direction == "EAST" or projectile.direction == "WEST"):
                #     direction = randint(0, 1)
                #     print "EASTWEST", direction
                #     if direction == 0:
                #         self.y_coordinate += 1
                #     if direction == 1:
                #         self.y_coordinate -= 1

                if (0 <= (self.x_coordinate - projectile.x_coordinate) <= (self.size * 2)) and (abs(self.y_coordinate - projectile.y_coordinate) <= (self.size * 2)) and (projectile.direction == "NORTH" or projectile.direction == "SOUTH"):
                    self.x_coordinate += 1

                if (-(self.size * 2) <= (self.x_coordinate - projectile.x_coordinate) < 0) and (abs(self.y_coordinate - projectile.y_coordinate) <= (self.size * 2)) and (projectile.direction == "NORTH" or projectile.direction == "SOUTH"):
                    self.x_coordinate -= 1

                if (0 <= (self.y_coordinate - projectile.y_coordinate) <= (self.size * 2)) and (abs(self.x_coordinate - projectile.x_coordinate) <= (self.size * 2)) and (projectile.direction == "EAST" or projectile.direction == "WEST"):
                    self.y_coordinate += 1

                if (-(self.size * 2) <= (self.y_coordinate - projectile.y_coordinate) < 0) and (abs(self.x_coordinate - projectile.x_coordinate) <= (self.size * 2)) and (projectile.direction == "EAST" or projectile.direction == "WEST"):
                    self.y_coordinate -= 1

                self.dodge_speed_count = 0
        self.dodge_speed_count += 1
