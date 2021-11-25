"""
This is a Team Seas Game jam Entry
Created on: 14:11:2021
Time: 02:28:50 PM
"""

import pygame
import sys
from pygame.image import load
from pygame.math import Vector2
import random
import math
# from data.Text_render import TextAnimator


class Wind:
    def __init__(self, vel):

        self.lines = []
        if vel < 0:
            for a in range(20):
                f = random.randint(0, screenHeight)
                x = random.randint(0, 1000)
                self.lines.append([[screenWidth+x, f], [screenWidth+x, f]])
        else:
            for a in range(20):
                f = random.randint(0, screenHeight)
                x = random.randint(0, 1000)
                self.lines.append([[-x, f], [-x, f]])
        self.vel = vel
        self.max_len = 150
        self.x = 0

    def length(self, l):
        # length = math.hypot(intersection[0] - self.rect.center[0], intersection[1] - self.rect.center[1])
        return math.hypot(l[0][0]-l[1][0], l[0][1]-l[1][1])

    def update(self):
        self.x += 1
        if self.x >= 15:
            self.vel += -2 if self.vel < 0 else 2
            self.x = 0
        r = []
        if self.vel < 0:
            for l in self.lines:
                l[1][0] += self.vel
                if self.length(l) >= self.max_len:
                    l[0][0] += self.vel
                if l[0][0] <= 0:
                    r.append(l)
            for v in r:
                self.lines.remove(v)
                f = random.randint(0, screenHeight)
                x = random.randint(0, 100)
                self.lines.append([[screenWidth+x, f], [screenWidth+x, f]])
        else:
            for l in self.lines:
                l[1][0] += self.vel
                if self.length(l) >= self.max_len:
                    l[0][0] += self.vel
                if l[0][0] >= screenWidth:
                    r.append(l)
            for v in r:
                self.lines.remove(v)
                f = random.randint(0, screenHeight)
                x = random.randint(0, 100)
                self.lines.append([[-x, f], [-x, f]])

    def draw(self, win):
        for l in self.lines:
            pygame.draw.line(win, COLOR_WHITE, l[0], l[1], 1)


class Trash:
    def __init__(self, x, y, img):
        img = load(img).convert_alpha()
        self.img = img

        self.img = pygame.transform.rotozoom(
            self.img, random.randint(0, 360), 1)

        self.img2 = self.img.convert()

        darken_percent = .8
        self.dark = pygame.Surface(self.img2.get_size()).convert_alpha()

        self.dark.fill((0, 0, 0, darken_percent*255))

        self.img2.blit(self.dark, (0, 0))
        self.img2.set_colorkey((0, 0, 0))
        # self.img.set_colorkey((0, 0, 0))

        self.pos = [x, y]
        self.acc = [0, 0]
        self.vel = [0, 0]

    def to_tuple(self, l):
        return int(l[0]), int(l[1])

    def draw(self):
        # screen.blit(self.img2, (self.pos[0]-4, self.pos[1]+5))
        screen.blit(self.img, (self.pos[0], self.pos[1]))
        # screen.blit(self.dark, (0,0))
        # pygame.draw.circle(screen, COLOR_GREEN, self.to_tuple(self.pos), 10)
        # pygame.draw.circle(screen, COLOR_BLUE, (self.pos[0], self.pos[1]), 10)

    def collisions(self, trash):
        pass
        # for t in trash:

        #     x, y = t.pos
        #     w, h = 32, 32
        #     r = pygame.Rect(x,y,w,h)

        #     x2, y2 = self.pos
        #     w2, h2 = 32, 32
        #     r2 = pygame.Rect(x2,y2,w2,h2)

        #     if r.colliderect(r2):

        #         if abs(r.top - r2.bottom) <= 2: r.top = r.bottom
        #         if abs(r.bottom - r2.top) <= 2: r.bottom = r2.top
        #         if abs(r.right - r2.left) <= 2: r.right = r2.left
        #         if abs(r.left - r2.right) <= 2: r.left = r2.right

        #         t.pos = (r.x,r.y)
        #         self.pos = (r2.x,r2.y)

    def add(self, a, b):
        return [a[0]+b[0], a[1]+b[1]]

    def update(self):

        # self.collisions(trash)
        self.pos = self.add(self.pos, self.vel)
        self.vel = self.add(self.vel, self.acc)

        x, y = self.pos
        if x <= 0:
            self.acc = [0, 0]
            # self.vel = [0,0]
            x = 0
        if x+self.img.get_width() >= screenWidth:
            self.acc = [0, 0]
            # self.vel = [0,0]
            x = screenWidth - self.img.get_width()
        if y <= 0:
            self.acc = [0, 0]
            # self.vel = [0,0]
            y = 0
        if y+self.img.get_height() >= screenHeight:
            self.acc = [0, 0]
            # self.vel = [0,0]
            y = screenHeight - self.img.get_height()

        self.pos = [x, y]

        d = .2
        if self.vel[0] != 0:
            if self.vel[0] > 0:
                self.vel[0] -= d
            if self.vel[0] < 0:
                self.vel[0] += d
        if self.vel[1] != 0:
            if self.vel[1] < 0:
                self.vel[1] += d
            if self.vel[1] > 0:
                self.vel[1] -= d


class Player:
    def __init__(self):
        self.direction = pygame.math.Vector2(0, 0)
        self.vel = .5
        #               images, ind, timmer, ori timmer
        self.player_up_anim_data = [[], 0, 0,    7]
        self.player_down_anim_data = [[], 0, 0,  7]
        self.player_left_anim_data = [[], 0, 0,  7]
        self.player_right_anim_data = [[], 0, 0, 7]

        self.images = 0
        self.ind = 1
        self.timer = 2
        self.ori_timer = 3

        self.max_i = 15

        ss = pygame.image.load('data/images/player/p_up.png').convert_alpha()

        self.w, self.h = 32*3, 32*3
        for x in range(self.max_i):
            x *= 32
            cropped = (x, 0, x + 32, 32)
            s = pygame.Surface((32, 32))
            print(cropped)

            s.blit(ss, (0, 0), cropped)
            s.set_colorkey((0, 0, 0))
            s = pygame.transform.scale(s, (self.w, self.h))

            self.player_up_anim_data[0].append(s)
        ss = pygame.image.load('data/images/player/p_down.png').convert_alpha()
        for x in range(self.max_i):
            x *= 32
            cropped = (x, 0, x + 32, 32)
            s = pygame.Surface((32, 32))
            print(cropped)

            s.blit(ss, (0, 0), cropped)
            s.set_colorkey((0, 0, 0))
            s = pygame.transform.scale(s, (self.w, self.h))

            self.player_down_anim_data[0].append(s)
        ss = pygame.image.load('data/images/player/p_left.png').convert_alpha()
        for x in range(self.max_i):
            x *= 32
            cropped = (x, 0, x + 32, 32)
            s = pygame.Surface((32, 32))
            print(cropped)

            s.blit(ss, (0, 0), cropped)
            s.set_colorkey((0, 0, 0))
            s = pygame.transform.scale(s, (self.w, self.h))

            self.player_left_anim_data[0].append(s)
        ss = pygame.image.load(
            'data/images/player/p_right.png').convert_alpha()
        for x in range(self.max_i):
            x *= 32
            cropped = (x, 0, x + 32, 32)
            s = pygame.Surface((32, 32))
            print(cropped)

            s.blit(ss, (0, 0), cropped)
            s.set_colorkey((0, 0, 0))
            s = pygame.transform.scale(s, (self.w, self.h))

            self.player_right_anim_data[0].append(s)
        self.current_image = self.player_up_anim_data[self.images][0]

    def get_dir(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction[0] = -self.vel
            if event.key == pygame.K_RIGHT:
                self.direction[0] = self.vel
            if event.key == pygame.K_UP:
                self.direction[1] = -self.vel
            if event.key == pygame.K_DOWN:
                self.direction[1] = self.vel
        if event.type == pygame.KEYUP:
            self.direction = Vector2(0, 0)

    def draw(self):
        screen.blit(self.current_image, (10, screenHeight -
                    (self.current_image.get_height()+10)))

    def update(self, trash):
        if self.direction.x < 0:
            self.player_left_anim_data[self.timer] -= 1

            if self.player_left_anim_data[self.timer] <= 0:
                self.player_left_anim_data[self.ind] += 1
                self.player_left_anim_data[self.timer] = self.player_left_anim_data[self.ori_timer]
                if not self.player_left_anim_data[self.ind] <= len(
                        self.player_left_anim_data[self.images]):
                    self.player_left_anim_data[self.ind] = 0

                self.current_image = self.player_left_anim_data[self.images][
                    self.player_left_anim_data[self.ind] - 1]
        elif self.direction.x > 0:
            self.player_right_anim_data[self.timer] -= 1

            if self.player_right_anim_data[self.timer] <= 0:
                self.player_right_anim_data[self.ind] += 1
                self.player_right_anim_data[self.timer] = self.player_right_anim_data[self.ori_timer]
                if not self.player_right_anim_data[self.ind] <= len(
                        self.player_right_anim_data[self.images]):
                    self.player_right_anim_data[self.ind] = 0

                self.current_image = self.player_right_anim_data[self.images][
                    self.player_right_anim_data[self.ind] - 1]

        elif self.direction.y > 0:

            self.player_down_anim_data[self.timer] -= 1

            if self.player_down_anim_data[self.timer] <= 0:
                self.player_down_anim_data[self.ind] += 1
                self.player_down_anim_data[self.timer] = self.player_down_anim_data[self.ori_timer]
                if not self.player_down_anim_data[self.ind] <= len(
                        self.player_down_anim_data[self.images]):
                    self.player_down_anim_data[self.ind] = 0

                self.current_image = self.player_down_anim_data[self.images][
                    self.player_down_anim_data[self.ind] - 1]
        elif self.direction.y <= 0:
            self.player_up_anim_data[self.timer] -= 1
            if self.player_up_anim_data[self.timer] <= 0:
                self.player_up_anim_data[self.ind] += 1
                self.player_up_anim_data[self.timer] = self.player_up_anim_data[self.ori_timer]
                if not self.player_up_anim_data[self.ind] <= len(
                        self.player_up_anim_data[self.images]):
                    self.player_up_anim_data[self.ind] = 0

                self.current_image = self.player_up_anim_data[self.images][
                    self.player_up_anim_data[self.ind] - 1]

        for t in trash:
            t.acc = [self.direction[0], self.direction[1]]
            # print(self.direction)


class Bucket:
    def __init__(self):
        # self.line1 = [(screenWidth//2-50, 0), (screenWidth//2-50, 10)]
        # self.line2 = [(screenWidth//2+50, 0), (screenWidth//2+50, 10)]

        self.r = pygame.Rect(screenWidth//2-50, 0, 100, 20)
        self.dir = -1

    def _reset(self):
        self.dir = -1

    def draw(self):
        if self.r.x <= 0:
            self.dir *= -1
        if self.r.right >= screenWidth:
            self.dir *= -1
        self.r.x += self.dir

        pygame.draw.line(screen, COLOR_RED, self.r.topleft,
                         self.r.bottomleft, 5)
        pygame.draw.line(screen, COLOR_RED, self.r.topright,
                         self.r.bottomright, 5)
        pygame.draw.line(screen, COLOR_RED, self.r.topright,
                         self.r.topleft, 5)
        # pygame.draw.rect(screen,COLOR_RED,self.r)

    def collisions(self, trash, score):
        to_remove = []
        for t in trash:
            if self.r.collidepoint(t.to_tuple(t.pos)):
                to_remove.append(t)
                score += 1
                point_m.play()

                self.dir += -1 if self.dir < 0 else 1

            if t.pos[1] <= 0:
                lose_m.play()
                to_remove.append(t)

        for x in to_remove:
            try:
                trash.remove(x)
            except ValueError:
                pass
        return trash, score


class Obstacles:
    def __init__(self):
        self.dificulty = "Easy"
        self.dificulty_list = [0, 1, 2, 3, 4, 5, 6, 4, 7, 8, 9,
                               10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        self.ind = 0
        self.pos_l = [pygame.Rect(random.randint(0, screenWidth), random.randint(
            0, screenHeight), 64, 64) for _ in range(self.dificulty_list[self.ind])]
        # load img from Res folder
        self.img = pygame.image.load('data/images/rock.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (64, 64))

    def _reset(self):
        self.ind += 1
        self.pos_l = [pygame.Rect(random.randint(0, screenWidth), random.randint(
            0, screenHeight), 64, 64) for _ in range(self.dificulty_list[self.ind])]

    def collisions(self, trash, score):
        to_remove = []
        for t in trash:
            r = pygame.Rect(t.pos[0], t.pos[1], 30, 30)
            for p in self.pos_l:
                if p.colliderect(r):
                    to_remove.append(t)
                    self.ind += 1
                    lose_m.play()

        for x in to_remove:
            try:
                trash.remove(x)
            except ValueError:
                pass
            score += 0
        return trash, score

    def draw(self, win):
        for p in self.pos_l:
            win.blit(self.img, p)
            # pygame.draw.rect(win, COLOR_BLUE, p)

# class Animator:
#     def __init__(self,pos,text):


def rand(n):
    return random.randint(0, n)


pygame.init()
# *****************-- Normal Variables --*****************
screenHeight = 600
screenWidth = 1000
FPS = 60

# Colour
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

COLOR_GRAY = (100, 100, 100)
COLOR_LIGHT_GRAY = (200, 200, 200)
COLOR_DARK_GRAY = (50, 50, 50)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

COLOR_YELLOW = (255, 255, 0)
COLOR_PINK = (255, 0, 255)


# *****************-- SystemCore Variables --*************
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Seas Game jam Entry')
clock = pygame.time.Clock()
# ********************************************************
b = ["coca cola.png", "pepsi.png", "soda.png", "soda half.png", "soda empty.png"]
trash = [Trash(rand(screenWidth), rand(screenHeight),
               f"data/images/{random.choice(b)}") for _ in range(10)]
player = Player()
b = Bucket()
o = Obstacles()
wind_r = Wind(7)
wind_l = Wind(-7)
g = pygame.image.load('data/images/bg.png').convert_alpha()
g = pygame.transform.scale(g, (64, 64))
bg = pygame.Surface((screenWidth, screenHeight))


point_m = pygame.mixer.Sound('data/sfx/gain.wav')
point_m.set_volume(.2)
lose_m = pygame.mixer.Sound('data/sfx/delete.wav')
lose_m.set_volume(.2)

score = 0
highest_score = 0
with open('data/score.txt') as f:
    highest_score = int(f.read())
# TextAnimator
FONT = pygame.font.Font("data/NOVACUT-REGULAR.TTF", 35)


for i in range(0, screenWidth, g.get_width()):
    for j in range(0, screenHeight, g.get_height()):
        bg.blit(g, (i, j))


def draw_text(pos, text):
    t = FONT.render(text, True, COLOR_WHITE)
    screen.blit(t, pos)


def draw_window():

    screen.fill((114, 200, 238))
    # screen.fill((255, 255, 255))
    # screen.blit(bg, (0, 0))
    player.draw()
    for t in trash:
        t.update()
        t.draw()
    o.draw(screen)
    b.draw()
    if player.direction.x < 0:
        wind_l.update()
        wind_l.draw(screen)
    if player.direction.x > 0:

        wind_r.draw(screen)
        wind_r.update()

    draw_text((10, 10), f"Highest Score:{highest_score}")
    draw_text((10, 45), f"Trash Collected:{score}")
    pygame.display.flip()


def home_screen():
    background = pygame.image.load(
        'data/images/Home screen/Web 1920 – 1.png').convert_alpha()
    music = pygame.mixer.Sound('data/sfx/entry music 3.wav')
    music.play(-1, fade_ms=5000)
    # music.fade_in(100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                music.stop()
                game_loop()

        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


def game_loop():
    global trash, score, highest_score
    music2 = pygame.mixer.Sound('data/sfx/bg_music.wav')
    music2.play(-1, fade_ms=5000)
    music2.set_volume(1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            player.get_dir(event)
        trash, score = b.collisions(trash, score)
        player.update(trash)
        trash, score = o.collisions(trash, score)

        if score > highest_score:
            highest_score = score

        if not trash:

            with open('data/score.txt', 'w') as f:
                f.write(str(highest_score))
            try:
                o._reset()
            except IndexError:
                pygame.mixer.Sound('data/sfx/press.wav').play()
                end_screen()
            b._reset()
            bc = ["coca cola.png", "pepsi.png", "soda.png",
                  "soda half.png", "soda empty.png"]

            trash = [Trash(rand(screenWidth), rand(screenHeight),
                           f"data/images/{random.choice(bc)}") for _ in range(10)]

        draw_window()
        clock.tick(FPS)


def end_screen():
    F = pygame.font.Font("data/NOVACUT-REGULAR.TTF", 61)
    # t_pos = (194, 273)
    # t_pos2 = (296, 341)
    t = F.render(f"Highest Score: {highest_score}", True, COLOR_WHITE)
    t2 = F.render(f"Highest Score: {highest_score}", True, COLOR_BLACK)
    t_blur = pygame.transform.smoothscale(pygame.transform.scale(
        t2, (t2.get_width() // 2, t2.get_height() // 2)), (t2.get_width(), t2.get_height()))
    F = pygame.font.Font("data/NOVACUT-REGULAR.TTF", 53)

    t2 = F.render(f"Current Score: {score}", True, COLOR_WHITE)
    t22 = F.render(f"Current Score: {score}", True, COLOR_BLACK)
    t_blur2 = pygame.transform.smoothscale(pygame.transform.scale(
        t22, (t22.get_width() // 2, t22.get_height() // 2)), (t22.get_width(), t22.get_height()))

    F = pygame.font.Font("data/SUPERMARIO256.TTF", 101)

    mt = F.render("GAME OVER", True, COLOR_BLACK)

    while True:
        screen.fill((114, 200, 238))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        x = (screenWidth//2) - (t.get_width()//2)
        screen.blit(t_blur, (x+1, 273+1))
        screen.blit(t, (x, 273))
        x = (screenWidth//2) - (t2.get_width()//2)

        screen.blit(t_blur2, (x+1, 341+1))
        screen.blit(t2, (x, 341))

        x = (screenWidth//2) - (mt.get_width()//2)

        screen.blit(mt, (x, 106))

        pygame.display.flip()
        clock.tick(FPS)


home_screen()
