import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.radius = 10
        self.max_radius = 40
        self.speed = 100  # pixels per second
        self.color = pygame.Color("white")
        self.timer = (self.max_radius - self.radius) / self.speed

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()
        self.radius += self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, self.position, int(self.radius), 2
        )
