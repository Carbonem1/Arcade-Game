#!/usr/bin/python

import pygame
import sys
import math
from pygame.locals import *
from pygame import gfxdraw

from enemy import Enemy

class BlueEnemy(object, Enemy):
    size = 20
    x_coordinate = 0
    y_coordinate = 0
    old_x_coordinate = 0
    old_y_coordinate = 0
    spawn_speed = 400
    spawn_speed_count = 0
    speed = 5
    speed_count = 0
    movement_vector = 0

    def __init__(self, x_start, y_start):
        Enemy.__init__(self)
        if Enemy.blue_enemy_count == -1:
            Enemy.blue_enemy_count += 1
            return
        self.x_coordinate = x_start
        self.y_coordinate = y_start
        self.old_x_coordinate = x_start
        self.old_y_coordinate = y_start
        Enemy.enemy_count += 1
        Enemy.enemy_list.append(self)
        Enemy.blue_enemy_count += 1
        Enemy.blue_enemy_list.append(self)

    def drawBlueEnemy(self, game, color, erase_color):
        # erase our old character position and draw the new one

        old_blue_enemy = pygame.gfxdraw.aacircle(game, int(self.old_x_coordinate), int(self.old_y_coordinate), self.size + 1, erase_color)
        old_blue_enemy = pygame.gfxdraw.filled_circle(game, int(self.old_x_coordinate), int(self.old_y_coordinate), self.size + 1, erase_color)

        blue_enemy = pygame.gfxdraw.aacircle(game, int(self.x_coordinate), int(self.y_coordinate), self.size, color)
        #blue_enemy = pygame.gfxdraw.filled_circle(game, self.x_coordinate, self.y_coordinate, self.size, color)

        # set old position to be current for next redraw
        self.old_x_coordinate = self.x_coordinate
        self.old_y_coordinate = self.y_coordinate

        return

    def gotHit(self, game, erase_color):
        hit_old_blue_enemy = pygame.gfxdraw.aacircle(game, int(self.old_x_coordinate), int(self.old_y_coordinate), self.size + 1, erase_color)
        hit_old_blue_enemy = pygame.gfxdraw.filled_circle(game, int(self.old_x_coordinate), int(self.old_y_coordinate), self.size + 1, erase_color)

        hit_blue_enemy = pygame.gfxdraw.aacircle(game, int(self.x_coordinate), int(self.y_coordinate), self.size, erase_color)
        # prevent "x not in list" error
        if self in Enemy.enemy_list:
            Enemy.enemy_list.remove(self)
        if self in Enemy.blue_enemy_list:
            Enemy.blue_enemy_list.remove(self)
        return

    def move(self, character):
        if self.speed_count == self.speed:
            distance = [character.x_coordinate - self.x_coordinate, character.y_coordinate - self.y_coordinate]
            norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
            direction = [distance[0] / norm, distance[1] / norm]
            self.movement_vector = [direction[0], direction[1]]

            self.x_coordinate += self.movement_vector[0]
            self.y_coordinate += self.movement_vector[1]
            self.speed_count = 0

        self.speed_count += 1

        return
