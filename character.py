#!/usr/bin/python

import pygame
import sys
from pygame.locals import *

import math

from enemy import Enemy
from projectile import Projectile
from basic_projectile import BasicProjectile
from piercing_projectile import PiercingProjectile

class Character():
    size = 40
    speed = 3
    speed_count = 0
    x_coordinate = 0
    y_coordinate = 0
    old_x_coordinate = 0
    old_y_coordinate = 0
    legal_moves = []
    direction = None
    ship_color = None
    ship_rank = None
    ship_name = None
    image = None
    image_rect = (0, 0)

    def __init__(self, x_start, y_start, image = None):
        self.x_coordinate = x_start
        self.y_coordinate = y_start
        self.old_x_coordinate = x_start
        self.old_y_coordinate = y_start
        self.ship_color, self.ship_rank, self.ship_name = image
        if not image == None:
            self.image = pygame.image.load("images/ships/" + self.ship_color + "/" + self.ship_rank + "/" + self.ship_name + "-east.png")
            self.image_rect = self.image.get_rect()

    def drawCharacter(self, game, color, erase_color, mouse_x = 0, mouse_y = 0):
        # if a ship is specified, get the ships direction and angle
        if not self.image == None:
            pos = mouse_x, mouse_y
            angle = 360 - math.atan2(pos[1] - self.y_coordinate, pos[0] - self.x_coordinate) * 180 / math.pi
            rotimage = pygame.transform.rotate(self.image, angle)
            rect = rotimage.get_rect(center=(self.x_coordinate, self.y_coordinate))
            my_old_character = pygame.draw.circle(game, erase_color, (self.old_x_coordinate, self.old_y_coordinate), self.size+10, 0)
            game.blit(rotimage, (self.x_coordinate-rotimage.get_width()/2, self.y_coordinate-rotimage.get_height()/2))
        else:
            # erase our old character position and draw the new one
            my_old_character = pygame.draw.circle(game, erase_color, (self.old_x_coordinate, self.old_y_coordinate), self.size, 0)
            my_character = pygame.draw.circle(game, color, (self.x_coordinate, self.y_coordinate), self.size, 0)

        # set old position to be current for next redraw
        self.old_x_coordinate = self.x_coordinate
        self.old_y_coordinate = self.y_coordinate

        return

    def shoot(self, game, color, erase_color, character, mouse_x, mouse_y):
        character.getDirection(mouse_x, mouse_y)
        proj = PiercingProjectile(character)

        return

    def getDirection(self, mouse_x, mouse_y):
        magnitude = 0
        direction = None
        if self.x_coordinate - mouse_x < 0:
            current_magnitude = abs(self.x_coordinate - mouse_x)
            if current_magnitude >= magnitude:
                self.direction = "EAST"
                direction =  "EAST"
                magnitude = current_magnitude

        if self.x_coordinate - mouse_x > 0:
            current_magnitude = abs(self.x_coordinate - mouse_x)
            if current_magnitude >= magnitude:
                self.direction = "WEST"
                direction =  "WEST"
                magnitude = current_magnitude

        if self.y_coordinate - mouse_y < 0:
            current_magnitude = abs(self.y_coordinate - mouse_y)
            if current_magnitude >= magnitude:
                self.direction = "SOUTH"
                direction =  "SOUTH"
                magnitude = current_magnitude

        if self.y_coordinate - mouse_y > 0:
            current_magnitude = abs(self.y_coordinate - mouse_y)
            if current_magnitude >= magnitude:
                self.direction = "NORTH"
                direction =  "NORTH"
                magnitude = current_magnitude

        if self.x_coordinate - mouse_x < -75 and self.y_coordinate - mouse_y < -75:
            self.direction = "SOUTHEAST"
            direction =  "SOUTHEAST"

        if self.x_coordinate - mouse_x > 75 and self.y_coordinate - mouse_y < -75:
            self.direction = "SOUTHWEST"
            direction =  "SOUTHWEST"

        if self.x_coordinate - mouse_x < -75 and self.y_coordinate - mouse_y > 75:
            self.direction = "NORTHEAST"
            direction =  "NORTHEAST"

        if self.x_coordinate - mouse_x > 75 and self.y_coordinate - mouse_y > 75:
            self.direction = "NORTHWEST"
            direction =  "NORTHWEST"

        return direction

    def getLegalMoves(self, config):
        if self.x_coordinate >= 0 and "LEFT" not in self.legal_moves:
            self.legal_moves.append("LEFT")
        if self.x_coordinate <= config.display_x and "RIGHT" not in self.legal_moves:
            self.legal_moves.append("RIGHT")
        if self.y_coordinate >= 0 and "UP" not in self.legal_moves:
            self.legal_moves.append("UP")
        if self.y_coordinate <= config.display_y and "DOWN" not in self.legal_moves:
            self.legal_moves.append("DOWN")

        if not self.x_coordinate >= 0 and "LEFT" in self.legal_moves:
            self.legal_moves.remove("LEFT")
        if not self.x_coordinate <= config.display_x and "RIGHT" in self.legal_moves:
            self.legal_moves.remove("RIGHT")
        if not self.y_coordinate >= 0 and "UP" in self.legal_moves:
            self.legal_moves.remove("UP")
        if not self.y_coordinate <= config.display_y and "DOWN" in self.legal_moves:
            self.legal_moves.remove("DOWN")

        return self.legal_moves
