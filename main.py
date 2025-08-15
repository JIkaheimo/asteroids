import pygame

from constants import *

from asteroid import Asteroid
from asteroidfield import AsteroidField
from player import Player
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()

    dt = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        asteroid_list = asteroids.sprites()
        for i, asteroid1 in enumerate(asteroid_list):
            # Asteroid on asteroid collision
            for asteroid2 in asteroid_list[i + 1 :]:
                if asteroid1.collides(asteroid2):
                    distance = asteroid1.position.distance_to(
                        asteroid2.position
                    )
                    overlap = (asteroid1.radius + asteroid2.radius) - distance
                    if overlap > 0:
                        direction = (
                            asteroid1.position - asteroid2.position
                        ).normalize()
                        asteroid1.position += direction * overlap / 2
                        asteroid2.position -= direction * overlap / 2

                    asteroid1.velocity, asteroid2.velocity = (
                        asteroid2.velocity,
                        asteroid1.velocity,
                    )
            # Shot on asteroid collision
            for shot in shots:
                if shot.collides(asteroid1):
                    shot.kill()
                    asteroid1.split()
            # Player on asteroid collision
            if player.collides(asteroid1):
                asteroid1.split()
                player.hit()
                if player.lives <= 0:
                    print("Game over!")
                    return

        screen.fill(pygame.Color("black"))

        for entity in drawable:
            entity.draw(screen)

        lives_text = font.render(
            f"Lives: {player.lives}", True, pygame.Color("white")
        )
        screen.blit(lives_text, (10, 10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000.0


if __name__ == "__main__":
    main()
