import sys
from time import sleep

import pygame
import random

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
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
        self.filename = 'Alien_Invasion/highscore.txt'

        # Windowed Mode
        """
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        """
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.shooter_aliens = pygame.sprite.Group()
        #self.quokka = Quokka(self)

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        #Set background color
        self.bg_color = (230,230,230)
    


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self.bullets.update()
                self.alien_bullets.update()
                self._check_alien_bullet_ship_collisions()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._check_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_k:
            self._skip_level()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_high_score(self):
        with open(self.filename, 'w') as f:
            current_high_score = str(self.stats.high_score)
            f.write(current_high_score)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb._prep_images()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.shooter_aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
    
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)
        #print(len(self.bullets))

        self._check_bullet_alien_collisions()

    def _fire_alien_bullet(self, alien):
        """Create a new enemy bullet and add it to the enemy bullet group"""
        if alien:
            new_alien_bullet = Bullet(self, alien, True)
            self.alien_bullets.add(new_alien_bullet)

    def _check_alien_bullet_ship_collisions(self):
        # Check for any alien bullets that have hit ship/
        #   If so, get rid of the alien bullet and a life of ship
        hit_bullet = pygame.sprite.spritecollideany(self.ship, self.alien_bullets)

        if hit_bullet:
            # Remove the bullet
            hit_bullet.kill()
            # Handle ship being hit
            self._ship_hit()

    def _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        
        collisions_alien = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        
        for bullet, hit_list in collisions_alien.items():
            for enemy in hit_list:
                overlap_rect = bullet.rect.clip(enemy.rect)

                hit_x, hit_y = overlap_rect.center

                added_score = self.settings.alien_points
                self.stats.score += added_score
                self.sb.prep_score()
                self.sb.add_popup(hit_x, hit_y, added_score, False)
                self.sb.add_explosion(hit_x, hit_y)
                self.sb.check_high_score()

        collisions_shooter_alien = pygame.sprite.groupcollide(
            self.bullets, self.shooter_aliens, True, True)
        
        for bullet, hit_list in collisions_shooter_alien.items():
            for enemy in hit_list:
                overlap_rect = bullet.rect.clip(enemy.rect)

                hit_x, hit_y = overlap_rect.center

                added_score = self.settings.shooter_alien_points
                self.stats.score += added_score
                self.sb.prep_score()
                self.sb.add_popup(hit_x, hit_y, added_score, True)
                self.sb.add_explosion(hit_x, hit_y)
                self.sb.check_high_score()

        
        if not self.aliens and not self.shooter_aliens:
            self._start_new_level()
    
    def _start_new_level(self):
        #Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level
        self.stats.level += 1
        self.sb.prep_level_up()
        self.sb.prep_level()

    def _ship_hit(self, type=1):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            #Decrement ships_left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            if type == 1:
                #Get rid of any remaining aliens and bullets.
                self.aliens.empty()
                self.shooter_aliens.empty()
                self.bullets.empty()
                self.alien_bullets.empty()

                #Create a new fleet and center the ship.
                self._create_fleet()
                self.ship.center_ship()
            elif type == 2:
                self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _create_fleet(self):
        """Create fleet of aliens"""
        # Create an alien and find the number of aliens in a row.
        #Spacing between each alien is equal to one alien width.
        alien = Alien(self, 1)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                #Create an alien and place it in the row.
                if row_number > number_rows // 2:
                    self._create_alien(alien_number, row_number, True)
                else:
                    self._create_alien(alien_number, row_number, False)
    
    def _create_alien(self, alien_number, row_number, is_not_shooter):
        """Create an alien and place it in the row."""

        if random.random() < self.settings.shooter_alien_chance and is_not_shooter == False:
            is_shooter_alien = True 
            alien = Alien(self, 2)
        else:
            is_shooter_alien = False
            alien = Alien(self, 1)
        
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        if is_shooter_alien == True:
            self.shooter_aliens.add(alien)
        else:
            self.aliens.add(alien)

    def _update_aliens(self):
        """
        Check if the fleet is at an edge
            then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()
        self.shooter_aliens.update()

        self._alien_fire_logic()

        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit(1)
        
        #Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _alien_fire_logic(self):
        """Randomly make aliens shoot bullets towards the player"""
        
        for alien in self.shooter_aliens.sprites():
            if random.random() < self.settings.alien_bullet_fire_chance:
                self._fire_alien_bullet(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in list(self.aliens.sprites()) + list(self.shooter_aliens.sprites()):
            if alien.check_edges():
                self._change_fleet_direction()
                break
        
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in list(self.aliens.sprites()) + list(self.shooter_aliens.sprites()):
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in list(self.aliens.sprites()) + list(self.shooter_aliens.sprites()):
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit(1)
                break


    def _skip_level(self):
        """Gets rid of all enemies in the current level"""
        self.aliens.empty()
        self.alien_bullets.empty()
        self.shooter_aliens.empty()
        self._update_bullets()
        self._update_screen()


    def _update_screen(self):
        #Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        #self.quokka.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.shooter_aliens.draw(self.screen)

        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()

        # Draw the score information, popups, and explosions of enemies
        self.sb.explosions.update()
        self.sb.popups.update()
        
        self.sb.show_score()
        #self.sb.explosions.draw(self.screen)
        self.sb.popups.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
    
if __name__ == '__main__':
    #Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
