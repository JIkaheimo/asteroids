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

    def collides(self, other: "CircleShape") -> bool:
        return (
            self.position.distance_to(other.position)
            < self.radius + other.radius
        )

    def draw(self, screen: pygame.Surface) -> None:
        raise NotImplementedError("Subclasses must implement draw method")

    def update(self, dt: float) -> None:
        raise NotImplementedError("Subclasses must implement update method")
