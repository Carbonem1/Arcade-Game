#!/usr/bin/python

import pygame
import sys
from pygame.locals import *

from enemy import Enemy

class GreenEnemy(Enemy):
    size = 10
    x_coordinate = 0
    y_coordinate = 0
    old_x_coordinate = 0
    old_y_coordinate = 0
    spawn_speed = 1600
    spawn_speed_count = 0
    speed = 15
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
        old_green_enemy = pygame.draw.circle(game, erase_color, (self.old_x_coordinate, self.old_y_coordinate), self.size, 0)
        green_enemy = pygame.draw.circle(game, color, (self.x_coordinate, self.y_coordinate), self.size, 0)

        # set old position to be current for next redraw
        self.old_x_coordinate = self.x_coordinate
        self.old_y_coordinate = self.y_coordinate

        return

    def gotHit(self, game, erase_color):
        hit_old_green_enemy = pygame.draw.circle(game, erase_color, (self.old_x_coordinate, self.old_y_coordinate), self.size, 0)
        hit_green_enemy = pygame.draw.circle(game, erase_color, (self.x_coordinate, self.y_coordinate), self.size, 0)
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
