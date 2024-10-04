import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FPS = 60

# Game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Space Battle")

# Player class
class Spaceship:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 2
        self.color = color
        self.fuel = 100
        self.ammo = 5
        self.health = 100
        self.width, self.height = 20, 20

    def rotate(self, direction):
        if direction == "left":
            self.angle += 5
        if direction == "right":
            self.angle -= 5

    def move(self):
        if self.fuel > 0:
            self.fuel -= 0.1  # Fuel consumption
            rad = math.radians(self.angle)
            self.x += math.cos(rad) * self.speed
            self.y -= math.sin(rad) * self.speed

    def shoot(self):
        if self.ammo > 0:
            rad = math.radians(self.angle)
            bullet_dx = math.cos(rad) * 5
            bullet_dy = -math.sin(rad) * 5
            return Bullet(self.x, self.y, bullet_dx, bullet_dy, self.color)
        return None

    def draw(self):
        rad = math.radians(self.angle)
        rotated_ship = pygame.transform.rotate(pygame.Surface((self.width, self.height)), self.angle)
        pygame.draw.polygon(window, self.color, [
            (self.x, self.y),
            (self.x + math.cos(rad + 2.356) * 10, self.y - math.sin(rad + 2.356) * 10),
            (self.x + math.cos(rad - 2.356) * 10, self.y - math.sin(rad - 2.356) * 10)
        ])

# Bullet class
class Bullet:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = 5

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

# Terrain class
class Terrain:
    def __init__(self):
        self.points = [(0, HEIGHT - 100)]
        for x in range(1, WIDTH, 10):
            self.points.append((x, HEIGHT - random.randint(50, 150)))
        self.points.append((WIDTH, HEIGHT - 100))

    def draw(self):
        pygame.draw.polygon(window, (0, 200, 0), self.points + [(WIDTH, HEIGHT), (0, HEIGHT)])

    def destruct(self, bullet):
        for i, (x, y) in enumerate(self.points):
            if abs(bullet.x - x) < 10 and bullet.y < y:
                self.points[i] = (x, bullet.y + 20)

# Main function
def main():
    clock = pygame.time.Clock()

    # Create players
    player1 = Spaceship(100, HEIGHT - 150, RED)
    player2 = Spaceship(700, HEIGHT - 150, BLUE)

    bullets = []
    terrain = Terrain()

    run = True
    while run:
        clock.tick(FPS)
        window.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # Player 1 controls (WASD)
        if keys[pygame.K_w]:
            player1.move()
        if keys[pygame.K_a]:
            player1.rotate("left")
        if keys[pygame.K_d]:
            player1.rotate("right")
        if keys[pygame.K_SPACE]:
            bullet = player1.shoot()
            if bullet:
                bullets.append(bullet)

        # Player 2 controls (Arrow keys)
        if keys[pygame.K_UP]:
            player2.move()
        if keys[pygame.K_LEFT]:
            player2.rotate("left")
        if keys[pygame.K_RIGHT]:
            player2.rotate("right")
        if keys[pygame.K_RETURN]:
            bullet = player2.shoot()
            if bullet:
                bullets.append(bullet)

        # Draw terrain and players
        terrain.draw()
        player1.draw()
        player2.draw()

        # Move and draw bullets
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw()
            if 0 < bullet.x < WIDTH and 0 < bullet.y < HEIGHT:
                terrain.destruct(bullet)  # Destroy terrain
            else:
                bullets.remove(bullet)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
