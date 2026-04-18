import pygame
import sys
import random

class Particle:
    def __init__(self, x, y, color, velocity=None):
        self.x, self.y = x, y
        if velocity:
            self.vx, self.vy = velocity
        else:
            self.vx = random.uniform(-7, -2)
            self.vy = random.uniform(-2, 2)
        self.lifetime = 255
        self.color = color

    def update(self, scroll):
        self.x += self.vx - scroll
        self.y += self.vy
        self.lifetime -= 12
        return self.lifetime > 0

    def draw(self, screen, offset=(0,0)):
        if self.lifetime > 0:
            s = pygame.Surface((4, 4))
            s.set_alpha(self.lifetime)
            s.fill(self.color)
            screen.blit(s, (self.x + offset[0], self.y + offset[1]))

def run_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("STARDUST: SMASH & SHATTER")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 25)

    player_rect = pygame.Rect(100, 300, 14, 14)
    score, scroll_speed = 5, 5
    has_shield = False
    
    dash_power, dash_cooldown = 180, 50
    current_cooldown, shake_timer = 0, 0
    is_dashing = False
    target_x = 100

    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(100)]
    obstacles, particles, powerups = [], [], []
    
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 500)

    running = True
    while running:
        render_offset = [0, 0]
        if shake_timer > 0:
            render_offset = [random.randint(-4, 4), random.randint(-4, 4)]
            shake_timer -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == SPAWN_EVENT:
                h = random.randint(50, 180)
                obstacles.append(pygame.Rect(WIDTH + 50, random.randint(0, HEIGHT-h), 35, h))
                if random.random() < 0.12:
                    powerups.append(pygame.Rect(WIDTH + 50, random.randint(50, HEIGHT-50), 18, 18))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_rect.top > 0: player_rect.y -= 7
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT: player_rect.y += 7

        if keys[pygame.K_SPACE] and current_cooldown == 0:
            player_rect.x += dash_power
            current_cooldown = dash_cooldown
            is_dashing = True
            for _ in range(15):
                particles.append(Particle(player_rect.x, player_rect.centery, (200, 255, 255)))

        if player_rect.x > target_x:
            player_rect.x -= 4
            is_dashing = True
        else:
            player_rect.x = target_x
            is_dashing = False

        if current_cooldown > 0: current_cooldown -= 1
        score += 1

        for s in stars:
            s[0] -= scroll_speed * 0.2
            if s[0] < 0: s[0] = WIDTH
            
        for obs in obstacles: obs.x -= scroll_speed
        for p in powerups: p.x -= scroll_speed
        particles = [p for p in particles if p.update(scroll_speed)]
        obstacles = [o for o in obstacles if o.right > -50]
        powerups = [p for p in powerups if p.right > -50]

        for p in powerups[:]:
            if player_rect.colliderect(p):
                has_shield = True
                powerups.remove(p)

        for obs in obstacles[:]:
            if player_rect.colliderect(obs):
                if is_dashing:
                    shake_timer = 10
                    obstacles.remove(obs)
                    for _ in range(20):
                        v = (random.uniform(-10, 10), random.uniform(-10, 10))
                        particles.append(Particle(obs.centerx, obs.centery, (100, 100, 110), v))
                elif has_shield:
                    has_shield = False
                    obstacles.remove(obs)
                    shake_timer = 5
                else:
                    running = False

        screen.fill((5, 5, 12))
        for s in stars: pygame.draw.circle(screen, (70, 70, 100), (int(s[0] + render_offset[0]), s[1] + render_offset[1]), 1)
        for p in particles: p.draw(screen, render_offset)
        for o in obstacles: 
            pygame.draw.rect(screen, (60, 60, 75), o.move(render_offset[0], render_offset[1]))
            pygame.draw.rect(screen, (180, 180, 200), o.move(render_offset[0], render_offset[1]), 1)
        for p in powerups:
            pygame.draw.circle(screen, (0, 200, 255), (p.centerx + render_offset[0], p.centery + render_offset[1]), 9)

        p_color = (0, 255, 255) if is_dashing else (255, 255, 255)
        if has_shield and not is_dashing: p_color = (0, 255, 150)
        pygame.draw.rect(screen, p_color, player_rect.move(render_offset[0], render_offset[1]))
        
        s_txt = font.render(f"SCORE: {score}", True, (255, 255, 0))
        d_txt = font.render("READY" if current_cooldown == 0 else "...", True, (0, 255, 255))
        screen.blit(s_txt, (20, 20))
        screen.blit(d_txt, (20, 50))
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    run_game()
