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
        

# the turret

class Turret:
    def __init__(self, lane):
        self.lane = lane
        self.x = lane_x(lane)
        self.y = TURRET_Y

        self.cooldown = random.randint(0, 25)
        self.fire_delay = 28

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def can_fire(self):
        return self.cooldown <= 0

    def fire(self, target):
        self.cooldown = self.fire_delay
        return Bullet(self.x, self.y - 25, target)

    def draw(self, target=None):
        # Base
        base = pygame.Rect(
            int(self.x - 45),
            int(self.y - 20),
            90,
            45
        )

        pygame.draw.rect(
            screen,
            (25, 45, 60),
            base,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            CYAN,
            base,
            2,
            border_radius=10
        )

        # turret body
        pygame.draw.circle(
            screen,
            (40, 80, 105),
            (int(self.x), int(self.y - 5)),
            24
        )

        pygame.draw.circle(
            screen,
            CYAN,
            (int(self.x), int(self.y - 5)),
            20,
            3
        )

        # aim toward target
        if target is not None:
            dx = target.x - self.x
            dy = target.y - (self.y - 5)
            angle = math.atan2(dy, dx)

            end_x = self.x + math.cos(angle) * 38
            end_y = (self.y - 5) + math.sin(angle) * 38

            pygame.draw.line(
                screen,
                WHITE,
                (int(self.x), int(self.y - 5)),
                (int(end_x), int(end_y)),
                8
            )

        pygame.draw.circle(
            screen,
            BLUE,
            (int(self.x), int(self.y - 5)),
            8
        )
        
        
# design the bullet

class Bullet:
    def __init__(self, x, y, target):
        self.x = float(x)
        self.y = float(y)

        dx = target.x - self.x
        dy = target.y - self.y

        length = math.hypot(dx, dy)

        if length == 0:
            self.vx = 0
            self.vy = -BULLET_SPEED
        else:
            self.vx = dx / length * BULLET_SPEED
            self.vy = dy / length * BULLET_SPEED

        self.radius = 5

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(self.x), int(self.y)),
            self.radius + 4
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(self.x), int(self.y)),
            self.radius
        )

# target selection

def nearest_enemy(turret, enemies):
    """
    find the closest enemy in the turret's lane
    """

    lane_enemies = [
        enemy for enemy in enemies
        if enemy.lane == turret.lane
        and enemy.y < turret.y
    ]

    if not lane_enemies:
        return None

    return min(
        lane_enemies,
        key=lambda enemy: turret.y - enemy.y
    )

# fire helper
def fire(turret, target):
    return turret.fire(target)


# design and draw the game

def draw_background():
    screen.fill(BG)

    total_width = LANES * LANE_WIDTH + (LANES - 1) * LANE_GAP
    left = (WIDTH - total_width) // 2

    for lane in range(LANES):
        x = left + lane * (LANE_WIDTH + LANE_GAP)

        lane_rect = pygame.Rect(
            x,
            55,
            LANE_WIDTH,
            HEIGHT - 125
        )

        pygame.draw.rect(
            screen,
            (8, 20, 30),
            lane_rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            GRID,
            lane_rect,
            2,
            border_radius=8
        )

        # lane lines
        for y in range(75, HEIGHT - 100, 35):
            pygame.draw.line(
                screen,
                (25, 70, 95),
                (x + 10, y),
                (x + LANE_WIDTH - 10, y),
                2
            )

        # lane number
        label = SMALL_FONT.render(
            f"{lane + 1:02d}",
            True,
            (70, 90, 105)
        )

        screen.blit(
            label,
            label.get_rect(
                center=(x + LANE_WIDTH // 2, HEIGHT - 145)
            )
        )


def draw_hud(score, speed, lives):
    score_text = FONT.render(
        f"SCORE: {score}",
        True,
        WHITE
    )

    speed_text = FONT.render(
        f"SPEED: {speed:.1f}",
        True,
        CYAN
    )

    lives_text = FONT.render(
        f"LIVES: {lives}",
        True,
        WHITE
    )

    screen.blit(score_text, (25, 18))
    screen.blit(
        speed_text,
        (WIDTH // 2 - speed_text.get_width() // 2, 18)
    )
    screen.blit(
        lives_text,
        (WIDTH - lives_text.get_width() - 25, 18)
    )


def draw_game_over(score):
    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 185))
    screen.blit(overlay, (0, 0))

    title = BIG_FONT.render(
        "SYSTEM OVERRUN",
        True,
        RED
    )

    score_text = FONT.render(
        f"Final score: {score}",
        True,
        WHITE
    )

    restart = SMALL_FONT.render(
        "Press R to restart  •  ESC to quit",
        True,
        WHITE
    )

    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 70)
        )
    )

    screen.blit(
        score_text,
        score_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )
    )

    screen.blit(
        restart,
        restart.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 55)
        )
    )



# game reset

def reset_game():
    enemies = []
    bullets = []
    turrets = [Turret(lane) for lane in range(LANES)]

    score = 0
    speed = BASE_ENEMY_SPEED
    lives = 3

    spawn_timer = 0
    game_over = False

    return (
        enemies,
        bullets,
        turrets,
        score,
        speed,
        lives,
        spawn_timer,
        game_over
    )

# main game


(
    enemies,
    bullets,
    turrets,
    score,
    speed,
    lives,
    spawn_timer,
    game_over
) = reset_game()

running = True

while running:
    clock.tick(FPS)

    
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_r and game_over:
                (
                    enemies,
                    bullets,
                    turrets,
                    score,
                    speed,
                    lives,
                    spawn_timer,
                    game_over
                ) = reset_game()


    # update
    if not game_over:

        # spawn enemies
        spawn_timer += clock.get_time()

        current_spawn_time = max(
            350,
            SPAWN_TIME - score // 100 * 40
        )

        if spawn_timer >= current_spawn_time:
            spawn_timer = 0

            lane = random.randrange(LANES)

            enemy_speed = speed + random.uniform(-0.25, 0.45)

            enemies.append(
                Enemy(lane, enemy_speed)
            )


        # enemy movement

        for enemy in enemies:
            enemy.update()

        # if enemies reach the defense line, lose a life
        for enemy in enemies[:]:
            if enemy.y >= TURRET_Y - 35:
                enemies.remove(enemy)
                lives -= 1

                if lives <= 0:
                    game_over = True
                    break


        # turret targeting and firing
        for turret in turrets:
            turret.update()

            target = nearest_enemy(
                turret,
                enemies
            )

            if target and turret.can_fire():
                bullets.append(
                    fire(turret, target)
                )


        # bullet movement
        for bullet in bullets:
            bullet.update()


        # bullet / enemy collisions
        #
        # important:
        # iterate over copies with [:] so removing objects
        # during iteration does not cause skipped elements.
        for bullet in bullets[:]:
            for enemy in enemies[:]:

                if bullet.rect.colliderect(
                    enemy.rect
                ):
                    if enemy in enemies:
                        enemies.remove(enemy)

                    if bullet in bullets:
                        bullets.remove(bullet)

                    score += 100
                    break

        # remove bullets outside the screen.
        for bullet in bullets[:]:
            if (
                bullet.x < -30
                or bullet.x > WIDTH + 30
                or bullet.y < -30
                or bullet.y > HEIGHT + 30
            ):
                bullets.remove(bullet)


        # difficulty scaling
        # here we make it scale smoothly while preserving the behavior
        if score >= 300:
            speed = 6

        if score >= 800:
            speed = 7

        if score >= 1500:
            speed = 8


    # draw
    draw_background()

    # find targets for turret visuals.
    targets = [
        nearest_enemy(turret, enemies)
        for turret in turrets
    ]

    for enemy in enemies:
        enemy.draw()

    for bullet in bullets:
        bullet.draw()

    for i, turret in enumerate(turrets):
        turret.draw(targets[i])

    draw_hud(
        score,
        speed,
        lives
    )

    if game_over:
        draw_game_over(score)

    pygame.display.flip()

pygame.quit()