import pygame
import random
import os
import colorsys
import sys

# Initialize pygame
pygame.init()

# Constants
infoObject = pygame.display.Info()
magicnumber = 420
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_NAME = pygame.font.match_font('arial')

# Feedback Sounds
correct_sound = pygame.mixer.Sound(os.path.join('correct.wav'))
wrong_sound = pygame.mixer.Sound(os.path.join('incorrect.wav'))
feedback = ""
feedback_color = WHITE

# Function to draw text
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font("zenhand3.ttf", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Convert HSV to RGB
def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Generate colors based on mode
def generate_colors(mode, main_color, difficulty):
    if mode == "tone":
        colors = [main_color]
        for _ in range(4):
            shade = int(random.uniform(-difficulty, difficulty))
            colors.append((max(0, min(255, main_color[0] + shade)),
                           max(0, min(255, main_color[1] + shade)),
                           max(0, min(255, main_color[2] + shade))))
    elif mode == "hue":
        h, s, v = colorsys.rgb_to_hsv(main_color[0]/255, main_color[1]/255, main_color[2]/255)
        colors = [main_color]
        for _ in range(4):
            h_variation = (h + random.uniform(-difficulty/magicnumber, difficulty/magicnumber)) % 1
            colors.append(hsv_to_rgb(h_variation, s, v))
    else:  # mode == "saturation"
        h, s, v = colorsys.rgb_to_hsv(main_color[0]/255, main_color[1]/255, main_color[2]/255)
        colors = [main_color]
        for _ in range(4):
            s_variation = max(0, min(1, s + random.uniform(-difficulty, difficulty)))
            colors.append(hsv_to_rgb(h, s_variation, v))
    random.shuffle(colors)
    return colors

# Main loop
def main(mode):
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption(f"{mode.capitalize()} Variation Matcher")
    clock = pygame.time.Clock()
    score = 0
    tries = 10
    difficulty = 300
    main_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    colors = generate_colors(mode, main_color, difficulty)
    feedback = ""
    feedback_color = WHITE

    while tries > 0:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for index, color in enumerate(colors):
                    rect = pygame.Rect((index+1)*magicnumber , HEIGHT // 2 - 50, 100, 100)
                    if rect.collidepoint(x, y):
                        if color == main_color:
                            score += 2
                            feedback = "Correct!"
                            feedback_color = (0, 255, 0)  # Green
                            correct_sound.play()
                        else:
                            score -= 1
                            feedback = "Wrong!"
                            feedback_color = (255, 0, 0)  # Red
                            wrong_sound.play()
                        tries -= 1
                        difficulty = int(difficulty * 0.75)
                        main_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                        colors = generate_colors(mode, main_color, difficulty)
                        break

        pygame.draw.rect(screen, main_color, (WIDTH // 2 - 50, HEIGHT // 4, 100, 100))
        for index, color in enumerate(colors):
            pygame.draw.rect(screen, color, ((index+1)*magicnumber , HEIGHT // 2 - 50, 100, 100))

        draw_text(screen, feedback, 32, WIDTH // 2, HEIGHT // 2 + 100, feedback_color)
        draw_text(screen, f"Difficulty: {int(1/(difficulty+1)*300)}  Score: {score}", 32, WIDTH - 200, 10, WHITE)

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
                    main(mode)
                    return
        screen.fill(BLACK)
        draw_text(screen, f"Final Score: {score}", 100, WIDTH // 2, HEIGHT // 3, WHITE)
        draw_text(screen, "Press Q to quit and R to restart", 32, WIDTH // 2, HEIGHT // 2 + 150, WHITE)
        pygame.display.flip()

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ["tone", "hue", "saturation"]:
        print("Usage: python game.py [tone|hue|saturation]")
        sys.exit(1)
    mode = sys.argv[1]
    main(mode)
