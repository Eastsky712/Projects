import sys

import pygame

from settings import Settings
from ship import Ship
#from quokka import Quokka

class AlienInvasion:
    """The main class to manage the game"""
    
    def __init__(self):
        """Start the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        # Full Screen Mode
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Windowed Mode
        """
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        """
        pygame.display.set_caption("Alien Invasion")
        
        
        self.ship = Ship(self)
        #self.quokka = Quokka(self)

        #Set background color
        self.bg_color = (230,230,230)
    
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            
            #Make the most recently drawn screen visible
            pygame.display.flip()
    
    def _check_events(self):
        """For checking keyboard and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            


    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()


    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        #Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        #self.quokka.blitme()
    
if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
