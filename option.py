import pygame

class Option:

    hovered = False

    def __init__(self, game, color, menu_font, text, pos):
        self.text = text
        self.pos = pos
        self.menu_font = menu_font
        self.color = color
        self.set_rect()
        self.game = game
        self.draw()

    def draw(self):
        self.set_rend()
        self.game.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return self.color
        else:
            return (100, 100, 100)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
