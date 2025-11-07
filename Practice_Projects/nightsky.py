import sys

import pygame
from random import randint

from star import Star

class NightSky:
    """The main class to manage the creation of the night sky"""

    def __init__(self):
        pygame.init()
        
        
        self.screen = pygame.display.set_mode((1200, 800))

        pygame.display.set_caption("Night Sky simulation")

        self.stars = pygame.sprite.Group()

        self._create_night_sky()

        self.bg_color = (0,0,0)

    def run_program(self):
        while True:
            self._update_events()

            self._update_screen()
            
            pygame.display.flip()
    
    def _update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
    
    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_n:
            self._create_night_sky()

    def _create_night_sky(self):
        for star in range(randint(30,80)):
            self._create_star()
    
    def _create_star(self):
        star = Star(self)
        star.x = randint(0, self.screen.width)
        star.rect.x = star.x
        star.y = randint(0, self.screen.height)
        star.rect.y = star.y
        self.stars.add(star)



    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.stars.draw(self.screen)

if __name__ == '__main__':
    ns = NightSky()
    ns.run_program()