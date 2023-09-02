import pygame
import random
import os

# Initialize pygame
pygame.init()

# Constants
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_NAME = pygame.font.match_font('arial')

# Feedback Sounds
correct_sound = pygame.mixer.Sound(os.path.join('correct.wav'))
wrong_sound = pygame.mixer.Sound(os.path.join('incorrect.wav'))

# Function to draw text
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font("zenhand3.ttf", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Main loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Color Shade Matcher")
    clock = pygame.time.Clock()
    score = 0
    tries = 10
    difficulty = 300
    feedback = ""
    feedback_color = WHITE
    main_color = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    colors = [main_color]

    for _ in range(4):
        shade = random.randint(-difficulty, difficulty)
        colors.append((max(0, min(255, main_color[0] + shade)),
                       max(0, min(255, main_color[1] + shade)),
                       max(0, min(255, main_color[2] + shade))))

    random.shuffle(colors)

    while tries > 0:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for index, color in enumerate(colors):
                    rect = pygame.Rect((index+1)*420 , HEIGHT // 2 - 50, 100, 100)
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
                        colors = [main_color]
                        for _ in range(4):
                            shade = random.randint(-difficulty, difficulty)
                            colors.append((max(0, min(255, main_color[0] + shade)),
                                           max(0, min(255, main_color[1] + shade)),
                                           max(0, min(255, main_color[2] + shade))))
                        random.shuffle(colors)
                        break

        pygame.draw.rect(screen, main_color, (WIDTH // 2 - 50, HEIGHT // 4, 100, 100))
        for index, color in enumerate(colors):
            pygame.draw.rect(screen, color, ((index+1)*420 , HEIGHT // 2 - 50, 100, 100))

        draw_text(screen, feedback, 32, WIDTH // 2, HEIGHT // 2 + 100, feedback_color)
        draw_text(screen, f"Difficulty: {int(1/difficulty*300)}  Score: {score}", 32, WIDTH - 200, 10, WHITE)

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
