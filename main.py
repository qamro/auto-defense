import pygame
import random
import math

pygame.init()

# auto defense settings

WIDTH = 900
HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Qamro's Auto Defense")
clock = pygame.time.Clock()

# colors

BG = (5, 10, 18)
GRID = (20, 55, 75)
WHITE = (235, 245, 255)
CYAN = (70, 230, 255)
BLUE = (60, 130, 255)
RED = (255, 70, 75)
ORANGE = (255, 170, 60)
GREEN = (70, 230, 140)
YELLOW = (255, 220, 80)
GRAY = (90, 105, 125)


# fonts

FONT = pygame.font.SysFont("arial", 28, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 18)
BIG_FONT = pygame.font.SysFont("arial", 52, bold=True)


# game settings

LANES = 3
LANE_WIDTH = 190
LANE_GAP = 30

TURRET_Y = HEIGHT - 85
ENEMY_SIZE = 42
BULLET_SPEED = 10

BASE_ENEMY_SPEED = 2.0
SPAWN_TIME = 850  # milliseconds


# helper functions that will help us

def lane_x(lane):
    total_width = LANES * LANE_WIDTH + (LANES - 1) * LANE_GAP
    left = (WIDTH - total_width) // 2
    return left + lane * (LANE_WIDTH + LANE_GAP) + LANE_WIDTH // 2


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


# build the enemy

class Enemy:
    def __init__(self, lane, speed):
        self.lane = lane
        self.x = lane_x(lane)
        self.y = -ENEMY_SIZE
        self.speed = speed
        self.radius = ENEMY_SIZE // 2

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            ENEMY_SIZE,
            ENEMY_SIZE
        )

    def update(self):
        self.y += self.speed

    def draw(self):
        # glow
        pygame.draw.circle(
            screen,
            (80, 25, 30),
            (int(self.x), int(self.y)),
            self.radius + 10
        )

        pygame.draw.circle(
            screen,
            RED,
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            ORANGE,
            (int(self.x), int(self.y)),
            self.radius - 9,
            3
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            5
        )
        

