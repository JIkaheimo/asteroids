import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
import random
import math


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x, y, radius)
        self.shape = self._generate_shape()
        self.rotation = 0
        self.rotation_speed = random.uniform(-50, 50)

    def _generate_shape(self):
        points = []
        num_vertices = 12
        for i in range(num_vertices):
            angle = (i / num_vertices) * 2 * math.pi
            dist = self.radius + random.uniform(-self.radius / 3, self.radius / 3)
            x = dist * math.cos(angle)
            y = dist * math.sin(angle)
            points.append(pygame.Vector2(x, y))
        return points

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
        rotated_shape = [
            point.rotate(self.rotation) + self.position for point in self.shape
        ]
        pygame.draw.polygon(screen, pygame.Color("brown"), rotated_shape, 2)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
