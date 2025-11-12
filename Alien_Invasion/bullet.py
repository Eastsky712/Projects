import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game, shooter=None, is_alien_bullet=False):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.is_alien_bullet = is_alien_bullet

        self.color = (
            self.settings.alien_bullet_color
            if is_alien_bullet
            else self.settings.bullet_color
        )

        #Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        if is_alien_bullet and shooter:
            self.rect.midbottom = shooter.rect.midbottom
        else:
            self.rect.midtop = ai_game.ship.rect.midtop

        #Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    
    def update(self):
        """Move the bullet up the screen."""
        if self.is_alien_bullet:
            # Update the decimal position of enemy bullet
            self.y += self.settings.alien_bullet_speed
        else:
            #Update the decimal position of the bullet.
            self.y -= self.settings.bullet_speed
            
        #Update the rect position.
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
       