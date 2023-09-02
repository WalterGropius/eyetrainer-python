import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constants
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_NAME = pygame.font.match_font('arial')

# Slider class
class Slider:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = 0.5  # Default position

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 20, 200))
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + int(200 * self.position)), 10)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x < event.pos[0] < self.x + 20 and self.y < event.pos[1] < self.y + 200:
                self.position = (event.pos[1] - self.y) / 200

# Main loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Angle Discerning Game")
    clock = pygame.time.Clock()

    slider = Slider(WIDTH // 4, HEIGHT // 2)

    target_angle = random.randint(0, 180)
    feedback = ""

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    guessed_angle = int(slider.position * 180)
                    difference = abs(target_angle - guessed_angle)
                    if difference <= 5:
                        feedback = "Great! You're close!"
                    else:
                        feedback = f"Off by {difference} degrees!"
            slider.handle_event(event)

        pygame.draw.line(screen, WHITE, (WIDTH // 2, HEIGHT // 2), (WIDTH // 2 + int(150 * math.cos(math.radians(target_angle))), HEIGHT // 2 - int(150 * math.sin(math.radians(target_angle)))), 3)
        pygame.draw.line(screen, (255, 0, 0), (WIDTH // 2, HEIGHT // 2), (WIDTH // 2 + int(150 * math.cos(math.radians(slider.position * 180))), HEIGHT // 2 - int(150 * math.sin(math.radians(slider.position * 180)))), 3)

        slider.draw(screen)
        draw_text(screen, feedback, 32, WIDTH // 2, HEIGHT // 2 + 250, WHITE)

        pygame.display.flip()
        clock.tick(30)

def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

if __name__ == "__main__":
    main()
