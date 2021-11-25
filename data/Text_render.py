"""
This is a pygame Text renderer
Created on: 25-09-2021
Time: 10:26:35
"""
import random
import sys
from typing import List, Tuple

import pygame

text_order = ['A',
              'B',
              'C',
              'D',
              'E',
              'F',
              'G',
              'H',
              'I',
              'J',
              'K',
              'L',
              'M',
              'N',
              'O',
              'P',
              'Q',
              'R',
              'S',
              'T',
              'U',
              'V',
              'W',
              'X',
              'Y',
              'Z',

              'a',
              'b',
              'c',
              'd',
              'e',
              'f',
              'g',
              'h',
              'i',
              'j',
              'k',
              'l',
              'm',
              'n',
              'o',
              'p',
              'q',
              'r',
              's',
              't',
              'u',
              'v',
              'w',
              'x',
              'y',
              'z'

              ]


# text_order = [
#     'A',
#     'B',
#     'C',
#     'D',
#     'E'
# ]

# print(len(text_order))


class Vector2(pygame.math.Vector2):
    def to_int(self) -> Tuple[float, float]:
        if type(self.x) == pygame.math.Vector2 or type(self.y) == pygame.math.Vector2:
            raise Exception(f"Non Integer to Convert: expected int, got {type(self)} instead.")
        return int(self.x), int(self.y)


class TextAnimator:

    def __init__(self, loc: Vector2, string: str, color, blink_timer, font: pygame.font or pygame.font.SysFont,
                 font_animation_timer=15,mistakes = True):
        self.pos = loc
        self.color = color
        self.original_blink_timer = blink_timer
        self.blink_timer = self.original_blink_timer
        self.line = False

        self.font_anim = [string[:x + 1] for x, s in enumerate(string)]
        self.font = font
        self.original_font_animation_timer = font_animation_timer
        self.font_animation_timer = self.original_font_animation_timer
        self.index = 0

        for x, s in enumerate(self.font_anim):
            var = random.choice([False, False,False,False, False, False, False, mistakes])
            if var:
                s2 = random.choice(text_order)
                self.font_anim.insert(x, s + s2)
                self.font_anim.insert(x, s)

    def set_text_animation(self, animation: list):
        self.font_anim = animation

    def render(self, win):
        t1 = self.font.render(self.font_anim[self.index], True, self.color)
        win.blit(t1, self.pos.to_int())

        t2 = self.font.render("|" if self.line else "", True, self.color)
        win.blit(t2, (self.pos[0] + t1.get_width(), self.pos[1] - 2))

    def change_text(self, new_text):
        self.text = new_text

    def update(self):
        print(self.font_anim)

        self.blink_timer -= 1
        self.font_animation_timer -= 1
        if self.blink_timer <= 0:
            self.line = not self.line
            self.blink_timer = self.original_blink_timer
        if self.font_animation_timer <= 0:
            self.font_animation_timer = self.original_font_animation_timer
            self.index += 1 if self.index < len(self.font_anim) - 1 else 0


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

# ********************************************************
FONT = pygame.font.SysFont("Roberto", 35)

images: List[pygame.Surface] = [
    FONT.render(x, True, COLOR_WHITE) for x in text_order]

text = {
}
for i in range(len(images)):
    text[text_order[i]] = images[i]

# *****************-- SystemCore Variables --*************
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('pygame Text renderer')
clock = pygame.time.Clock()

# t.set_text_animation(
t = TextAnimator(Vector2(50, 50), "The quick brown fox jumps over the lazy dog.", COLOR_WHITE, 40, FONT, font_animation_timer=5)


#     [
#         "A",
#         "AB",
#         "ABC",
#         "AB",
#         "ABD"
#     ]
# )

def this(this='', is_equal_to=''):
    return this == is_equal_to


# ********************************************************

def render_font2(string):
    length_of_text = len(text) * images[0].get_width()
    # width_of_letter = images[0].get_width()
    height_of_letter = images[0].get_height()

    w = False
    a = False

    s = pygame.Surface((length_of_text, height_of_letter))
    for x, letter in enumerate(string):
        width_of_letter = images[x].get_width() - 2

        coor_x = x * width_of_letter

        try:
            if string[x - 1] == 'M' or string[x - 1] == 'W':
                coor_x += 8
                w = True
            elif string[x + 1] == 'A' or string[x - 1] == 'A':
                coor_x += 2
                a = True
            else:
                if w:
                    coor_x += 8
                elif a:
                    coor_x += 4


        except IndexError:
            pass
            # s.blit(text[letter], (x * width_of_letter  , 0))
        if not x == 0: coor_x -= x * 3
        s.blit(text[letter], (coor_x, 0))

        # coor_x

    s.set_colorkey((0, 0, 0))
    return s


def render_font(string):
    length_of_text = len(text) * images[0].get_width()
    height_of_letter = images[0].get_height()

    s = pygame.Surface((length_of_text, height_of_letter))
    # c = 0
    px = 0

    for x, letter in enumerate(string):
        width_of_letter = text[letter].get_width()
        c = px + width_of_letter
        print(c, px, width_of_letter)
        px = c

        px += 2

        # print(x, width_of_letter, coor_x, letter)
        # try:
        #     if this(string[x+1],is_equal_to='E'):
        #         px += 5
        # except IndexError:
        #     pass
        # if letter == 'E' or letter == 'G':
        #     pygame.draw.circle(s,COLOR_RED,(c,0),1)
        #     pygame.draw.circle(s,COLOR_GREEN,(c+width_of_letter,0),1)

        s.blit(text[letter], (c, 0))

    s.set_colorkey((0, 0, 0))
    return s


timer = 30
line = False


def draw_window():
    global timer, line
    screen.fill(COLOR_DARK_GRAY)
    px = 0
    # for x, i in enumerate(text_order):
    #     c = px + text[i].get_width() + 8
    #
    #     screen.blit(text[i], (x + c, 50))
    #     px = c
    # screen.blit(text[''],(10,10))

    # timer -= 1
    # if timer <= 0:
    #     line = not line
    #     timer = 30
    #
    # t1 = FONT.render(f"ABC", True, COLOR_WHITE)
    # screen.blit(t1, (10, 10))
    # t = FONT.render(f"|" if line else "", True, COLOR_WHITE)
    # screen.blit(t, (t1.get_width() + 10, 8))

    t.render(screen)

    # screen.blit(render_font('PRATHAMESH'), (10, 10))

    # for x, i in enumerate(text_order):
    # t = FONT.render('ABCDEFGHIJKLMNOPQRSTUVWXYZ',False,COLOR_WHITE)
    # print(t.get_width(),i)
    # screen.blit(t,(x*20,400))
    # # for x, i in enumerate(text_order):
    # t = FONT.render('ABCDEFGHIJKLMNOPQRSTUVWXYZ', True, COLOR_WHITE)
    # print(t.get_width(), i)
    # screen.blit(t, (x * 20, 500))

    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN :
            # t.set_text_animation(
            #     ['Scrore']
            # )
    t.update()
    draw_window()
    # break
    clock.tick(FPS)
