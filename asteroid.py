import pygame
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, pygame.Color("gray"), self.position, self.radius, 2)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt