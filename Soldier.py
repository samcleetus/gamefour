class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        img = pygame.image.load('./assets/img_4/player/idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def move(self, moving_left, moving_right):
        #reset moving variables
        dx = 0
        dy = 0

		#assign moving variables
        if moving_left:
            dx = -self.speed
        if moving_right:
            dy = self.speed

        #update rect position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(self.image, self.rect)