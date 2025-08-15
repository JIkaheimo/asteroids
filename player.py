from circleshape import CircleShape
from constants import (
    PLAYER_ACCELERATION,
    PLAYER_FRICTION,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    PLAYER_SHOT_COOLDOWN,
    PLAYER_SHOT_SPEED,
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
        self.velocity = pygame.Vector2(0, 0)

    def hit(self):
        self.lives -= 1
        if self.lives > 0:
            self.position.x = SCREEN_WIDTH / 2
            self.position.y = SCREEN_HEIGHT / 2
            self.rotation = 0
            self.velocity = pygame.Vector2(0, 0)
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

    def accelerate(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def shoot(self) -> Shot | None:
        if self.timer > 0:
            return None

        self.timer = PLAYER_SHOT_COOLDOWN

        shot = Shot(
            self.position.x,
            self.position.y,
            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
            + self.velocity,
        )
        return shot

    def update(self, dt: float) -> None:
        self.timer -= dt

        # Limit velocity
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity.scale_to_length(PLAYER_MAX_SPEED)

        # Apply friction
        self.velocity *= PLAYER_FRICTION

        self.position += self.velocity * dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.accelerate(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_s]:
            self.accelerate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
