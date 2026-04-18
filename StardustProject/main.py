import pygame
import sys

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Stardust: First Light")
    clock = pygame.time.Clock()

    # Player position (Start in the middle)
    x, y = 400, 300
    speed = 5

    print("Stardust Engine Active. Use Arrow Keys to move your star!")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 1. Handle Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: x -= speed
        if keys[pygame.K_RIGHT]: x += speed
        if keys[pygame.K_UP]: y -= speed
        if keys[pygame.K_DOWN]: y += speed

        # 2. Draw
        screen.fill((10, 10, 30)) # Deep Space
        
        # Draw the "Star" (a small 10x10 square)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 10, 10))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game()
