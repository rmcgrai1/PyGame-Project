#

import sys
import os
import pygame
import math
import time
import random
from pygame.locals				import *
from drawable					import *
from player						import *
from sprite						import *
from math2						import *
from mat						import *
from arwing						import *
from arwing_player				import *
from sys						import *

COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,255)

FONT_WHITE = 0
FONT_BLACK = 1
FONT_RED = 2
FONT_GREEN = 3
FONT_BLUE = 4
FONT_YELLOW = 5
FONT_CYAN = 6
FONT_MAGENTA = 7

SPR_FONT = None
SPR_HPBAR = None
fontCharList = None
subCharList = None
fontWidth = 8
fontHeight = 8

def init():
	global IMG_FONT
	global IMG_HPBAR
	global fontCharList
	global messageList
	
	
	SPR_FONT = Sprite("img/font.png", 16,16)
	SPR_HPBAR = Sprite("img/hpBar.png", 1,1)
	IMG_HPBAR = SPR_HPBAR.get(0,0)[0]
	
	# Create list of lists to store each letter in a different color
	fontCharList = []
	for i in range(0,8):
		fontCharList.append( [None] * (16*16) )	
	
	for y in range(0,16):
		for x in range(0,16):
			c = y*16 + x
			
			white = fontCharList[FONT_WHITE][c] = SPR_FONT.get(0,0, frame=c)[0].copy()			
			
			black = fontCharList[FONT_BLACK][c] = white.copy()
			black.fill((0,0,0,255), special_flags=BLEND_RGB_MULT)

			red = fontCharList[FONT_RED][c] = white.copy()
			red.fill((255,0,0,255), special_flags=BLEND_RGB_MULT)

			green = fontCharList[FONT_GREEN][c] = white.copy()
			green.fill((0,255,0,255), special_flags=BLEND_RGB_MULT)
			
			blue = fontCharList[FONT_BLUE][c] = white.copy()
			blue.fill((0,0,255,255), special_flags=BLEND_RGB_MULT)

			yellow = fontCharList[FONT_YELLOW][c] = white.copy()
			yellow.fill((255,255,0,255), special_flags=BLEND_RGB_MULT)
			
			magenta = fontCharList[FONT_MAGENTA][c] = white.copy()
			magenta.fill((255,0,255,255), special_flags=BLEND_RGB_MULT)
			
			cyan = fontCharList[FONT_CYAN][c] = white.copy()
			cyan.fill((0,255,255,255), special_flags=BLEND_RGB_MULT)
			
			
	subCharList = fontCharList[FONT_WHITE]
			
def drawChar(surf, c, x,y, xscale=1,yscale=1):
	img = subCharList[ord(c)]

	if xscale != 1 or yscale != 1:
		img = pygame.transform.smoothscale(img, (int(xscale*fontWidth),int(yscale*fontHeight)) )

	surf.blit(img, (x,y, fontWidth,fontHeight))
	pass

	
def drawText(surf, txt, x,y, color=FONT_WHITE, xscale=1,yscale=1):
	global subCharList
	subCharList = fontCharList[color]
	
	oriX = x
	
	for c in txt:	
		if c == '\n':
			x = oriX
			y += fontHeight*yscale
		elif c == ' ':
			x += fontWidth*xscale
		else:
			drawChar(surf, c, x,y, xscale, yscale)
			x += fontWidth*xscale

def drawTextShadow(surf, txt, x,y, color=FONT_WHITE, xscale=1,yscale=1):
	drawText(surf, txt, x+2,y+1, FONT_BLACK, xscale, yscale);
	drawText(surf, txt, x,y, color, xscale, yscale);
	
def drawHealthbar(surf, frac, x,y):
	surf.blit(IMG_HPBAR, (x+2,y+2), (0,0,192*contain(0,frac,1),19))
	pygame.draw.rect(surf, COLOR_WHITE, (x,y,195,20), 1)