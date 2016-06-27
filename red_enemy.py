#!/usr/bin/python

import pygame
import sys
from pygame.locals import *

from random import randint

from enemy import Enemy

class RedEnemy(Enemy):
    size = 6
    length = 150

    # lower accuracy value = more accurate
    accuracy = 5
    accuracy_count = 0

    x_coordinate = 0
    y_coordinate = 0

    # lower speed value = faster
    spawn_speed = 4000
    spawn_speed_count = 0
    speed = 8
    speed_count = 0

    def __init__(self, x_start, y_start):
        Enemy.__init__(self)
        if Enemy.red_enemy_count == -1:
            Enemy.red_enemy_count += 1
            return
        self.location_list = []

        self.x_coordinate = x_start
        self.y_coordinate = y_start

        self.location_list.append([self.x_coordinate, self.y_coordinate])

        Enemy.enemy_count += 1
        Enemy.enemy_list.append(self)
        Enemy.red_enemy_count += 1
        Enemy.red_enemy_list.append(self)

    def drawRedEnemy(self, game, color, erase_color):
        if len(self.location_list) >= self.length:
            old_red_enemy = pygame.gfxdraw.aacircle(game, (self.location_list[len(self.location_list)-self.length])[0], (self.location_list[len(self.location_list)-self.length])[1], self.size + 1, erase_color)
            old_red_enemy = pygame.gfxdraw.filled_circle(game, (self.location_list[len(self.location_list)-self.length])[0], (self.location_list[len(self.location_list)-self.length])[1], self.size + 1, erase_color)
            self.location_list.remove(self.location_list[len(self.location_list)-self.length])
        for index in self.location_list:
            red_enemy = pygame.gfxdraw.aacircle(game, index[0], index[1], self.size, color)

        return

    def gotHit(self, game, erase_color):
        # prevent "x not in list" error
        for index in self.location_list:
            # hit_old_red_enemy = pygame.gfxdraw.aacircle(game, (self.location_list[len(self.location_list)-self.length])[0], (self.location_list[len(self.location_list)-self.length])[1], self.size + 1, erase_color)
            # hit_old_red_enemy = pygame.gfxdraw.filled_circle(game, (self.location_list[len(self.location_list)-self.length])[0], (self.location_list[len(self.location_list)-self.length])[1], self.size + 1, erase_color)
            hit_red_enemy = pygame.gfxdraw.filled_circle(game, index[0], index[1], self.size + 1, erase_color)
        del self.location_list[:]

        if self in Enemy.enemy_list:
            Enemy.enemy_list.remove(self)
        if self in Enemy.red_enemy_list:
            Enemy.red_enemy_list.remove(self)

        return

    def move(self, character):
        if self.speed_count == self.speed:
            if self.accuracy_count >= self.accuracy:
                if self.x_coordinate - character.x_coordinate >= 0:
                    self.x_coordinate -= 3
                else:
                    self.x_coordinate += 3

                if self.y_coordinate - character.y_coordinate > 0:
                    self.y_coordinate -= 3
                else:
                    self.y_coordinate += 3

                if self.x_coordinate - character.x_coordinate > 0:
                    self.x_coordinate -= 3
                else:
                    self.x_coordinate += 3

                if self.y_coordinate - character.y_coordinate > 0:
                    self.y_coordinate -= 3
                else:
                    self.y_coordinate += 3
                self.speed_count = 0
                self.accuracy_count = 0

            else:
            # get a new random point within 50px
                self.x_coordinate = randint(self.x_coordinate - 3, self.x_coordinate + 3)
                self.y_coordinate = randint(self.y_coordinate - 3, self.y_coordinate + 3)
                self.speed_count = 0
                self.accuracy_count += 1

            if [self.x_coordinate, self.y_coordinate] not in self.location_list:
                self.location_list.append([self.x_coordinate, self.y_coordinate])

        self.speed_count += 1
