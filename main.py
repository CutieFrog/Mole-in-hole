import pygame
import random

# Ініціалізація Pygame
pygame.init()
pygame.mixer.init()

# Налаштування розміру вікна
SCREEN_WIDTH = 760
SCREEN_HEIGHT = 760
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Whack a Mole")

# Завантаження зображень
background = pygame.image.load('img/bg.png')
mole_image = pygame.image.load('img/mole.png')
hole_image = pygame.image.load('img/mole_in_hole.png')
hammer_image = pygame.image.load('img/hummer.png')

pygame.mixer.music.load('music/bg_music.mp3')
pygame.mixer.music.set_volume(0.3)  # Гучність музики (від 0.0 до 1.0)
pygame.mixer.music.play(-1)  # Відтворення фонової музики безперервно (-1 означає повторення)

hit_sound = pygame.mixer.Sound('music/udar.mp3')  # Шлях до файлу зі звуковим ефектом
hit_sound.set_volume(0.7)  # Гучність звуку

promah_sound = pygame.mixer.Sound("music/promah.mp3")
promah_sound.set_volume(1)

# Зміна розміру зображень, якщо потрібно
mole_image = pygame.transform.scale(mole_image, (120, 120))
hole_image = pygame.transform.scale(hole_image, (120, 120))
hammer_image = pygame.transform.scale(hammer_image, (50, 50))

# Клас для крота
class Mole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mole_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, SCREEN_WIDTH - 150)
        self.rect.y = random.randint(350, SCREEN_HEIGHT - 150)
        self.is_visible = False
        self.visible_time = 0

    def appear(self):
        self.is_visible = True
        self.visible_time = pygame.time.get_ticks()

    def hide(self):
        self.is_visible = False

    def update(self):
        if self.is_visible and pygame.time.get_ticks() - self.visible_time > 1000:
            self.hide()

# Клас для молотка
class Hammer:
    def __init__(self):
        self.image = hammer_image
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

# Створення об'єктів
moles = [Mole() for _ in range(5)]
hammer = Hammer()

start_time = pygame.time.get_ticks()
game_duration = 20000  # Тривалість гри 20 секунд (20000 мілісекунд)

# Головний цикл гри
running = True
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

while running:
    screen.blit(background, (0, 0))

    # Рахуємо, скільки часу минуло
    elapsed_time = pygame.time.get_ticks() - start_time
    time_left = max(0, (game_duration - elapsed_time) // 1000)  # Секунди, що залишились

    # Перевіряємо, чи завершився час
    if elapsed_time >= game_duration:
        running = False  # Зупиняємо гру, коли минуло 20 секунд
    
    # Перевірка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hit = False
            for mole in moles:
                if mole.is_visible and mole.rect.collidepoint(event.pos):
                    score += 1
                    mole.hide()  # Приховати крота після влучання
                    hit_sound.play()
                    hit = True
                    break 
            
            if not hit:
                score -= 1
                promah_sound.play()

    # Рандомна поява крота
    for mole in moles:
        if not mole.is_visible and random.random() < 0.01:
            mole.appear()

    # Оновлення об'єктів
    mole.update()
    hammer.update()

    # Оновлення кротів
    for mole in moles:
        mole.update()
        # Спочатку малюємо діру
        screen.blit(hole_image, mole.rect.topleft)
        # Якщо кріт видимий, малюємо його поверх діри
        if mole.is_visible:
            screen.blit(mole_image, mole.rect.topleft)


    # Відображення молотка
    hammer.draw(screen)

    # Відображення рахунку
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    timer_text = font.render(f"Time left: {time_left}s", True, (255, 0, 0))
    screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))

    # Оновлення екрану
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
