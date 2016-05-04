# Jacob Kassman & Ryan McGrail
# hud.py
# Contains a definition for the hud class, which draws 2d elements on the screen.

import sys
import os
import pygame
import math
import time
import random
from drawable import *
from pygame.locals	import *
from math2			import *
import gfx2d
from pygame			import *


class Hud(Drawable):	
	def __init__(self, gameSpace):
		super(Hud, self).__init__(gameSpace, 0,0,0, 0,0,1, 0,1,0)
		
		# Initialize blank message list
		self.messageList = []
		
		# Load sprites
		self.imgStatic = Sprite("img/static.png", 2,1)
		self.imgFlynn = Sprite("img/flynn.png", 3,1)
		self.imgRadar = Sprite("img/radar.png", 1,1)
		self.imgShip = Sprite("img/ship.png", 1,1)
		self.imgPlayerShip = Sprite("img/pship.png", 1,1)
		self.imgTalkBar = Sprite("img/talkbar.png", 1,1)
		
		# Sprite index
		self.ind = 0

		# Load Sounds
		self.sndInd = 0
		self.snds = 6
		
		self.sndFlynn = []
		for i in range(0,self.snds):
			self.sndFlynn.append(pygame.mixer.Sound("snd/flynn" + str(i) + ".ogg"))
				
		self.sndRadioStart = pygame.mixer.Sound("snd/radioStart.ogg")
		self.sndRadioEnd = pygame.mixer.Sound("snd/radioEnd.ogg")

		# Timers for animation
		self.staticTimeMax = 20
		self.staticTimeIn = self.staticTimeMax
		self.scaredTime = 50		
		self.liveTime = 250
		self.staticTimeOut = self.staticTimeMax		

		# Text & index through text
		self.text = "Welcome, new pilot! You can fly around with\nthe mouse, and shoot with the left mouse\nbutton. Use W to boost, and S to slow down.\n\nTry spinning with A/D--that's a neat trick!\n\nGood luck, and enjoy your flight!"
		self.talkInd = 0
		
		# Play radio start sound
		self.sndRadioStart.play()
				
		
	def tick(self, input):
		self.ind = (self.ind + .4) % 2
		
		# Tick timers for animations/Perform various small 
		if self.staticTimeIn > 0:
			self.staticTimeIn -= 1
		elif self.scaredTime > 0:
			self.scaredTime -= 1
		elif self.talkInd < len(self.text):
			self.talkInd += .5
			
			if rnd() < .3:
				snd = self.sndFlynn[random.randrange(0,self.snds)]
				snd.play()
			
			self.sndInd = (self.sndInd + 1) % self.snds
		elif self.liveTime > 0:
			self.ind = 0
			self.liveTime -= 1
		elif self.staticTimeOut > 0:
			if self.staticTimeOut == self.staticTimeMax:
				self.sndRadioEnd.play()
				
			self.staticTimeOut -= 1

	def draw(self, screen):
		pass
		
	def blitToScreen(self, screen):
		pl = self.gs.player

		if pl.deathAnimation > -1:
			gfx2d.drawTextShadow(screen, "YOU DIED.\nPress r to respawn.", 640 - 200, 100, 1,5, FONT_WHITE)
			return
		
		w = 96
		h = 96
		xTB = 15+96+15
		yTB = 480-15-96

		# If talking has not ended
		if self.staticTimeOut > 0:	
			# Draw talk bar
			self.imgTalkBar.draw(screen, int(xTB+373/2),yTB+48)
			
			
			# If in intro static, draw & set height
			if self.staticTimeIn > 0:
				h = int(h * (self.staticTimeMax-self.staticTimeIn)/self.staticTimeMax)
				self.imgStatic.draw(screen, 15+48, 480-48-15, frame=self.ind, scale=(.75, .75*(self.staticTimeMax-self.staticTimeIn)/self.staticTimeMax))	

			# Otherwise, if talk box is still not too old...
			elif self.liveTime > 0:	
				# Draw sprite
				if self.scaredTime > 0:
					self.imgFlynn.draw(screen, 15+48, 480-48-15, frame=2, scale=.75)
				else:
					self.imgFlynn.draw(screen, 15+48, 480-48-15, frame=self.ind, scale=.75)
			
				# Draw name
				gfx2d.drawTextShadow(screen, "FLYNN", xTB+2,yTB+2, color=gfx2d.FONT_YELLOW)
				
				# Draw spoken text
				gfx2d.drawTextShadow(screen, self.text[:(int)(self.talkInd)], xTB+15,yTB+15, color=gfx2d.FONT_WHITE, xscale=1,yscale=1.25)

			# Otherwise, draw outro static
			else:
				h = int(h * (self.staticTimeOut)/self.staticTimeMax)
				self.imgStatic.draw(screen, 15+48, 480-48-15, frame=self.ind, scale=(.75, .75*(self.staticTimeOut)/self.staticTimeMax))	

			# Draw sprite
			pygame.draw.rect(screen, (255,255,255), (int(15+48-w/2),int(480-48-15-h/2), int(w),int(h)), 1)

		
		# Draw health bar
		rFrac = pl.hurtAnimation
		
		# Generate random x & y to shake health bar if damaged
		if rFrac == -1 or rFrac > .8:
			rX = rY = 0
		else:
			rFrac = sqr(1-rFrac)
			rX = (1 - 2*random.random()) * rFrac * 8
			rY = (1 - 2*random.random()) * rFrac * 8
			
		
		gfx2d.drawHealthbar(screen, pl.drawHP, 640-15-195 + rX,15 + rY)

		
		# Draw Radar
		radarX = 640-15-48
		radarY = 480-48-15
		radarScale = 100

		self.imgRadar.draw(screen, radarX, radarY, frame=0, scale=.75)
		
		arwingList = self.gs.arwingInsts
		if self.gs.isConnected and len(arwingList) > 0:
			for arwingID in arwingList:	
				arwing = arwingList[arwingID]
			
				# Get position from player
				x = arwing.ori[0]/radarScale
				y = -arwing.ori[1]/radarScale
				z = -arwing.ori[2]
				
				# If player within bounds of radar...
				if sqrt(x*x + y*y) < 48:
					# Get direction
					dir = ptDir(-x,-y, -arwing.ori[3]/radarScale,arwing.ori[4]/radarScale)

					# Draw blip
					if arwing == pl:
						self.imgPlayerShip.draw(screen, radarX+x,radarY+y, angle=dir, scale=.25)
					else:
						self.imgShip.draw(screen, radarX+x,radarY+y, angle=dir, scale=.25)
		else:
			arwing = pl
			
			# Get position from player
			x = arwing.ori[0]/radarScale
			y = -arwing.ori[1]/radarScale
			z = -arwing.ori[2]
			
			# If player within bounds of radar...
			if sqrt(x*x + y*y) < 48:
				# Get direction & draw blip
				dir = ptDir(-x,-y, -arwing.ori[3]/radarScale,arwing.ori[4]/radarScale)			
				self.imgPlayerShip.draw(screen, radarX+x,radarY+y, angle=dir, scale=.25)		
		
	
		if self.gs.isConnected:
			gfx2d.drawTextShadow(screen, "Successfully connected!", 0,0, color=gfx2d.FONT_GREEN)
		else:
			dotStr = "." * (3 - self.gs.connectTimer/self.gs.connectDiv % 4)

			gfx2d.drawTextShadow(screen, "Attempting to connect" + dotStr, 0,0, color=gfx2d.FONT_RED)

		# Draw messages
		y = gfx2d.fontHeight
		for message in self.messageList:
			message[1] -= 1
			if message[1] < 0:
				self.messageList.remove(message)
				continue
			
			gfx2d.drawTextShadow(screen, message[0], 0, y)
			y += gfx2d.fontHeight
		
		#draw score:
		if (self.gs.id in self.gs.arwingInsts):
			score = self.gs.arwingInsts[self.gs.id].points;
			gfx2d.drawTextShadow(screen, "Score: " + str(score), 640 - 200, 42, gfx2d.FONT_GREEN, 1,2)
		
	def addMessage(self, txt):
		self.messageList.append([txt, 200])		

