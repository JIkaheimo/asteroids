import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Background:
    def __init__(self, width, height, star_count):
        self.width = width
        self.height = height
        self.stars = []
        for _ in range(star_count):
            x = random.randint(-self.width // 2, self.width // 2)
            y = random.randint(-self.height // 2, self.height // 2)
            size = random.randint(1, 3)
            self.stars.append({"pos": pygame.Vector2(x, y), "size": size})

    def draw(self, screen, player_pos):
        screen.fill((0, 0, 0))  # Black background
        for star in self.stars:
            # Parallax effect
            star_screen_pos = (star["pos"] - player_pos * 0.1) % pygame.Vector2(
                self.width, self.height
            )

            # Center the star positions
            star_screen_pos.x -= self.width / 2
            star_screen_pos.y -= self.height / 2

            # Wrap around screen edges
            if star_screen_pos.x < -SCREEN_WIDTH / 2:
                star_screen_pos.x += SCREEN_WIDTH
            if star_screen_pos.x > SCREEN_WIDTH / 2:
                star_screen_pos.x -= SCREEN_WIDTH
            if star_screen_pos.y < -SCREEN_HEIGHT / 2:
                star_screen_pos.y += SCREEN_HEIGHT
            if star_screen_pos.y > SCREEN_HEIGHT / 2:
                star_screen_pos.y -= SCREEN_HEIGHT

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    int(star_screen_pos.x + SCREEN_WIDTH / 2),
                    int(star_screen_pos.y + SCREEN_HEIGHT / 2),
                ),
                star["size"],
            )
