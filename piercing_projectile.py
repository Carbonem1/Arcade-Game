#!/usr/bin/python

import pygame
import sys
import math
from pygame.locals import *

from projectile import Projectile

class PiercingProjectile(Projectile):
    size = 4
    initial_x_coordinate = 0
    initial_y_coordinate = 0
    x_coordinate = 0
    y_coordinate = 0
    old_x_coordinate = 0
    old_y_coordinate = 0
    speed = 3
    speed_count = 0
    bullet_vector = 0

    def __init__(self, character):
        Projectile.__init__(self, self)
        self.initial_x_coordinate = character.x_coordinate
        self.initial_y_coordinate = character.y_coordinate
        self.x_coordinate = character.x_coordinate
        self.y_coordinate = character.y_coordinate
        self.old_x_coordinate = self.x_coordinate
        self.old_y_coordinate = self.y_coordinate
        self.direction = character.direction
        Projectile.projectile_count += 1
        Projectile.piercing_projectile_list.append(self)

    def drawProjectile(self, game, color, erase_color):
        old_piercing_projectile = pygame.draw.circle(game, erase_color, (int(self.old_x_coordinate), int(self.old_y_coordinate)), self.size, 0)
        piercing_projectile = pygame.draw.circle(game, color, (int(self.x_coordinate), int(self.y_coordinate)), self.size, 0)

        self.old_x_coordinate = self.x_coordinate
        self.old_y_coordinate = self.y_coordinate

    def remove(self, game, erase_color):
        remove_old_piercing_projectile = pygame.draw.circle(game, erase_color, (int(self.old_x_coordinate), int(self.old_y_coordinate)), self.size, 0)
        remove_piercing_projectile = pygame.draw.circle(game, erase_color, (int(self.x_coordinate), int(self.y_coordinate)), self.size, 0)
        Projectile.projectile_list.remove(self)

    def move(self, mouse_x, mouse_y):
        if self.speed_count == self.speed:
            if self.bullet_vector == 0:
                distance = [mouse_x - self.initial_x_coordinate, mouse_y - self.initial_y_coordinate]
                norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
                direction = [distance[0] / norm, distance[1] / norm]
                self.bullet_vector = [direction[0], direction[1]]

            self.x_coordinate += self.bullet_vector[0]
            self.y_coordinate += self.bullet_vector[1]
            self.speed_count = 0

        self.speed_count += 1

        return
