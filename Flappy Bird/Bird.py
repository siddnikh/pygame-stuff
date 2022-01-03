import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0 #speed of animation

        for num in range(1 , 4):
            img = pygame.image.load(f'assets/bird{num}.png')
            self.images.append(img)
        
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.clicked = False
        self.vel = 0 #velocity
        self.flying = False
        self.game_over = False

    def update(self):

        if self.flying == True:
            #gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        #jump
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -9
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.game_over == False:
            #Animation handling
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0

            self.image = self.images[self.index]

            #Rotation of bird sprite
            self.image = pygame.transform.rotate(self.images[self.index], -2 * self.vel)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

    def reset(self, x, y):
        self.index = 0
        self.counter = 0
        self.rect.center = [x, y]
        self.clicked = False
        self.vel = 0
        self.flying = False
        self.game_over = False
        self.image = pygame.transform.rotate(self.images[0], 0)

        return 0