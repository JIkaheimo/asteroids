import pygame
import random
import math
from circleshape import CircleShape
from constants import POWERUP_LIFETIME


class PowerUp(CircleShape):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 10)
        self.type = random.choice(["shotgun", "triple", "shield"])
        self.lifetime = POWERUP_LIFETIME
        if self.type == "shotgun":
            self.color = pygame.Color("orange")
        elif self.type == "triple":
            self.color = pygame.Color("cyan")
        else:
            self.color = pygame.Color("white")

    def update(self, dt: float):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        pygame.draw.circle(
            screen, pygame.Color("white"), self.position, self.radius, 2
        )
        if self.lifetime > 0:
            angle = (self.lifetime / POWERUP_LIFETIME) * 2 * math.pi
            rect = pygame.Rect(
                self.position.x - self.radius - 3,
                self.position.y - self.radius - 3,
                (self.radius + 3) * 2,
                (self.radius + 3) * 2,
            )
            pygame.draw.arc(screen, pygame.Color("gray"), rect, 0, angle, 3)
