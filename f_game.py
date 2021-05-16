import pygame
import os
import random
import math
import pickle

from pygame.constants import MOUSEBUTTONDOWN

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

icon = pygame.image.load("./assets/fgame/crosshair.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The adventure')
pygame.display.set_icon(icon)

#set framerate
clock = pygame.time.Clock()
fps = 65

#game variables
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0,0,255)
outside_col = (
0, 2, 18
)
red = (255, 0, 0)
green = (0, 255, 0)
moving_left = False
moving_right = False
moving_up = False
moving_down = False
move = 0
enemy_group = pygame.sprite.Group()
shoot_ok = True
radius1 = 160
radius2 = 30
enemy_list = []
score = 0
highscore = 0
font = pygame.font.SysFont('Futura', 30)

#images
img = pygame.image.load("./assets/fgame/hero.png")
hero_img = pygame.transform.scale(img, (50, 40))
health_box_img = pygame.image.load('./assets/img_4/icons/health_box.png')
crosshair_img = pygame.image.load("./assets/fgame/crosshair.png")

pygame.mouse.set_visible(False)
MANUAL_CURSOR = pygame.image.load("./assets/fgame/crosshair.png").convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def get_random() -> tuple[int, int, int]:
    rand_x = random.randint(1, 800)
    rand_y = random.randint(1, 800)
    rand_enemies = random.randint(1, 3)

    return [rand_x, rand_y, rand_enemies]

def draw_img(img, x, y):
    img = img
    screen.blit(img, (x, y))

#class player
class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, damage):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.max_health = 100
        self.health = self.max_health
        self.damage = damage
        img = pygame.image.load("./assets/fgame/hero.png")
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed

    def move(self, move):
        dx = 0
        dy = 0

		#assign moving variables
        if move == 1:
            dx = -self.speed
        if move == 2:
            dx = self.speed
        if move == 4:
            dy = -self.speed
        if move == 3:
            dy = self.speed

        #check if player has walked off the screen
        if self.rect.left < 0:
                self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        #update rect position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if shoot_ok == True:
            pos = pygame.mouse.get_pos()
            for enemy in enemy_group:
                if enemy.rect.collidepoint(pos):
                    enemy.health -= self.damage

    def update(self, enemy_group):
        if pygame.sprite.spritecollide(self, enemy_group, False):
            self.health -= enemy.damage

        

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False

    def draw_hit_zone(self):
        self.hit_zone = pygame.draw.circle(screen, white, (self.rect.x + 15, self.rect.y + 14), 160)
        self.hit_zone.center = self.rect.center


    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #update with new health
        self.health = health

        #calculate ratio
        ratio = self.health / self.max_health

        pygame.draw.rect(screen, black, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

#class enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, damage):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.max_health = 100
        self.health = self.max_health
        self.damage = damage
        img = pygame.image.load("./assets/fgame/enemy.png")
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        try:
            dx, dy = dx / dist, dy / dist  
        except:
            pass
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
    

    def spawn(self):
        rand_x, rand_y, rand_enemies = get_random()
        for enemy in range(rand_enemies):
            enemy = Enemy(rand_x, rand_y, 2, self.damage + 2)
            enemy_group.add(enemy)


    def draw_hit_zone(self):
        for enemy in enemy_group:
            self.hit_zone = pygame.draw.circle(screen, white, (self.rect.x + 15, self.rect.y + 25), 30)
            self.hit_zone.center = self.rect.center

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.damage = 0
            self.alive = False


    def draw(self):
        screen.blit(self.image, self.rect)



player = Player(hero_img, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 5, 25)

enemy = Enemy(200, 300, 2, 1)
enemy_group.add(enemy)
#enemy2 = Enemy(400, 500, 2, 1)
#enemy_group.add(enemy2)


health_bar = HealthBar(52, int(18.5), player.health, player.max_health)
health_bar2 = HealthBar(52, 50, enemy.health, enemy.max_health)
#health_bar3 = HealthBar(52, 100, enemy2.health, enemy2.max_health)

run = True
while run:
    clock.tick(fps)

    #load/create highscore
    try:
        with open('high_score.dat', 'rb') as file:
            highscore = pickle.load(file)

    except:
        highscore = 0

    if player.alive:
        player.move(move)


    screen.fill(outside_col)

    #show score
    draw_text(f'Score: {score}', font, white, 700, 10)

    #show the healthbar
    draw_img(health_box_img, 10, 10)
    health_bar.draw(player.health)
    health_bar2.draw(enemy.health)
    #health_bar3.draw(enemy2.health)

    #player.draw_hit_zone()
    player.draw()
    player.check_alive()
    player.update(enemy_group)

    #for enemy in enemy_group:   
    enemy.draw()
    enemy.move_towards_player(player)
    #enemy.draw_hit_zone()
    enemy.check_alive()
    enemy.update()

    for enemy in enemy_group:
        if enemy.alive == False:
            score += 1
            enemy.kill()
            enemy.spawn()



    with open('high_score.dat', 'wb') as file:
        pickle.dump(highscore, file)
    
    screen.blit( MANUAL_CURSOR, ( pygame.mouse.get_pos() ) )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and player.alive:
                move = 1
                #print(moving_left)
            if event.key == pygame.K_d and player.alive:
                move = 2
                #print(moving_right)
            if event.key == pygame.K_s and player.alive:
                move = 3
                #print(moving_down)
            if event.key == pygame.K_w and player.alive:
                move = 4
                #print(moving_up)
        if event.type == MOUSEBUTTONDOWN and player.alive:
            player.shoot()


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move = 0
            if event.key == pygame.K_d:
                move = 0
            if event.key == pygame.K_s:
                move = 0
            if event.key == pygame.K_w:
                move = 0

    pygame.display.update()