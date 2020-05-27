# Sprites for Flappy bird

# Importing the libraries
import pygame as pg
from conf import *


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        image = 'gallery/sprites/bird.png'
        self.image_org = pg.image.load(image).convert_alpha()
        self.image = self.image_org.copy()
        self.x = WIDTH / 5
        self.y = HEIGHT * 0.25
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.hitbox = pg.Rect(0, 0, 34, 24)
        self.hitbox.center = (self.x, self.y)
        self.vel = -9
        self.rot_speed = ROTATE * -self.vel
        self.max_vel = 10
        self.min_vel = -8
        self.acc = 0
        self.flapped = False
        self.rot = 0
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > DELAY:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_org, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        # Player Flying Mechanics
        if self.vel < self.max_vel and not self.flapped:
            self.vel += GRAVITY
            self.rot_speed = -self.vel * ROTATE
        if self.flapped:
            self.flapped = False
        self.y += self.vel
        self.rect.center = (self.x, self.y)
        self.hitbox.center = (self.x, self.y)
        if 45 < self.rot < 180:
            self.rot = 45
        if 180 < self.rot < 270:
            self.rot = 270

        self.rotate()


class Pipe(pg.sprite.Sprite):
    def __init__(self, state, gp_ht):  # state specifies whether the Pipe comes from the top or bottom
        pg.sprite.Sprite.__init__(self)  # gp_ht specifies the location of the gap
        self.state = state
        self.gp_ht = gp_ht
        if self.state == 't':
            image = 'gallery/sprites/pipe_top.png'
            self.image = pg.image.load(image).convert_alpha()
            self.x = SPAWN
            self.rect = self.image.get_rect()
            self.rect.bottom = self.gp_ht
            self.rect.right = self.x
        elif self.state == 'b':
            image = 'gallery/sprites/pipe_bottom.png'
            self.image = pg.image.load(image).convert_alpha()
            self.x = SPAWN
            self.rect = self.image.get_rect()
            self.rect.top = self.gp_ht + GAP
            self.rect.right = SPAWN

    def update(self):
        if self.state == 't':
            self.rect.bottom = self.gp_ht
        elif self.state == 'b':
            self.rect.top = self.gp_ht + GAP
        self.rect.right = self.x
