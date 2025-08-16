import pygame
import random

from constants import *

from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot
from explosion import Explosion
from background import Background
from powerup import PowerUp
from xporb import XPOrb


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)
        self.running = True
        self.game_state = "MENU"
        self.score = 0

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.xporbs = pygame.sprite.Group()

        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.updatable, self.drawable, self.asteroids)
        AsteroidField.containers = (self.updatable,)
        Shot.containers = (self.updatable, self.drawable, self.shots)
        Explosion.containers = (self.updatable, self.drawable, self.explosions)
        PowerUp.containers = (self.updatable, self.drawable, self.powerups)
        XPOrb.containers = (self.updatable, self.drawable, self.xporbs)

        self.player = None
        self.background = Background(SCREEN_WIDTH, SCREEN_HEIGHT, 200)

    def _reset_game(self):
        self.score = 0
        for group in [
            self.updatable,
            self.drawable,
            self.asteroids,
            self.shots,
            self.explosions,
            self.powerups,
            self.xporbs,
        ]:
            group.empty()

        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        AsteroidField()

    def run(self):
        dt = 0.0
        while self.running:
            if self.game_state == "MENU":
                self.main_menu_update()
            elif self.game_state == "PLAYING":
                self.playing_update(dt)
            elif self.game_state == "GAME_OVER":
                self.game_over_update()

            dt = self.clock.tick(60) / 1000.0

    def main_menu_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state = "PLAYING"
                    self._reset_game()
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        self.screen.fill(pygame.Color("black"))

        title_text = self.title_font.render(
            "Asteroids", True, pygame.Color("white")
        )
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        )
        self.screen.blit(title_text, title_rect)

        start_text = self.font.render(
            "Press ENTER to Start", True, pygame.Color("white")
        )
        start_rect = start_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        self.screen.blit(start_text, start_rect)

        exit_text = self.font.render(
            "Press ESC to Exit", True, pygame.Color("white")
        )
        exit_rect = exit_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
        )
        self.screen.blit(exit_text, exit_rect)

        pygame.display.flip()

    def playing_update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shots = self.player.shoot()
                if shots:
                    self.shots.add(shots)

        self._process_game_logic(dt)
        self._draw()
        if self.player.lives <= 0:
            self.game_state = "GAME_OVER"

    def game_over_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state = "MENU"

        self.screen.fill(pygame.Color("black"))

        title_text = self.title_font.render(
            "Game Over", True, pygame.Color("white")
        )
        title_rect = title_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        )
        self.screen.blit(title_text, title_rect)

        score_text = self.font.render(
            f"Score: {self.score}", True, pygame.Color("white")
        )
        score_rect = score_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        self.screen.blit(score_text, score_rect)

        restart_text = self.font.render(
            "Press ENTER to return to Menu", True, pygame.Color("white")
        )
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
        )
        self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def _process_game_logic(self, dt):
        self.updatable.update(dt)
        self._handle_collisions()

    def _handle_collisions(self):
        asteroid_list = self.asteroids.sprites()
        for i, asteroid1 in enumerate(asteroid_list):
            self._handle_asteroid_on_asteroid_collision(
                asteroid1, asteroid_list[i + 1 :]
            )
            self._handle_shot_on_asteroid_collision(asteroid1)
            if self._handle_player_on_asteroid_collision(asteroid1):
                break
        self._handle_player_on_powerup_collision()
        self._handle_player_on_xporb_collision()

    def _handle_asteroid_on_asteroid_collision(
        self, asteroid1, other_asteroids
    ):
        for asteroid2 in other_asteroids:
            if asteroid1.collides(asteroid2):
                distance = asteroid1.position.distance_to(asteroid2.position)
                overlap = (asteroid1.radius + asteroid2.radius) - distance
                if overlap > 0:
                    direction = (
                        asteroid1.position - asteroid2.position
                    ).normalize()
                    asteroid1.position += direction * overlap / 2
                    asteroid2.position -= direction * overlap / 2

                asteroid1.velocity, asteroid2.velocity = (
                    asteroid2.velocity,
                    asteroid1.velocity,
                )

    def _handle_shot_on_asteroid_collision(self, asteroid):
        for shot in self.shots:
            if shot.collides(asteroid):
                shot.kill()
                asteroid.split()
                self.score += 10
                Explosion(asteroid.position.x, asteroid.position.y)
                if random.random() < POWERUP_CHANCE:
                    PowerUp(asteroid.position.x, asteroid.position.y)
                if random.random() < XP_ORB_CHANCE:
                    XPOrb(asteroid.position.x, asteroid.position.y, 25)

    def _handle_player_on_asteroid_collision(self, asteroid):
        if self.player.collides(asteroid):
            asteroid.split()
            self.player.hit()
            if self.player.lives <= 0:
                return True
        return False

    def _handle_player_on_powerup_collision(self):
        for powerup in self.powerups:
            if self.player.collides(powerup):
                self.player.set_weapon(powerup.type)
                powerup.kill()

    def _handle_player_on_xporb_collision(self):
        for orb in self.xporbs:
            if self.player.collides(orb):
                self.player.add_xp(orb.value)
                orb.kill()

    def _draw(self):
        self.background.draw(self.screen, self.player.position)

        for entity in self.drawable:
            entity.draw(self.screen)

        self._draw_hud()

        pygame.display.flip()

    def _draw_hud(self):
        # Score and Lives
        score_text = self.font.render(
            f"Score: {self.score}", True, pygame.Color("white")
        )
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render(
            f"Lives: {self.player.lives}", True, pygame.Color("white")
        )
        self.screen.blit(lives_text, (10, 40))

        # Level and XP Bar
        level_text = self.font.render(
            f"Level: {self.player.level}", True, pygame.Color("white")
        )
        level_text_rect = level_text.get_rect(centerx=SCREEN_WIDTH / 2, y=10)
        self.screen.blit(level_text, level_text_rect)

        bar_width = SCREEN_WIDTH / 2
        bar_height = 15
        x = SCREEN_WIDTH / 2 - bar_width / 2
        y = 40
        fill = (self.player.xp / self.player.xp_to_next_level) * bar_width
        border_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(self.screen, pygame.Color("white"), border_rect, 2)
        pygame.draw.rect(self.screen, pygame.Color("magenta"), fill_rect)

        # Power-up and Shield Bars
        if self.player.powerup_timer > 0:
            self._draw_powerup_bar()
        if self.player.shield_timer > 0:
            self._draw_shield_bar()

    def _draw_powerup_bar(self):
        bar_width = 200
        bar_height = 20
        x = SCREEN_WIDTH / 2 - bar_width / 2
        y = SCREEN_HEIGHT - bar_height - 10
        fill = (self.player.powerup_timer / POWERUP_DURATION) * bar_width
        border_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(self.screen, pygame.Color("white"), border_rect, 2)
        pygame.draw.rect(self.screen, pygame.Color("cyan"), fill_rect)

    def _draw_shield_bar(self):
        bar_width = 200
        bar_height = 20
        x = SCREEN_WIDTH / 2 - bar_width / 2
        y = SCREEN_HEIGHT - bar_height - 40
        fill = (self.player.shield_timer / SHIELD_DURATION) * bar_width
        border_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(self.screen, pygame.Color("white"), border_rect, 2)
        pygame.draw.rect(self.screen, pygame.Color("white"), fill_rect)


def main():
    game = Game()
    game.run()



if __name__ == "__main__":
    main()
