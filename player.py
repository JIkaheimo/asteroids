from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOT_COOLDOWN,
    PLAYER_SHOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
import pygame

from shot import Shot


class Player(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation: float = 0
        self.timer: float = 0
        self.lives = 3

    def hit(self):
        self.lives -= 1
        if self.lives > 0:
            self.position.x = SCREEN_WIDTH / 2
            self.position.y = SCREEN_HEIGHT / 2
            self.rotation = 0
        else:
            self.kill()

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = (
            pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        )
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, pygame.Color("white"), self.triangle(), 2)

    def rotate(self, dt: float) -> None:
        self.rotation += dt * PLAYER_TURN_SPEED

    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self) -> Shot | None:
        if self.timer > 0:
            return None

        self.timer = PLAYER_SHOT_COOLDOWN

        shot = Shot(
            self.position.x,
            self.position.y,
            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED,
        )
        return shot

    def update(self, dt: float) -> None:
        self.timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        # Remove shooting from here, it's handled in main.py
        # if keys[pygame.K_SPACE]:
        #     self.shoot()
