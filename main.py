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