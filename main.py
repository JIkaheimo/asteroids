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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.score = 0

        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.updatable, self.drawable, self.asteroids)
        AsteroidField.containers = (self.updatable,)
        Shot.containers = (self.updatable, self.drawable, self.shots)
        Explosion.containers = (self.updatable, self.drawable, self.explosions)
        PowerUp.containers = (self.updatable, self.drawable, self.powerups)

        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        AsteroidField()
        self.background = Background(SCREEN_WIDTH, SCREEN_HEIGHT, 200)

    def run(self):
        dt = 0.0
        while self.running:
            self._handle_input()
            self._process_game_logic(dt)
            self._draw()
            dt = self.clock.tick(60) / 1000.0

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shot = self.player.shoot()
                if shot:
                    self.shots.add(shot)

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

    def _handle_player_on_asteroid_collision(self, asteroid):
        if self.player.collides(asteroid):
            asteroid.split()
            self.player.hit()
            if self.player.lives <= 0:
                print("Game over!")
                self.running = False
                return True
        return False

    def _handle_player_on_powerup_collision(self):
        for powerup in self.powerups:
            if self.player.collides(powerup):
                self.player.set_weapon(powerup.type)
                powerup.kill()

    def _draw(self):
        self.background.draw(self.screen, self.player.position)

        for entity in self.drawable:
            entity.draw(self.screen)

        lives_text = self.font.render(
            f"Lives: {self.player.lives}", True, pygame.Color("white")
        )
        self.screen.blit(lives_text, (10, 10))

        score_text = self.font.render(
            f"Score: {self.score}", True, pygame.Color("white")
        )
        self.screen.blit(score_text, (10, 40))

        if self.player.powerup_timer > 0:
            self._draw_powerup_bar()
        if self.player.shield_timer > 0:
            self._draw_shield_bar()

        pygame.display.flip()

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
