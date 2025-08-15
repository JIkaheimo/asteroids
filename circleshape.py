import pygame

class CircleShape(pygame.sprite.Sprite):
    containers = None

    def __init__(self, x: float, y: float, radius: float):
        if self.containers:
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.radius: float = radius

    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError("Subclasses must implement draw method")

    def update(self, dt: float) -> None:
        raise NotImplementedError("Subclasses must implement update method")