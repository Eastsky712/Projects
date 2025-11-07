import pygame
from pygame.sprite import Sprite
from random import randint

class Star(Sprite):
    """A class to represent stars"""

    def __init__(self, ns_program):
        super().__init__()

        #Load alien image and set its rect attitude
        self.image = pygame.image.load('Practice_Projects/images/star.bmp')
        star_size = randint(5, 35)
        self.image = pygame.transform.scale(self.image, (star_size, star_size))
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)