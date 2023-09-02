import pygame
import random

# Initialize pygame
pygame.init()

# Constants
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_NAME = pygame.font.match_font('arial')

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Slider class
class Slider:
    def __init__(self, x, y, color):
        self.color = color
        self.x = x
        self.y = y
        self.position = 0.5  # Default position

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 20, 200))
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y + int(200 * self.position)), 10)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x < event.pos[0] < self.x + 20 and self.y < event.pos[1] < self.y + 200:
                self.position = (event.pos[1] - self.y) / 200

# Main loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Subtractive Color Mixing Game")
    clock = pygame.time.Clock()

    red_slider = Slider(WIDTH // 4, HEIGHT // 2, RED)
    blue_slider = Slider(WIDTH // 4 + 100, HEIGHT // 2, BLUE)
    yellow_slider = Slider(WIDTH // 4 + 200, HEIGHT // 2, YELLOW)
    white_slider = Slider(WIDTH // 4 + 300, HEIGHT // 2, WHITE)

    sliders = [red_slider, blue_slider, yellow_slider, white_slider]

    target_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            for slider in sliders:
                slider.handle_event(event)

        mixed_color = (
            int(red_slider.position * 255),
            int(yellow_slider.position * 255),
            int(blue_slider.position * 255)
        )

        pygame.draw.rect(screen, target_color, (WIDTH // 2, HEIGHT // 4, 100, 100))
        pygame.draw.rect(screen, mixed_color, (WIDTH // 2 + 150, HEIGHT // 4, 100, 100))

        for slider in sliders:
            slider.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
