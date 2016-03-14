#!/usr/bin/python

import pygame
import sys
from pygame.locals import *

from projectile import Projectile

class LaserProjectile(Projectile):
    size = 10
    x_coordinate = 0
    y_coordinate = 0
    old_x_coordinate = 0
    old_y_coordinate = 0
    speed = 4
    speed_count = 0
    direction = None

    def __init__(self, character):
        Projectile.__init__(self, self)
        self.x_coordinate = character.x_coordinate
        self.y_coordinate = character.y_coordinate
        self.old_x_coordinate = self.x_coordinate
        self.old_y_coordinate = self.y_coordinate
        self.direction = character.direction
        Projectile.projectile_count += 1
        Projectile.piercing_projectile_list.append(self)

    def drawProjectile(self, game, color, erase_color):
        old_laser_projectile = pygame.draw.circle(game, erase_color, (self.old_x_coordinate, self.old_y_coordinate), self.size, 0)
        laser_projectile = pygame.draw.circle(game, color, (self.x_coordinate, self.y_coordinate), self.size, 0)

        self.old_x_coordinate = self.x_coordinate
        self.old_y_coordinate = self.y_coordinate

    def remove(self, game, erase_color):
        remove_old_laser_projectile = pygame.draw.circle(game, erase_color, (self.old_x_coordinate, self.old_y_coordinate), self.size, 0)
        remove_laser_projectile = pygame.draw.circle(game, erase_color, (self.x_coordinate, self.y_coordinate), self.size, 0)
        Projectile.projectile_list.remove(self)

    def move(self, mouse_x, mouse_y):
        if self.speed_count == self.speed:
            movement = (mouse_x - self.x_coordinate, mouse_y - self.y_coordinate)
            self.x_coordinate = movement[0]
            self.y_coordinate = movement[1]
            self.speed_count = 0

        self.speed_count += 1

        return
