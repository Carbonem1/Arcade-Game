#!/usr/bin/python

import pygame
import sys
from pygame.locals import *

from config import Config

from enemy import Enemy

class GreenEnemy(object, Enemy):
    config = Config()

    size = 10
    x_coordinate = 0
    y_coordinate = 0
    old_x_coordinate = 0
    old_y_coordinate = 0
    spawn_speed = 1600
    spawn_speed_min = 300
    spawn_speed_count = 0
    speed = 5
    speed_count = 0

    def __init__(self, x_start, y_start):
        Enemy.__init__(self)
        if Enemy.green_enemy_count == -1:
            Enemy.green_enemy_count += 1
            return
        self.x_coordinate = x_start
        self.y_coordinate = y_start
        self.old_x_coordinate = x_start
        self.old_y_coordinate = y_start
        Enemy.enemy_count += 1
        Enemy.enemy_list.append(self)
        Enemy.green_enemy_count += 1
        Enemy.green_enemy_list.append(self)

    def drawGreenEnemy(self, game, color, erase_color):
        # erase our old character position and draw the new one

        old_green_enemy = pygame.gfxdraw.aacircle(game, self.old_x_coordinate, self.old_y_coordinate, self.size + 1, erase_color)
        old_green_enemy = pygame.gfxdraw.filled_circle(game, self.old_x_coordinate, self.old_y_coordinate, self.size + 1, erase_color)

        green_enemy = pygame.gfxdraw.aacircle(game, self.x_coordinate, self.y_coordinate, self.size, color)
        #green_enemy = pygame.gfxdraw.filled_circle(game, self.x_coordinate, self.y_coordinate, self.size, color)

        # set old position to be current for next redraw
        self.old_x_coordinate = self.x_coordinate
        self.old_y_coordinate = self.y_coordinate

        return

    def gotHit(self, game, erase_color):
        hit_old_green_enemy = pygame.gfxdraw.aacircle(game, self.old_x_coordinate, self.old_y_coordinate, self.size + 1, erase_color)
        hit_old_green_enemy = pygame.gfxdraw.filled_circle(game, self.old_x_coordinate, self.old_y_coordinate, self.size + 1, erase_color)

        hit_green_enemy = pygame.gfxdraw.aacircle(game, self.x_coordinate, self.y_coordinate, self.size, erase_color)
        # prevent "x not in list" error
        if self in Enemy.enemy_list:
            Enemy.enemy_list.remove(self)
        if self in Enemy.green_enemy_list:
            Enemy.green_enemy_list.remove(self)

        return

    def move(self, character):
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
