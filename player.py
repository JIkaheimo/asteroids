from circleshape import CircleShape
from constants import (
    PLAYER_ACCELERATION,
    PLAYER_FRICTION,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    PLAYER_SHOT_COOLDOWN,
    PLAYER_SHOT_SPEED,
    PLAYER_TURN_SPEED,
    POWERUP_DURATION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHIELD_DURATION,
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
        self.weapon = "default"
        self.powerup_timer = 0.0
        self.shielded = False
        self.shield_timer = 0.0
        self.level: int = 1
        self.xp: int = 0
        self.xp_to_next_level: int = 100

    def hit(self):
        if self.shielded:
            return
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
        pygame.draw.polygon(screen, pygame.Color("yellow"), self.triangle(), 2)
        if self.shielded:
            pygame.draw.circle(
                screen,
                pygame.Color("white"),
                self.position,
                self.radius + 5,
                2,
            )

    def rotate(self, dt: float) -> None:
        self.rotation += dt * PLAYER_TURN_SPEED

    def accelerate(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt

    def shoot(self) -> list[Shot]:
        if self.timer > 0:
            return []

        self.timer = PLAYER_SHOT_COOLDOWN
        shots = []
        if self.weapon == "default":
            shots.append(self._shoot_default())
        elif self.weapon == "shotgun":
            shots.extend(self._shoot_shotgun())
        elif self.weapon == "triple":
            shots.extend(self._shoot_triple())

        return shots

    def _shoot_default(self):
        return Shot(
            self.position.x,
            self.position.y,
            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED
            + self.velocity,
        )

    def _shoot_shotgun(self):
        shots = []
        for i in range(-2, 3):
            direction = pygame.Vector2(0, 1).rotate(self.rotation + i * 10)
            shot = Shot(
                self.position.x,
                self.position.y,
                direction * PLAYER_SHOT_SPEED + self.velocity,
            )
            shots.append(shot)
        return shots

    def _shoot_triple(self):
        shots = []
        for i in range(-1, 2):
            direction = pygame.Vector2(0, 1).rotate(self.rotation + i * 20)
            shot = Shot(
                self.position.x,
                self.position.y,
                direction * PLAYER_SHOT_SPEED + self.velocity,
            )
            shots.append(shot)
        return shots

    def set_weapon(self, weapon_type):
        if weapon_type == "shield":
            self.shielded = True
            self.shield_timer = SHIELD_DURATION
        else:
            self.weapon = weapon_type
            self.powerup_timer = POWERUP_DURATION

    def add_xp(self, amount: int):
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)

    def update(self, dt: float) -> None:
        self.timer -= dt
        self.powerup_timer -= dt
        if self.powerup_timer <= 0:
            self.weapon = "default"

        self.shield_timer -= dt
        if self.shield_timer <= 0:
            self.shielded = False

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
