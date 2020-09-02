# Author: Guillermo Ochoa
# Last update: 30/09/2016 dd/mm/yyyy

#  V 0.4 disparos y misiles dirigidos

# Para colisiones self.rect.colliderect(other.rect)

import math, pygame, os, sys
from random import randint
from pygame.locals import *

WIDTH = 1366
HEIGHT = 768


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
    return image

class Boyfriend(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("player.png", -1)
        self.walk = []
        self.walk.append(load_image("player.png", -1))
        self.walk.append(load_image("walk.png", -1))
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y

        # actions
        self.left = False
        self.right = False

        # Animation
        self.counter = 0

    def update(self):

        if self.rect.x > WIDTH + 30:
            self.rect.x = -19
        if self.rect.x <= -20:
            self.rect.x = WIDTH + 29
        if self.left:
            self.rect.x -= 6
        if self.right:
            self.rect.x += 6

        if self.left or self.right:
            if self.counter == 20:
                self.image = self.walk[0]
                self.counter = 0

            elif self.counter == 10:
                self.image = self.walk[1]

            self.counter += 1

        else:
            self.image = self.walk[0]
            self.counter = 5


class Arm(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        pygame.sprite.Sprite.__init__(self)
        self.arms = []
        self.arms.append(load_image("fire.png", -1))
        self.arms.append(load_image("arm.png", -1))
        self.image = self.arms[0]
        self.rect = self.image.get_rect(center=(init_x, init_y))
        self.ANG = 0
        self.firing = False
        # Animation
        self.index = 0
        self.counter = 0

    def update(self):
        if self.firing:
            if self.counter == 10:
                self.index = 0
                self.counter = 0

            elif self.counter == 5:
                self.index = 1

            self.counter += 1
        if not self.firing:
            self.index = 0

        mouse_pos = pygame.mouse.get_pos()
        dy = self.rect.y - mouse_pos[1]
        dx = self.rect.x - mouse_pos[0]
        self.ANG = math.atan2(-dy, dx) * (180 / math.pi) + 180
        self.image = pygame.transform.rotate(self.arms[self.index], self.ANG)
        self.rect = self.image.get_rect(center=self.rect.center)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y, angle=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bullet.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
        self.bulletSpeed = 10
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.x += math.cos(math.radians(self.angle)) * self.bulletSpeed
        self.rect.y += -math.sin(math.radians(self.angle)) * self.bulletSpeed


class Missile(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y, ang):
        pygame.sprite.Sprite.__init__(self)
        self.destroyed = False
        self.image = load_image("missile.png", -1)
        self.rect = self.image.get_rect()
        self.rect.centerx = init_x
        self.rect.centery = init_y
        self.health = 100
        self.angle = ang
        self.image = pygame.transform.rotate(self.image, math.degrees(self.angle) + 90)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.speed = 5

    def update(self):
        self.rect.centerx += math.cos(self.angle) * self.speed
        self.rect.centery -= math.sin(self.angle) * self.speed


class Explotion(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(load_image("b1.png", -1))
        self.images.append(load_image("b2.png", -1))
        self.images.append(load_image("b3.png", -1))
        self.images.append(load_image("b4.png", -1))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = init_x - 70
        self.rect.y = init_y - 10
        self.counter = 0

    def update(self):
        if self.index == len(self.images):
            self.kill()
        else:
            if self.counter == 3:
                self.image = self.images[self.index]
                self.index += 1
                self.counter = 0
            self.counter += 1


def main():
    # initialize
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 32)
    pygame.display.set_caption("Missiles4u")
    pygame.display.flip()
    clock = pygame.time.Clock()
    spawn_time = 150
    firing = False
    next_shot = 0

    # background
    background = pygame.Surface(screen.get_size())
    background.fill((74, 107, 138))
    screen.blit(background, (0, 0))

    # content
    player = Boyfriend(WIDTH / 2, HEIGHT - 100)
    arm = Arm(WIDTH / 2, HEIGHT - 100)
    missiles = pygame.sprite.Group()
    explotions = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # loop
    while 1:
        clock.tick(60)

        # Event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                firing = True
                arm.firing = True
            elif event.type == MOUSEBUTTONUP:
                firing = False
                arm.firing = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_a:
                    player.left = True
                elif event.key == K_d:
                    player.right = True

            elif event.type == KEYUP:
                if event.key == K_a:
                    player.left = False
                    arm.left = False
                elif event.key == K_d:
                    player.right = False
                    arm.right = False

        # Handle Sprites
        arm.rect.center = player.rect.x, player.rect.y + 28
        spawn_time -= 1
        if spawn_time <= 0:
            mx = randint(1, WIDTH)
            my = 100
            dy = my - player.rect.centery
            dx = mx - player.rect.centerx
            ANG = math.atan2(dy, -dx)
            missiles.add(Missile(mx, my, ANG))
            spawn_time = 100

        for missile in missiles:
            if missile.rect.y >= 550:
                missile.destroyed = True
            for i in pygame.sprite.spritecollide(missile, bullets, True):
                missile.health -= 25
            if missile.destroyed or missile.health <= 0:
                explotions.add(Explotion(missile.rect.x, missile.rect.y))
                missiles.remove(missile)

        for bullet in bullets:
            if bullet.rect.x < 0 or bullet.rect.x >= WIDTH or bullet.rect.y < 0 or bullet.rect.y >= HEIGHT:
                bullets.remove(bullet)

        # EVENTS
        if firing:
            if next_shot <= 0:
                bullets.add(Bullet(arm.rect.centerx + 50 * math.cos(math.radians(arm.ANG)),
                                   arm.rect.centery - 50 * math.sin(math.radians(arm.ANG)), arm.ANG))
                next_shot = 10
            next_shot -= 1

        # Draw EEERRRRYTHING
        screen.blit(background, (0, 0))

        arm.update()
        player.update()
        bullets.update()
        missiles.update()
        explotions.update()

        missiles.draw(screen)
        bullets.draw(screen)
        explotions.draw(screen)
        screen.blit(player.image, player.rect.topleft)
        screen.blit(arm.image, arm.rect.topleft)
        pygame.display.update()


if __name__ == '__main__': main()