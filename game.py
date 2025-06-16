import pygame
import sys
import random
import os

pygame.init()

# Screen setup
screen_width, screen_height = 1000, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Trash Cleanup Game")

# Path to images
IMAGE_DIR = os.path.join("static", "images")

# Image loader with path handling and error checking
def load_image(filename, size=None):
    path = os.path.join(IMAGE_DIR, filename)
    if not os.path.exists(path):
        print(f"❌ ERROR: File '{path}' not found.")
        pygame.quit()
        sys.exit()
    img = pygame.image.load(path)
    if size:
        img = pygame.transform.scale(img, size)
    return img

# Load assets from 'static/images/'
background = load_image("city.jpg", (screen_width, screen_height))
trash_img = load_image("bnpeel.png", (64, 64))
cat_img = load_image("cat.png", (100, 100))
heart_img = load_image("hrt.png", (32, 32))
cursor_img = load_image("trashcan.png", (32, 32))
pygame.mouse.set_visible(False)

# Object positions
trash = pygame.Rect(200, 400, 64, 64)
dragging = False
cat = pygame.Rect(700, 350, 100, 100)
hearts = []

clock = pygame.time.Clock()

# Flying heart logic
class Heart:
    def __init__(self, x, y):
        self.x = x + random.randint(-10, 10)
        self.y = y
        self.alpha = 255
        self.speed_y = random.uniform(-2.5, -1.5)

    def update(self):
        self.y += self.speed_y
        self.alpha -= 2
        return self.alpha > 0

    def draw(self, surf):
        temp_img = heart_img.copy()
        temp_img.set_alpha(self.alpha)
        surf.blit(temp_img, (self.x, self.y))

# Game loop
while True:
    screen.blit(background, (0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if trash.collidepoint((mouse_x, mouse_y)):
                dragging = True

            if cat.collidepoint((mouse_x, mouse_y)):
                for _ in range(5):
                    hearts.append(Heart(cat.x + 40, cat.y))

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    if dragging:
        trash.center = (mouse_x, mouse_y)

    # Draw items
    screen.blit(trash_img, trash.topleft)
    screen.blit(cat_img, cat.topleft)

    # Draw hearts
    for heart in hearts[:]:
        if not heart.update():
            hearts.remove(heart)
        else:
            heart.draw(screen)

    # Custom cursor
    screen.blit(cursor_img, (mouse_x, mouse_y))

    pygame.display.flip()
    clock.tick(60)
