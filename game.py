import pygame
from pygame import mixer
import os
import random
import csv
import button
import pickle


mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

icon = pygame.image.load("./assets/img_4/desert_hawk.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')
pygame.display.set_icon(icon)

#set framerate
clock = pygame.time.Clock()
fps = 65

#images
bullet_img = pygame.image.load('./assets/img_4/icons/bullet.png')
grenade_img = pygame.image.load('./assets/img_4/icons/grenade.png')
health_box_img = pygame.image.load('./assets/img_4/icons/health_box.png')
ammo_box_img = pygame.image.load('./assets/img_4/icons/ammo_box.png')
grenade_box_img = pygame.image.load('./assets/img_4/icons/grenade_box.png')
coin_img = pygame.image.load('./assets/img_4/icons/coin.png')
gun_img = pygame.image.load('./assets/img_4/gun.png')
exp_img = pygame.image.load('./assets/img_4/explosion/exp2.png')
exp_img = pygame.transform.scale(exp_img, (320, 320))
intro_sign = pygame.image.load('./assets/img_4/intro_sign.png')
intro_sign = pygame.transform.scale(intro_sign, (428, 132))

item_boxes = {
    'Health'    : health_box_img,
    'Ammo'      :ammo_box_img,
    'Grenade'   :grenade_box_img,
    'Coin'      :coin_img
}
pine1_img = pygame.image.load('./assets/img_4/bg/pine1.png')
pine2_img = pygame.image.load('./assets/img_4/bg/pine2.png')
mountain_img = pygame.image.load('./assets/img_4/bg/mountain.png')
sky_img = pygame.image.load('./assets/img_4/bg/sky_cloud.png')


#buttons
start_img = pygame.image.load('./assets/img_4/start_btn.png')
exit_img = pygame.image.load('./assets/img_4/exit_btn.png')
restart_img = pygame.image.load('./assets/img_4/restart_btn.png')


#load music and sounds
grenade_fx = pygame.mixer.Sound('./assets/sounds/audio_grenade.wav')
grenade_fx.set_volume(0.005)
jump_fx = pygame.mixer.Sound('./assets/sounds/audio_jump.wav')
jump_fx.set_volume(0.0019)
shot_fx = pygame.mixer.Sound('./assets/sounds/audio_shot.wav')
shot_fx.set_volume(0.005)
coin_fx = pygame.mixer.Sound('./assets/sounds/coin.wav') 

#bg music
pygame.mixer.music.load('./assets/sounds/audio_music2.mp3')
pygame.mixer.music.set_volume(0.23)
pygame.mixer.music.play(-1, 0.0, 5000)

#game variables
moving_left = False
moving_right = False
bg = (127, 127, 127)
grey = (127, 127, 127)
red = (255,0,0)
white = (255, 255, 255)
green = (0, 255, 0)
black = (0,0,0)
font = pygame.font.SysFont('Futura', 30)
font2 = pygame.font.SysFont('Futura', 100)
GRAVITY = 0.75
shoot = False
grenade = False
grenade_thrown = False
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 1
SCROLL_THRESH = 350
screen_scroll = 0
bg_scroll = 0
start_game = False
MAX_LEVELS = 5 
score = 0
pink = (235, 65, 54)
crimson = (117, 1, 1)
start_intro = False

#load the tile images
img_list = []
for i in range(22):
    img = pygame.image.load(f'./assets/img_4/tile/{i}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

def reset_level():
    global score
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    enemy_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    
    return data

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_img(img, x, y):
    img = img
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(bg)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.shoot_cooldown = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)

        #load all images for the players
        animation_types = ['idle', 'run', 'jump', 'death']
        for animation in animation_types:
            #reset temp_list of images
            temp_list = []
            #count number of files in folder
            num_of_frames = len(os.listdir(f'./assets/img_4/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'./assets/img_4/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.check_alive()
        self.update_animation()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        screen_scroll = 0
        #reset moving variables
        dx = 0
        dy = 0

		#assign moving variables
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check for collsion
        for tile in world.obstacle_list:
            #check for collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #if the ai has hit a wal, make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0

            #check for collsion in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the grounf ie. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the grounf ie. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
                    self.in_air = False

        #check for collison with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        #check for collison with end sign
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        #check if player has walked off the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        #update rect position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player pos
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.70 *self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
            shot_fx.play()

    def ai(self):
        if self.alive and player.alive:
            if random.randint(1, 350) == 1 and self.idling == False:
                self.idling = True
                self.update_action(0)
                self.idling_counter = 50
            #check if the ai is near the player
            if self.vision.colliderect(player.rect):
                #stop running and face th player
                self.update_action(0)
                #shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    #update ai vision with movement
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1

                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
        #scroll
        self.rect.x += screen_scroll


    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #move the bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        #check if bullet has gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        #check collison with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:    
                player.health -= 5            
                self.kill()

        #check for collsion with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:  
                    enemy.health -= 25          
                    self.kill()

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        global player, health_bar
        self.level_length = len(data[0])
        #iterate through each value in data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile == 11:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 13:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 12:
                        self.obstacle_list.append(tile_data)
                    elif tile == 15:
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5, 25, 10)
                        health_bar = HealthBar(55, 19, player.health, player.max_health)
                    elif tile == 16:
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 25, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 21:
                        item_box = ItemBox('Coin', x * TILE_SIZE - 5, y * TILE_SIZE - 15)
                        item_box_group.add(item_box)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        global score
        #scroll
        self.rect.x += screen_scroll

        #check if player has collected the box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 20
            elif self.item_type == 'Grenade':
                player.grenades += 3
            elif self.item_type == 'Coin':
                score += 1
                coin_fx.play()

            self.kill()

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

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        #check for collsion with level
        for tile in world.obstacle_list:
            #check with collsion with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= 1
                dx = self.direction * self.speed
            #check for collsion in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                #check if below the grounf ie. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the grounf ie. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        #update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        #countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, 0.75)
            explosion_group.add(explosion)
            #do damage to anyone nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 40
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50
                    print(enemy.health)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'./assets/img_4/explosion/exp{num}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLOSION_SPEED = 4
        #update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1

            if self.frame_index >= len(self.images):
                self.kill()

            else:
                self.image = self.images[self.frame_index]

class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed

        if self.direction == 1: #whole screen fade
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))         
        if self.direction == 2: #vertical screen fade down
            pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.direction == 3: #end screen fade
            pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
            
        return fade_complete

#create screen fades
intro_fade = ScreenFade(1, black, 4)
death_fade = ScreenFade(2, crimson, 4)
end_fade = ScreenFade(2, black, 4)

#create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 35, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 80, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

#sprite groups
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
#load in level data an create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player, health_bar = world.process_data(world_data)


run = True
while run:
    clock.tick(fps)

    #load/create highscore
    try:
        with open('high_score.dat', 'rb') as file:
            highscore = pickle.load(file)

    except:
        highscore = 0

    #main menu
    if start_game == False:
        screen.fill(grey)
        draw_img(exp_img, SCREEN_WIDTH // 2 - 155, SCREEN_HEIGHT // 2 - 360)
        draw_img(intro_sign, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 280)
        draw_text(f'Highscore: {highscore}', font, white, SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 60)
        if start_button.draw(screen):
            start_game = True
            start_intro = True

        if exit_button.draw(screen):
            run = False

    else:

        #background
        draw_bg()

        #draw world map
        world.draw()


        #show grenades
        draw_img(grenade_box_img, 10, 57)
        draw_text(f'{player.grenades}', font, white, 54, 65)
        #show health
        draw_img(health_box_img, 10, 10)
        health_bar.draw(player.health)
        #draw_text(f'{player.health}', font, white, 54, 114)
        #show ammo
        draw_img(ammo_box_img, 10, 107)
        draw_text(f'{player.ammo}', font, white, 54, 114)
        #show score
        draw_text(f'Score: {score}', font, white, 700, 10)


        player.update()
        player.draw()

        #update and draw groups
        bullet_group.update()
        bullet_group.draw(screen)
        grenade_group.update()
        grenade_group.draw(screen)
        explosion_group.update()
        explosion_group.draw(screen)
        item_box_group.update()
        item_box_group.draw(screen)
        decoration_group.update()
        decoration_group.draw(screen)
        water_group.update()
        water_group.draw(screen)
        exit_group.update()
        exit_group.draw(screen)
        
        
        for enemy in enemy_group:
            enemy.ai()
            enemy.update()
            enemy.draw()

        #show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        #update player actions
        if player.alive:
            if shoot:
                player.shoot()
            elif grenade == True and grenade_thrown == False and player.grenades > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                            player.rect.top, player.direction)
                grenade_group.add(grenade)
                grenade_thrown = True
                player.grenades -= 1

            if player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1)
            else: 
                player.update_action(0)
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            #check if player has completed the level
            if level_complete:
                start_intro = True
                level += 1
                print(level)
                bg_scroll = 0
                world_data = reset_level()
                if level < MAX_LEVELS:
                    #load in level data an create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

                    world = World()
                    player, health_bar = world.process_data(world_data)

                elif level >= MAX_LEVELS:
                    if end_fade.fade():
                        draw_text('VICTORY', font2, crimson, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 280)
                        if restart_button.draw(screen):
                            end_fade.fade_counter = 0
                            level = 1
                            #start_intro = True
                            bg_scroll = 0
                            score = 0
                            world_data = reset_level()
                            #load in level data an create world
                            with open(f'level{level}_data.csv', newline='') as csvfile:
                                reader = csv.reader(csvfile, delimiter=',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)

                            world = World()
                            player, health_bar = world.process_data(world_data)

                        if exit_button.draw(screen):
                            run = False


        #if player has died
        if player.alive == False:
            screen_scroll = 0
            if score > highscore:
                highscore = score
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    score = 0
                    world_data = reset_level()
                    #load in level data an create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

                    world = World()
                    player, health_bar = world.process_data(world_data)

    with open('high_score.dat', 'wb') as file:
        pickle.dump(highscore, file)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and player.alive:
                moving_left = True
            if event.key == pygame.K_d and player.alive:
                moving_right = True
            if event.key == pygame.K_q and player.alive:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_SPACE and player.alive:
                shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()