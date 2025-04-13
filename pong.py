import pygame, time, random
from pygame.locals import *
from pong_ai import PongAI

pygame.init()

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720

running = True

FPS = 60
FramePerSec = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)

displaysurf = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Not-So-Smart Pong.")

class PlayerPaddle(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((10,75))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH-5, SCREEN_HEIGHT/2))
        self.velocity = 7.5

    def update(self):
        #pressed_keys = pygame.key.get_pressed()

        X_i = [ball.rect.centerx, ball.rect.centery, ball.velocity_x, ball.velocity_y, self.rect.centery]
        enemy.ai.X.append(X_i)

        #if pressed_keys[K_UP] and self.rect.top > 0:
        if ball.rect.centery < self.rect.centery and self.rect.top > 0:
            self.rect.move_ip(0,-self.velocity)
            enemy.ai.y.append(-1)
        #elif pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
        elif ball.rect.centery > self.rect.centery and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0,self.velocity)
            enemy.ai.y.append(1)
        else:
            enemy.ai.y.append(0)

    def draw(self):
        displaysurf.blit(self.surf,self.rect)

class EnemyPaddle(pygame.sprite.Sprite):

    def __init__(self,mode="d",isEnemy=True):
        super().__init__()
        self.surf = pygame.Surface((10,75))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center = ((5 if isEnemy else SCREEN_WIDTH-5), SCREEN_HEIGHT/2))
        self.velocity = 7.5
        self.ai = PongAI(mode)
        self.current_data = None
    
    def update(self):
        if self.ai.isTrained:
            X = [ball.rect.centerx, ball.rect.centery, ball.velocity_x, ball.velocity_y, self.rect.centery]
            dir = self.ai.predict([X])[0]
            if self.rect.top > 0 and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.move_ip(0, self.velocity * dir)

            if dir == -1 and self.rect.top > 0:
                self.rect.move_ip(0, -self.velocity)
            elif dir == 1 and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.move_ip(0, self.velocity)

        

    def draw(self):
        displaysurf.blit(self.surf,self.rect)

class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((10,10))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.vel = 5
        self.velocity_x = self.vel
        self.velocity_y = 0

    def update(self):

        def sign(x):
            if x>0:
                return 1
            elif x<0:
                return -1
            else:
                return 0

        if (self.rect.right > SCREEN_WIDTH or self.rect.left < 0) and not pygame.sprite.spritecollideany(self,Paddles):
            enemy.ai.train()
            time.sleep(0.5)
            for entity in Paddles:
                entity.rect.centery = SCREEN_HEIGHT/2
            self.rect.centerx = SCREEN_WIDTH/2
            self.rect.centery = SCREEN_HEIGHT/2
            self.velocity_x = self.vel * random.choice([1,-1])

        if self.rect.top <1 or self.rect.bottom > SCREEN_HEIGHT+1:
            self.velocity_y *= -1

        if pygame.sprite.spritecollideany(self, Paddles):
    # Find the actual paddle it collided with
            for paddle in Paddles:
                if self.rect.colliderect(paddle.rect):
                    # Only reverse direction if the ball is moving toward the paddle
                    if (self.velocity_x < 0 and paddle == enemy) or (self.velocity_x > 0 and paddle == player):
                        self.velocity_x *= -1

                        # Optional: add spin based on paddle movement
                        self.velocity_y += int(0.5 * paddle.velocity * (
                            -1 if paddle == enemy else 1
                        ))  # direction-sensitive

                    break

        self.rect.move_ip(self.velocity_x,self.velocity_y)
        
    def draw(self):
        displaysurf.blit(self.surf,self.rect)




player = PlayerPaddle()
enemy = EnemyPaddle("lr")

Paddles = pygame.sprite.Group()
Paddles.add(player)
Paddles.add(enemy)

ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(ball)

def start():
    global running
    while running:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        

        
        for sprite in all_sprites:
            sprite.update()

        displaysurf.fill(BLACK)
        for sprite in all_sprites:
            sprite.draw()

        pygame.display.flip()

        pygame.display.update()
        FramePerSec.tick(FPS)

start()