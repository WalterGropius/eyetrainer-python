import pygame
import random, os

# Initialize pygame
pygame.init()

# Constants
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_NAME = pygame.font.match_font('arial')
correct_sound = pygame.mixer.Sound(os.path.join('correct.wav'))
close_sound = pygame.mixer.Sound(os.path.join('nb.wav'))
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
    pygame.display.set_caption("Guess the Aspect Ratio")
    clock = pygame.time.Clock()
    input_box = pygame.Rect(WIDTH // 2 - 70, 20, 140, 32)
    color_active = pygame.Color('dodgerblue2')
    active = True
    color = color_active
    text = ''
    font = pygame.font.Font(None, 32)
    score = 0
    tries = 10
    feedback = ""
    feedback_color = WHITE
    aspect_ratio = random.uniform(1, 3)
    rect_width = random.randint(100, WIDTH - 100)
    rect_height = int(rect_width / aspect_ratio)
    if rect_height > HEIGHT - 200:
        rect_height = random.randint(100, HEIGHT - 200)
        rect_width = int(rect_height * aspect_ratio)

    while tries > 0:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            numerator, denominator = sorted([float(text.split(',')[0]), float(text.split(',')[1])], reverse=True)
                            guess = numerator / denominator
                            if 0.8 * aspect_ratio <= guess <= 1.2 * aspect_ratio:
                                score += 1
                                feedback = "in the ballpark"
                                feedback_color = (255, 255, 0)  # Yellow
                                close_sound.play()
                            if 0.9 * aspect_ratio <= guess <= 1.1 * aspect_ratio:
                                score += 2
                                feedback = "spot on!"
                                feedback_color = (0, 255, 0)  # Green
                                correct_sound.play()
                            else:
                                score -= 3
                                feedback = "baad!"
                                feedback_color = (255, 0, 0)  # Red
                                wrong_sound.play()
                            tries -= 1
                            aspect_ratio = random.uniform(1, 3)
                            rect_width = random.randint(100, WIDTH - 100)
                            rect_height = int(rect_width / aspect_ratio)
                            if rect_height > HEIGHT - 200:
                                rect_height = random.randint(100, HEIGHT - 200)
                                rect_width = int(rect_height * aspect_ratio)
                        except:
                            feedback = "Invalid input"
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - rect_width // 2, HEIGHT // 2 - rect_height // 2, rect_width, rect_height))
        draw_text(screen, feedback, 32, WIDTH // 2, HEIGHT // 2 + 100, feedback_color)
        draw_text(screen, f"Score: {score}", 32, WIDTH - 60, 10, WHITE)

        pygame.display.flip()
        clock.tick(30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.fill(BLACK)
        draw_text(screen, f"Final Score: {score}", 100, WIDTH // 2, HEIGHT // 3, WHITE)
        draw_text(screen, "Press Q to quit and R to restart", 32, WIDTH // 2, HEIGHT // 2 + 150, WHITE)
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

        pygame.display.flip()

if __name__ == "__main__":
    main()
