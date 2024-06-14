import datetime
import os
import random
import pygame

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Game")

ico = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(ico)
MENU_BACKGROUND = pygame.image.load("assets/dino.png")
MENU_BACKGROUND = pygame.transform.scale(MENU_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))
DEAD = pygame.image.load(os.path.join("assets/Dino", "DinoDead.png"))

game_speed = 20
x_pos_bg = 0
y_pos_bg = 380
points = 0
obstacles = []

FONT_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color = (0, 0, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=20)
        font = pygame.font.Font("freesansbold.ttf", 20)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, user_input):
        if self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or user_input[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 260]

    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, BACKGROUND_COLOR
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    death_count = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pass

        user_input = pygame.key.get_pressed()

        SCREEN.fill(BACKGROUND_COLOR)
        player.draw(SCREEN)
        player.update(user_input)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                save_score(points)
                death_count += 1
                menu(death_count)

        game_background()

        cloud.draw(SCREEN)
        cloud.update()

        display_score()

        clock.tick(30)
        pygame.display.update()

def game_background():
    global x_pos_bg, y_pos_bg
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg = 0
    x_pos_bg -= game_speed

def display_score():
    global points, game_speed
    points += 1
    if points % 100 == 0:
        game_speed += 1
    font = pygame.font.Font("freesansbold.ttf", 20)
    highscore = get_high_score()
    if points > highscore:
        highscore = points

    text = font.render("High Score: " + str(highscore) + "  Score: " + str(points), True, FONT_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (900, 40)
    SCREEN.blit(text, text_rect)

def menu(death_count):
    global points, FONT_COLOR, BACKGROUND_COLOR

    def start_game():
        main()

    def open_settings():
        settings_menu()

    def quit_game():
        pygame.quit()
        exit()

    run = True
    while run:
        current_time = datetime.datetime.now().hour
        if 7 < current_time < 19:
            FONT_COLOR = (0, 0, 0)
        else:
            FONT_COLOR = (255, 255, 255)
        SCREEN.blit(MENU_BACKGROUND, (0, 0))
        font = pygame.font.Font("freesansbold.ttf", 30)

        highscore = get_high_score()

        hs_text = font.render(f"High Score: {highscore}", True, FONT_COLOR)
        hs_text_rect = hs_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        SCREEN.blit(hs_text, hs_text_rect)

        score_text = font.render(f"Score: {points}", True, FONT_COLOR)
        score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        SCREEN.blit(score_text, score_text_rect)

        restart_button = Button("Restart", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 60, 100, 40, start_game)
        settings_button = Button("Settings", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 60, 120, 40, open_settings)
        quit_button = Button("Quit", SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 60, 100, 40, quit_game)

        restart_button.draw(SCREEN)
        settings_button.draw(SCREEN)
        quit_button.draw(SCREEN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                restart_button.is_clicked(event)
                settings_button.is_clicked(event)
                quit_button.is_clicked(event)


def settings_menu():
    global BACKGROUND_COLOR

    def change_background_color(color):
        global BACKGROUND_COLOR
        BACKGROUND_COLOR = color
        menu(0)

    run = True
    while run:
        SCREEN.fill((200, 200, 200))

        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Select Background Color", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        SCREEN.blit(text, text_rect)

        white_button = Button("White", SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 10, 100, 50, lambda: change_background_color((255, 255, 255)))
        black_button = Button("Black", SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 10, 100, 50, lambda: change_background_color((0, 0, 0)))
        gray_button = Button("Gray", SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 10, 100, 50, lambda: change_background_color((128, 128, 128)))
        
        white_button.draw(SCREEN)
        black_button.draw(SCREEN)
        gray_button.draw(SCREEN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                white_button.is_clicked(event)
                black_button.is_clicked(event)
                gray_button.is_clicked(event)

def save_score(score):
    with open("score.txt", "a") as f:
        f.write(f"{score}\n")

def get_high_score():
    try:
        with open("score.txt", "r") as f:
            scores = [int(line) for line in f]
            return max(scores)
    except ValueError:
        return 0

menu(death_count=0)
