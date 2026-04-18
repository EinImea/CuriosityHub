import pygame
import sys
import random
import math

class Particle:
    def __init__(self, x, y, color, velocity=None):
        self.x, self.y = x, y
        self.vx, self.vy = velocity if velocity else (random.uniform(-7, -2), random.uniform(-2, 2))
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

class SpaceSnake:
    def __init__(self, x, y, length=8, color_head=(180, 50, 255), color_body=(100, 20, 180)):
        self.segments = [[x + i*15, y] for i in range(length)]
        self.angle = random.uniform(0, 6.28)
        self.speed = random.uniform(3, 5)
        self.amplitude = random.uniform(3, 6)
        self.color_head = color_head
        self.color_body = color_body

    def update(self, scroll_speed, target_y=None):
        self.angle += 0.15
        head = self.segments[0]
        head[0] -= (scroll_speed + self.speed)
        
        if target_y is not None: # Homing Logic for Jormungandr
            dy = target_y - head[1]
            head[1] += dy * 0.05
        else:
            head[1] += math.sin(self.angle) * self.amplitude
        
        for i in range(len(self.segments)-1, 0, -1):
            self.segments[i][0] -= scroll_speed
            dx = self.segments[i-1][0] - self.segments[i][0]
            dy = self.segments[i-1][1] - self.segments[i][1]
            self.segments[i][0] += dx * 0.25
            self.segments[i][1] += dy * 0.25

    def get_rects(self):
        return [pygame.Rect(s[0]-8, s[1]-8, 16, 16) for s in self.segments]

    def draw(self, screen, offset):
        for i, s in enumerate(self.segments):
            color = self.color_head if i == 0 else self.color_body
            size = 12 if i == 0 else max(4, 10 - (i//3))
            pygame.draw.circle(screen, color, (int(s[0] + offset[0]), int(s[1] + offset[1])), size)

def run_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("STARDUST: JORMUNGANDR RISING")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 25)

    player_rect = pygame.Rect(100, 300, 14, 14)
    score, scroll_speed = 0, 5
    has_shield = False
    dash_power, dash_cooldown, current_cooldown, shake_timer = 180, 50, 0, 0
    is_dashing = False
    target_x = 100

    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(100)]
    obstacles, snakes, particles, powerups = [], [], [], []
    jormungandr = None
    
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 500)

    running = True
    while running:
        render_offset = [0, 0]
        if shake_timer > 0:
            render_offset = [random.randint(-6, 6), random.randint(-6, 6)]
            shake_timer -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == SPAWN_EVENT:
                chance = random.random()
                # Jormungandr Spawn (Low probability if one doesn't exist)
                if score > 1000 and jormungandr is None and random.random() < 0.05:
                    jormungandr = SpaceSnake(WIDTH+100, HEIGHT//2, length=30, color_head=(255, 50, 50), color_body=(150, 0, 0))
                    shake_timer = 30
                    print("JORMUNGANDR HAS AWAKENED")
                
                if chance < 0.65:
                    h = random.randint(60, 180)
                    obstacles.append(pygame.Rect(WIDTH+50, random.randint(0, HEIGHT-h), 35, h))
                elif chance < 0.85:
                    snakes.append(SpaceSnake(WIDTH+50, random.randint(100, HEIGHT-100)))
                
                if random.random() < 0.12:
                    powerups.append(pygame.Rect(WIDTH+50, random.randint(50, HEIGHT-50), 18, 18))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_rect.top > 0: player_rect.y -= 7
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT: player_rect.y += 7

        if keys[pygame.K_SPACE] and current_cooldown == 0:
            player_rect.x += dash_power
            current_cooldown, is_dashing = dash_cooldown, True
            for _ in range(15): particles.append(Particle(player_rect.x, player_rect.centery, (200, 255, 255)))

        if player_rect.x > target_x:
            player_rect.x -= 5
            is_dashing = True
        else:
            player_rect.x, is_dashing = target_x, False

        if current_cooldown > 0: current_cooldown -= 1
        score += 1

        # Updates
        for s in stars:
            s[0] -= scroll_speed * 0.2
            if s[0] < 0: s[0] = WIDTH
            
        for obs in obstacles: obs.x -= scroll_speed
        for p in powerups: p.x -= scroll_speed
        for snk in snakes: snk.update(scroll_speed)
        
        if jormungandr:
            jormungandr.update(scroll_speed, player_rect.y)
            if jormungandr.segments[-1][0] < -200: jormungandr = None

        particles = [p for p in particles if p.update(scroll_speed)]
        obstacles = [o for o in obstacles if o.right > -50]
        powerups = [p for p in powerups if p.right > -50]
        snakes = [s for s in snakes if s.segments[0][0] > -100]

        # Jormungandr Collision
        if jormungandr:
            for seg_rect in jormungandr.get_rects():
                if player_rect.colliderect(seg_rect):
                    if is_dashing:
                        shake_timer = 20
                        # You can't kill Jormungandr in one hit, but you bounce off
                        player_rect.x -= 40 
                        for _ in range(10): particles.append(Particle(seg_rect.centerx, seg_rect.centery, (255, 0, 0)))
                    elif has_shield:
                        has_shield = False
                        jormungandr = None # Only a shield can banish it
                        shake_timer = 40
                    else:
                        running = False

        # Standard Collisions
        for snk in snakes[:]:
            hit = False
            for seg in snk.get_rects():
                if player_rect.colliderect(seg):
                    if is_dashing or has_shield:
                        if has_shield and not is_dashing: has_shield = False
                        shake_timer, hit = 15, True
                        for _ in range(20): particles.append(Particle(seg.centerx, seg.centery, (180, 50, 255)))
                        break
                    else: running = False
            if hit: snakes.remove(snk)

        for obs in obstacles[:]:
            if player_rect.colliderect(obs):
                if is_dashing or has_shield:
                    if has_shield and not is_dashing: has_shield = False
                    shake_timer = 10
                    obstacles.remove(obs)
                else: running = False

        for p in powerups[:]:
            if player_rect.colliderect(p):
                has_shield = True
                powerups.remove(p)

        # Draw
        screen.fill((5, 5, 12))
        for s in stars: pygame.draw.circle(screen, (70, 70, 100), (int(s[0]+render_offset[0]), s[1]+render_offset[1]), 1)
        for p in particles: p.draw(screen, render_offset)
        for o in obstacles: pygame.draw.rect(screen, (60, 60, 75), o.move(render_offset[0], render_offset[1]))
        for p in powerups: pygame.draw.circle(screen, (0, 200, 255), (int(p.centerx+render_offset[0]), int(p.centery+render_offset[1])), 9)
        for snk in snakes: snk.draw(screen, render_offset)
        if jormungandr: jormungandr.draw(screen, render_offset)

        p_color = (0, 255, 255) if is_dashing else (255, 255, 255)
        if has_shield and not is_dashing: p_color = (0, 255, 150)
        pygame.draw.rect(screen, p_color, player_rect.move(render_offset[0], render_offset[1]))
        
        screen.blit(font.render(f"SCORE: {score}", True, (255, 255, 0)), (20, 20))
        if jormungandr: screen.blit(font.render("BOSS WARNING", True, (255, 0, 0)), (WIDTH//2 - 80, 20))
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    run_game()
