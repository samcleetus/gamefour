import pygame
import os
import random
import math
import pickle

from pygame.constants import MOUSEBUTTONDOWN

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

icon = pygame.image.load("./assets/fgame/cursor2.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Defeat the zombies. . . or face consequnces worse than death')
pygame.display.set_icon(icon)

#set framerate
clock = pygame.time.Clock()
fps = 75

#images
health_box_img = pygame.image.load('./assets/img_4/icons/health_box.png')
knight_right_img = pygame.image.load("./assets/fgame/knight_right.png")
knight_left_img = pygame.image.load("./assets/fgame/knight_left.png")
enemy_left = pygame.image.load("./assets/fgame/zombie_left.png")
enemy_right = pygame.image.load("./assets/fgame/zombie_right.png")
boss_left = pygame.image.load("./assets/fgame/boss_left.png")
boss_right = pygame.image.load("./assets/fgame/boss_right.png")
health_box_img = pygame.image.load('./assets/img_4/icons/health_box.png')
crosshair_img = pygame.image.load("./assets/fgame/crosshair.png")
bg_img = pygame.image.load("./assets/fgame/room_1.png")
room_1 = pygame.transform.scale(bg_img, (800, 800))
bg_img = pygame.image.load("./assets/fgame/room_2.png")
room_2 = pygame.transform.scale(bg_img, (800, 800))
bg_img = pygame.image.load("./assets/fgame/room_3.png")
room_3 = pygame.transform.scale(bg_img, (800, 800))
bg_img = pygame.image.load("./assets/fgame/room_4.png")
room_4 = pygame.transform.scale(bg_img, (800, 800))
bg_img = pygame.image.load("./assets/fgame/room_5.png")
room_5 = pygame.transform.scale(bg_img, (800, 800))



#change mouse image
#pygame.mouse.set_visible(False)
#MANUAL_CURSOR = pygame.image.load("./assets/fgame/cursor2.png").convert_alpha()

#colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0,0,255)
outside_col = (0, 2, 18)
red = (255, 0, 0)
green = (0, 255, 0)

#groups
enemy_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()

#game variables
move = 0
shoot_ok = True
change_dir = False
moving_right = False
moving_left = False
score = 0
game_score = 0
font = pygame.font.SysFont('Futura', 30)
collide = False
move_left = False
move_right = False
move_down = False
move_right_2 = False
move_down_2 = False
move_left_3 = False
move_left_5 = False
move_up_5 = False
move_right_4 = False
move_up_4 = False
room = 1

#defs
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def check_player_movement():
    global moving_left
    global moving_right
    global change_dir
    if moving_right == True:
        change_dir = 1
    elif moving_left == True:
        change_dir = 2

    return change_dir

def get_random():
    #rand_enemies = random.randint(2, 4)
    rand_x = random.randint(1, 775)
    rand_y = random.randint(1, 709)
    rand_gremlin = random.randint(1, 3)
    rand_enemies = random.randint(1, 2)

    return rand_x, rand_y, rand_gremlin, rand_enemies

def draw_img(img, x, y):
    img = img
    screen.blit(img, (x, y))

def get_boss():
    rand_boss = random.randint(1, 20)

    return rand_boss

def draw_rect(player):
    global move_left
    global move_right
    global move_down
    global move_right_2
    global move_down_2
    global move_left_3
    global move_left_5
    global move_up_5
    global move_right_4
    global move_up_4
    #room 1
    if room == 1:
        #left exit
        left_rect = pygame.draw.rect(screen, blue, pygame.Rect(0, 300, 30, 130))
        if left_rect.colliderect(player.rect):
            move_left = True
        else:
            move_left = False

        #right exit
        right_rect = pygame.draw.rect(screen, blue, pygame.Rect(770, 300, 30, 130))
        if right_rect.colliderect(player.rect):
            move_right = True
        else:
            move_right = False

        #south exit
        bottom_rect = pygame.draw.rect(screen, blue, pygame.Rect(275, 710, 251, 100))
        if bottom_rect.colliderect(player.rect):
            move_down = True
        else:
            move_down = False

    #----------------------------------------------------------------------------------
    #room 2

    if room == 2:
        #right exit
        right_rect = pygame.draw.rect(screen, blue, pygame.Rect(770, 367, 30, 150))
        if right_rect.colliderect(player.rect):
            move_right_2 = True
        else:
            move_right_2 = False

        #south exit
        bottom_rect = pygame.draw.rect(screen, blue, pygame.Rect(235, 690, 223, 150))
        if bottom_rect.colliderect(player.rect):
            move_down_2 = True
        else:
            move_down_2 = False

    
    #----------------------------------------------------------------------------------
    #room 3
    if room == 3:
        #left exit
        left_rect = pygame.draw.rect(screen, blue, pygame.Rect(0, 290, 52, 225))
        if left_rect.colliderect(player.rect):
            move_left_3 = True
        else:
            move_left_3 = False

    #----------------------------------------------------------------------------------
    #room 4
    if room == 4:
        #left exit
        right_rect = pygame.draw.rect(screen, blue, pygame.Rect(769, 313, 30, 170))
        if right_rect.colliderect(player.rect):
            move_right_4 = True
        else:
            move_right_4 = False

        #north exit
        up_rect = pygame.draw.rect(screen, blue, pygame.Rect(277, 0, 245, 107))
        if up_rect.colliderect(player.rect):
            move_up_4 = True
        else:
            move_up_4 = False

    #----------------------------------------------------------------------------------
    #room 5
    if room == 5:
        #left exit
        left_rect = pygame.draw.rect(screen, blue, pygame.Rect(0, 290, 30, 225))
        if left_rect.colliderect(player.rect):
            move_left_5 = True
        else:
            move_left_5 = False

        #north exit
        up_rect = pygame.draw.rect(screen, blue, pygame.Rect(277, 0, 245, 107))
        if up_rect.colliderect(player.rect):
            move_up_5 = True
        else:
            move_up_5 = False

    
    




#classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, damage):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.max_health = 1000
        self.health = self.max_health
        self.damage = damage
        self.image = pygame.transform.scale(knight_left_img, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed

    def move(self, move):
        global room
        dx = 0
        dy = 0

		#assign moving variables
        if move == 1: #left
            self.image = pygame.transform.scale(knight_left_img, (50, 60))
            dx = -self.speed
        if move == 2: #right
            self.image = pygame.transform.scale(knight_right_img, (50, 60))
            dx = self.speed
        if move == 4:
            dy = -self.speed
        if move == 3:
            dy = self.speed

    
        #check if player left the designated play zone

        #room 1
        if self.rect.left < 25 and move_left == False and room == 1:
            self.rect.left = 25
        if self.rect.right > SCREEN_WIDTH - 25 and move_right == False and room == 1:
            self.rect.right = SCREEN_WIDTH - 25
        if self.rect.bottom < 95 and room == 1:
            self.rect.bottom = 95
        if self.rect.bottom >= SCREEN_HEIGHT - 91 and move_down == False and room == 1:
            self.rect.bottom = SCREEN_HEIGHT - 91

        if self.rect.right > SCREEN_WIDTH and room == 1:
            room = 3
            self.rect.x = 15
            self.rect.y = 360

        if self.rect.left < 0 and room == 1:
            room = 2
            self.rect.x = 710
            self.rect.y = 400

        if self.rect.bottom >= SCREEN_HEIGHT and room == 1:
            room = 5
            self.rect.x = 375
            self.rect.y = 15

        #room 2
        if self.rect.left < 25 and room == 2:
            self.rect.left = 25
        if self.rect.right > SCREEN_WIDTH - 25 and move_right_2 == False and room == 2:
            self.rect.right = SCREEN_WIDTH - 25
        if self.rect.bottom < 109 and room == 2:
            self.rect.bottom = 109
        if self.rect.bottom >= SCREEN_HEIGHT - 109 and move_down_2 == False and room == 2:
            self.rect.bottom = SCREEN_HEIGHT - 109

        if self.rect.right > SCREEN_WIDTH and room == 2:
            room = 1
            self.rect.x = 15
            self.rect.y = 340

        if self.rect.bottom >= SCREEN_HEIGHT and room == 2:
            room = 4
            self.rect.x = 375
            self.rect.y = 15

        #room 3
        if self.rect.left < 52 and room == 3 and move_left_3 == False:
            self.rect.left = 52

        if self.rect.right > SCREEN_WIDTH - 57 and room == 3:
            self.rect.right = SCREEN_WIDTH - 57
        if self.rect.bottom < 170 and room == 3:
            self.rect.bottom = 170
        if self.rect.bottom >= SCREEN_HEIGHT - 164 and move_down_2 == False and room == 3:
            self.rect.bottom = SCREEN_HEIGHT - 164

        if self.rect.left < 0 and room == 3:
            room = 1
            bg_img = pygame.image.load("./assets/fgame/room_1.png")
            bg = pygame.transform.scale(bg_img, (800, 800))
            self.rect.x = 710
            self.rect.y = 340

        #room 4
        if self.rect.left < 25 and room == 4:
            self.rect.left = 25
        if self.rect.right > SCREEN_WIDTH - 25 and move_right_4 == False and room == 4:
            self.rect.right = SCREEN_WIDTH - 25
        if self.rect.bottom < 109 and move_up_4 == False and room == 4:
            self.rect.bottom = 109
        if self.rect.bottom >= SCREEN_HEIGHT - 109 and room == 4:
            self.rect.bottom = SCREEN_HEIGHT - 109

        if self.rect.top < 0 and room == 4:
            room = 2
            self.rect.x = 335
            self.rect.y = 710  

        if self.rect.right > SCREEN_WIDTH and room == 4:
            room = 5
            self.rect.x = 15
            self.rect.y = 360  
        
        #room 5
        if self.rect.left < 25 and move_left_5 == False and room == 5:
            self.rect.left = 25
        if self.rect.right > SCREEN_WIDTH - 25 and room == 5:
            self.rect.right = SCREEN_WIDTH - 25
        if self.rect.bottom < 109 and move_up_5 == False and room == 5:
            self.rect.bottom = 109
        if self.rect.bottom >= SCREEN_HEIGHT - 109 and room == 5:
            self.rect.bottom = SCREEN_HEIGHT - 109

        if self.rect.left < 0 and room == 5:
            room = 4
            self.rect.x = 710
            self.rect.y = 360

        if self.rect.top < 0 and room == 5:
            room = 1
            self.rect.x = 375
            self.rect.y = 710


        #update rect position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if shoot_ok == True:
            pos = pygame.mouse.get_pos()
            for enemy in enemy_group:
                if enemy.rect.collidepoint(pos):
                    enemy.health -= self.damage
            for boss in boss_group:
                if boss.rect.collidepoint(pos):
                    boss.health -= self.damage

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.damage = 0
            self.alive = False

    def update(self, enemy_group):
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(self, enemy_group, False) and enemy.alive:
                self.health -= enemy.damage
        for boss in boss_group:
            if pygame.sprite.spritecollide(self, boss_group, False) and boss.alive:
                self.health -= boss.damage

        for potion in potion_group:
            if pygame.sprite.spritecollide(self, potion_group, False):
                potion.kill()
                self.health += 150
                if self.health + 150 >= self.max_health:
                    self.health = self.max_health
                


    def draw(self):
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, x, y, speed, damage):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.name = name
        self.speed = speed
        self.max_health = 100
        self.health = self.max_health
        self.damage = damage
        img = pygame.image.load(f"./assets/fgame/{self.name}_left.png")
        self.image = pygame.transform.scale(img, (33, 46))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        #print(dist)
        try:
            dx, dy = dx / dist, dy / dist  
        except:
            pass

        change_dir = check_player_movement()
        if change_dir == 1:
            img = pygame.image.load(f"./assets/fgame/{self.name}_right.png")
            self.image = pygame.transform.scale(img, (33, 46))
        elif change_dir == 2:
            img = pygame.image.load(f"./assets/fgame/{self.name}_left.png")
            self.image = pygame.transform.scale(img, (33, 46))

        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def spawn(self):
        rand_x, rand_y, rand_gremlin, rand_enemies = get_random()
        if len(enemy_group) >= 4:
            rand_enemies = 0
        if rand_gremlin == 1:
            for enemy in range(rand_enemies):
                rand_x, rand_y, rand_gremlin, rand_enemies = get_random()
                enemy = Enemy('zombie', rand_x, rand_y, 2, 1)
                enemy_group.add(enemy)

        elif rand_gremlin == 2:
            for gremlin in range(rand_enemies):
                rand_x, rand_y, rand_boss, rand_enemies = get_random()
                enemy = Enemy('gremlin', rand_x, rand_y, 2, 1)
                enemy_group.add(enemy)

        elif rand_gremlin == 3:
            rand_x, rand_y, rand_boss, rand_enemies = get_random()
            if len(potion_group) < 1:
                health_potion = Potion('health', rand_x, rand_y)
                potion_group.add(health_potion)
            else:
                enemy = Enemy('zombie', rand_x, rand_y, 2, 1)
                enemy_group.add(enemy)
        

    def check_alive(self):
        global change_dir
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.damage = 0
            self.alive = False

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

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, damage):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.max_health = 250
        self.health = self.max_health
        self.damage = damage
        self.image = pygame.transform.scale(boss_left, (61, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        #print(dist)
        try:
            dx, dy = dx / dist, dy / dist  
        except:
            pass

        change_dir = check_player_movement()
        if change_dir == 1:
            self.image = pygame.transform.scale(boss_right, (61, 80))
        elif change_dir == 2:
            self.image = pygame.transform.scale(boss_left, (61, 80))

        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def spawn(self):
        rand_x, rand_y, rand_bigboss, rand_enemies = get_random()
        rand_enemies = 1
        for enemy in range(rand_enemies):
            #rand_x, rand_y, rand_boss = get_random()
            boss = Boss(rand_x, rand_y, 2, 5)
            boss_group.add(boss)
        

    def check_alive(self):
        global change_dir
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.damage = 0
            self.alive = False

    def draw(self):
        screen.blit(self.image, self.rect)

class Potion(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        img = pygame.image.load(f"./assets/fgame/{self.name}_potion.png")
        self.image = pygame.transform.scale(img, (28, 35))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)
        

#create instances
player = Player(400, 400, 5, 50)
enemy = Enemy('zombie', 600, 200, 2, 1)
enemy_group.add(enemy)
boss = Boss(600, 200, 2, 5)
boss_group.add(boss)

health_bar = HealthBar(52, int(18.5), player.health, player.max_health)

run = True
while run:
    clock.tick(fps)

    draw_rect(player)

    if room == 1:
        screen.blit(room_1, (0, 0))
    elif room == 2:
        screen.blit(room_2, (0, 0))
    elif room == 3:
        screen.blit(room_3, (0, 0))
    elif room == 4:
        screen.blit(room_4, (0, 0))
    elif room == 5:
        screen.blit(room_5, (0, 0))

    #draw_rect(player)

    #show the healthbar
    draw_img(health_box_img, 10, 10)
    health_bar.draw(player.health)

    #show score
    draw_text(f'Score: {score}', font, white, 700, 10)

    #player defs and actions and shit
    if player.alive:
        player.move(move)
    player.draw()
    player.check_alive()
    player.update(enemy_group)


    #enemy defs and actions and shit
    for enemy in enemy_group:
        enemy.move_towards_player(player)
        enemy.draw()
        enemy.check_alive()
        enemy.update()
    if score > 5:
        boss.draw()
        boss.move_towards_player(player)
        boss.check_alive()
        boss.update()

    for potion in potion_group:
        potion.draw()

    for enemy in enemy_group:
        if enemy.alive == False:
            score += 1
            enemy.spawn()
            enemy.kill()

    for boss in boss_group:
        if boss.alive == False:
            score += 5
            boss.spawn()
            boss.kill()

    if collide == True:
        for potion in potion_group:
            potion.kill()


    #change mouse image
    #screen.blit( MANUAL_CURSOR, ( pygame.mouse.get_pos() ) )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and player.alive:
                move = 1
                moving_left = True
            if event.key == pygame.K_d and player.alive:
                move = 2
                moving_right = True
            if event.key == pygame.K_s and player.alive:
                move = 3
            if event.key == pygame.K_w and player.alive:
                move = 4
        if event.type == MOUSEBUTTONDOWN and player.alive:
            player.shoot()


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move = 0
                moving_left = False
            if event.key == pygame.K_d:
                move = 0
                moving_right = False
            if event.key == pygame.K_s:
                move = 0
            if event.key == pygame.K_w:
                move = 0

    pygame.display.update()