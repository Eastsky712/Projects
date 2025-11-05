import pygame

class Quokka:
    """This class manages the quokka"""

    def __init__(self, ai_game):
        """Initialize the quokka and its starting location"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('Alien_Invasion/images/quokka.bmp')
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()

        self.rect.midtop = self.screen_rect.midtop

    def blitme(self):
        self.screen.blit(self.image, self.rect)