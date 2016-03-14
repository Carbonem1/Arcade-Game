#!/usr/bin/python

class Projectile:
    projectile_count = -1
    projectile_list = []
    piercing_projectile_list = []

    def __init__(self, projectile):
        if self.projectile_count == -1:
            self.projectile_count += 1
            return

        self.projectile_list.append(projectile)
        return

    def getProjectileCount(self):
        return self.projectile_count

    def getProjectileList(self):
        return self.projectile_list

    def getPiercingProjectileList(self):
        return self.piercing_projectile_list

    def getSlope(self, mouse_x, mouse_y):
        x_delta = self.x - mouse_x
        y_delta = self.y - mouse.y

        return x_delta/y_delta
