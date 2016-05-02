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


fontSprite = None
fontCharList = []
fontWidth = 8
fontHeight = 8

def init():
	global fontSprite
	global fontCharList
	
	fontSprite = Sprite("img/font.png", 16,16)	
	fontCharList = [None] * (16*16)
	
	for y in range(0,16):
		for x in range(0,16):
			c = y*16 + x			
			fontCharList[c] = fontSprite.get(0,0, frame=c)[0].copy()
			
def drawChar(surf, c, x,y):
	surf.blit(fontCharList[ord(c)], (x,y, fontWidth,fontHeight))
	pass
	
def drawText(surf, txt, x,y):
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
