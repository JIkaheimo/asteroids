import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
import random


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x, y, radius)

    def split(self) -> None:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2

        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen, pygame.Color("gray"), self.position, self.radius, 2
        )

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
