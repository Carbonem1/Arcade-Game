#!/usr/bin/python

class Enemy:
    enemy_count = -1
    blue_enemy_count = -1
    green_enemy_count = -1
    red_enemy_count = -1
    enemy_list = []
    blue_enemy_list = []
    green_enemy_list = []
    red_enemy_list = []

    def __init__(self):
        if self.enemy_count == -1:
            self.enemy_count += 1
            return
        return

    def getEnemyCount(self):
        return self.enemy_count

    def getEnemyList(self):
        return self.enemy_list

    def getBlueEnemyList(self):
        return self.blue_enemy_list

    def getGreenEnemyList(self):
        return self.green_enemy_list

    def getRedEnemyList(self):
        return self.red_enemy_list

    def clearEnemyList(self):
        del self.enemy_list[:]
