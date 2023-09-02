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

# Base colors
BASE_COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128),
    "teal": (0, 128, 128)
}

# Convert RGB to HSV
def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx * 100
    return h, s, v

# Convert HSV to RGB
def hsv_to_rgb(h, s, v):
    h = float(h)
    s = float(s) / 100
    v = float(v) / 100
    hi = int((h / 60) % 6)
    f = (h / 60) - hi
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


# Function to draw text
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def shift_hue(color, shift_amount):
    h, s, v = rgb_to_hsv(*color)
    h = (h + shift_amount) % 1
    return hsv_to_rgb(h, s, v)

# Main loop for Hue Shift Hunt
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Hue Shift Hunt")
    clock = pygame.time.Clock()
    score = 0
    tries = 10
    feedback = ""
    feedback_color = WHITE

    main_color_name = random.choice(list(BASE_COLORS.keys()))
    main_color = BASE_COLORS[main_color_name]
    shifted_color = shift_hue(main_color, random.uniform(-0.1, 0.1))
    colors = [main_color, shifted_color]

    while tries > 0:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for index, (color_name, color) in enumerate(BASE_COLORS.items()):
                    rect = pygame.Rect((index+1)*420 , HEIGHT // 2 - 50, 100, 100)
                    if rect.collidepoint(x, y):
                        # Check if the selected color's hue direction matches the actual hue shift direction
                        if color_name == main_color_name:
                            score += 3
                            feedback = "Correct!"
                            feedback_color = (0, 255, 0)  # Green
                        else:
                            score -= 1
                            feedback = "Wrong!"
                            feedback_color = (255, 0, 0)  # Red
                        tries -= 1
                        main_color_name = random.choice(list(BASE_COLORS.keys()))
                        main_color = BASE_COLORS[main_color_name]
                        shifted_color = shift_hue(main_color, random.uniform(-0.1, 0.1))
                        break

        pygame.draw.rect(screen, main_color, (WIDTH // 4 - 50, HEIGHT // 4, 100, 100))
        pygame.draw.rect(screen, shifted_color, (3*WIDTH // 4 - 50, HEIGHT // 4, 100, 100))
        for index, (color_name, color) in enumerate(BASE_COLORS.items()):
            pygame.draw.rect(screen, color, ((index+1)*420 , HEIGHT // 2 - 50, 100, 100))

        draw_text(screen, feedback, 32, WIDTH // 2, HEIGHT // 2 + 200, feedback_color)
        draw_text(screen, f"Score: {score}", 32, WIDTH - 60, 10, WHITE)

        pygame.display.flip()
        clock.tick(30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    return
                if event.key == pygame.K_r:
                    main()
                    return
        screen.fill(BLACK)
        draw_text(screen, f"Final Score: {score}", 100, WIDTH // 2, HEIGHT // 3, WHITE)
        draw_text(screen, "Press Q to quit and R to restart", 32, WIDTH // 2, HEIGHT // 2 + 150, WHITE)
        pygame.display.flip()

if __name__ == "__main__":
    main()
