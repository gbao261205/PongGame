import pygame
import random
import math

# Khởi tạo pygame
pygame.init()

# Thiết lập màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pháo Hoa Tự Động")

# Màu sắc
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

# Lớp Particle (Hạt)
class Particle:
    def __init__(self, x, y, color, angle, speed, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.angle = angle
        self.speed = speed
        self.lifetime = lifetime
        self.radius = 5

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.radius -= 0.1
        self.lifetime -= 1

    def draw(self, surface):
        if self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

    def is_alive(self):
        return self.lifetime > 0 and self.radius > 0

# Lớp Rocket (Tên lửa)
class Rocket:
    def __init__(self, x, y, color, target_y):
        self.x = x
        self.y = y
        self.color = color
        self.target_y = target_y
        self.speed = 5
        self.exploded = False

    def update(self):
        if self.y > self.target_y:
            self.y -= self.speed
        else:
            self.exploded = True

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.rect(surface, self.color, (int(self.x) - 2, int(self.y) - 10, 4, 10))

# Hàm tạo pháo hoa
def create_firework(x, y, num_particles=100):
    particles = []
    for _ in range(num_particles):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        lifetime = random.randint(40, 80)
        color = random.choice(COLORS)
        particles.append(Particle(x, y, color, angle, speed, lifetime))
    return particles

def banphaohoa():
    # Danh sách tên lửa và pháo hoa
    rockets = []
    fireworks = []

    # Vòng lặp chính
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Tạo tên lửa tự động
        if random.randint(1, 40) == 1:  # Tạo tên lửa mới mỗi khung hình với xác suất
            x = random.randint(50, WIDTH - 50)
            color = random.choice(COLORS)
            target_y = random.randint(150, HEIGHT // 2)
            rockets.append(Rocket(x, HEIGHT, color, target_y))

        # Vẽ nền đen
        screen.fill(BLACK)

        # Cập nhật và vẽ tên lửa
        for rocket in rockets[:]:
            rocket.update()
            rocket.draw(screen)
            if rocket.exploded:
                fireworks.append(create_firework(rocket.x, rocket.y))
                rockets.remove(rocket)

        # Cập nhật và vẽ pháo hoa
        for firework in fireworks:
            for particle in firework[:]:
                particle.update()
                particle.draw(screen)
                if not particle.is_alive():
                    firework.remove(particle)

        # Loại bỏ pháo hoa đã hoàn toàn biến mất
        fireworks = [fw for fw in fireworks if len(fw) > 0]

        # Cập nhật màn hình
        pygame.display.flip()
        clock.tick(60)

    # Thoát
    pygame.quit()