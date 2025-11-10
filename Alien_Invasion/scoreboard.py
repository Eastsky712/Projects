import pygame.font
import time
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self,ai_game):
        """Initialize score keeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.filename = ai_game.filename

        #Fonts settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.showing_level_up = False
        self.level_up_start_time = 0

        #Prepare the initial score image.
        self._prep_images()

    def _prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_level_up(self):
        """Flash a level up text whenever you level up"""
        flash_text = f"LEVEL {self.stats.level}!" 
        self.flash_image = self.font.render(flash_text, True, (217, 33, 33))
        self.flash_rect = self.flash_image.get_rect(center=self.screen_rect.center)

        self.showing_level_up = True
        self.level_up_start_time = pygame.time.get_ticks()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        with open(self.filename, encoding='utf-8') as f:
            current_high_score = int(f.readline())
            if high_score < current_high_score:
                high_score = current_high_score
        
        high_score_str = "Highscore: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, 
                    self.text_color, self.settings.bg_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect= self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = f"Level: {(self.stats.level)}"
        self.level_image = self.font.render(level_str, True,
                    self.text_color, self.settings. bg_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)


    
    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

        # Draw a visual cue of transitioning to next level
        if self.showing_level_up:
            current_time = pygame.time.get_ticks()
            if current_time - self.level_up_start_time < 1000:
                self.screen.blit(self.flash_image, self.flash_rect)
            else:
                self.showing_level_up = False
    def add_popup(self, x, y, points):
        popup = ScorePopup(x, y, points, self.font)
        self.popups.add(popup)
class ScorePopup(pygame.sprite.Sprite):
    def __init__(self, x, y, points, font):
        super().__init__()
        self.image = font.render(f"+{points}", True, (255, 215, 0))
        self.rect = self.image.get_rect(center=(x,y))
        self.timer = 60

    def update(self):
        self.rect.y -= 1
        self.timer -= 1
        if self.timer <= 0:
            self.kill()