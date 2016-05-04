import sys
import os
import pygame
import math
import time
import random
from pygame.locals				import *
from src						import *
from drawable					import *
from deathstar					import *
from earth						import *
from player						import *
from earthchunk					import *
from sprite						import *
from math2						import *
from explosion					import *
from mat						import *
from skybox						import *
from arwing						import *
from arwing_player				import *
from twisted.internet.protocol	import Protocol, ClientFactory, Factory
from twisted.internet.task 		import LoopingCall
from twisted.internet			import reactor
from twisted.protocols.basic	import LineReceiver
from twisted.internet.tcp		import Port
from sys						import *
from radar						import *
import json


FONT_WHITE = 0
FONT_BLACK = 1
FONT_RED = 2
FONT_GREEN = 3
FONT_BLUE = 4
FONT_YELLOW = 5
FONT_CYAN = 6
FONT_MAGENTA = 7

fontSprite = None
fontCharList = None
subCharList = None
fontWidth = 8
fontHeight = 8

def init():
	global fontSprite
	global fontCharList
	
	fontSprite = Sprite("img/font.png", 16,16)	
	
	# Create list of lists to store each letter in a different color
	fontCharList = []
	for i in range(0,8):
		fontCharList.append( [None] * (16*16) )	
	
	for y in range(0,16):
		for x in range(0,16):
			c = y*16 + x
			
			white = fontCharList[FONT_WHITE][c] = fontSprite.get(0,0, frame=c)[0].copy()			
			
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
			
def drawChar(surf, c, x,y):
	surf.blit(subCharList[ord(c)], (x,y, fontWidth,fontHeight))
	pass

	
def drawText(surf, txt, x,y, color=FONT_WHITE):
	global subCharList
	subCharList = fontCharList[color]
	
	oriX = x
	
	for c in txt:	
		if c == '\n':
			x = oriX
			y += fontHeight
		elif c == ' ':
			x += fontWidth
		else:
			drawChar(surf, c, x,y)
			x += fontWidth

def drawTextShadow(surf, txt, x,y, color=FONT_WHITE):
	drawText(surf, txt, x+2,y+1, FONT_BLACK);
	drawText(surf, txt, x,y, color);