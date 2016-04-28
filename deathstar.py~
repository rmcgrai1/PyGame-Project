import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2		import *
from drawable 		import Drawable
from sprite 		import Sprite


green = (0,255,0)
def drawPulseLine(surf, col, startpos, endpos, maxWidth = 1):
	x1 = startpos[0]
	y1 = startpos[1]
	x2 = endpos[0]
	y2 = endpos[1]

	dx = x2-x1
	dy = y2-y1
	
	segL = 4
	n = ptDis(x1,y1,x2,y2)/segL
	i = 0
	t = epoch()

	# Draw n segments to create line, varying width to simulate pulse
	while i < n:
		# Calculate width based on time and position along line
		segW = int( math.fabs(lenY(maxWidth, -800*t+i*30)) )
	
		# Get initial & final fractional positions along line
		fi = i/n
		ff = (i+1)/n
		pi = ( int(x1+fi*dx) , int(y1+fi*dy) )
		pf = ( int(x1+ff*dx) , int(y1+ff*dy) )

		# Draw current line segment
		pygame.draw.line(surf, col, pi, pf, segW)
		i += 1


class Deathstar(Drawable):
	def __init__(self, gameSpace, x, y):
		super(Deathstar, self).__init__(gameSpace, x,y, "img/deathstar.png", 1,1)
		
		self.r = self.sprite.w/2

		self.prevChargePercent = 0;
		self.chargePercent = 0
		
		self.spriteScale = .5

		# Load sounds		
		self.sndLaserCharge = pygame.mixer.Sound("snd/laserCharge.ogg")
		self.sndLaserFire = pygame.mixer.Sound("snd/laserFire.ogg")
		self.sndLaserFire.set_volume(.25)

		# Load explosion image
		self.imgLaserHit = Sprite("img/explosion.png", 13,1)
		self.laserHitFrame = 0
		
	
	def tick(self, input):
		# Update radius based on sprite width and sprite scale
		self.r = self.sprite.w*self.spriteScale/2

		# Accelerate based on currently held key
		self.vx += input['key_hdir']*.2
		self.vy += input['key_vdir']*.2
		
		
		# Fraction to multipy velocity by when bouncing off walls (friction!)
		bounceFrac = .7

		# Left wall
		if self.x-self.r < 0:
			self.x = self.r
			self.vx *= -bounceFrac
		# Right wall
		elif self.x+self.r > self.gs.width:
			self.x = self.gs.width-self.r
			self.vx *= -bounceFrac
		# Top wall
		if self.y-self.r < 0:
			self.y = self.r
			self.vy *= -bounceFrac
		# Bottom wall
		elif self.y+self.r > self.gs.height:
			self.y = self.gs.height-self.r
			self.vy *= -bounceFrac


		# Animate laser sprite
		self.laserHitFrame += 1
		self.laserHitFrame %= self.imgLaserHit.frameNum


		super(Deathstar, self).tick(input)
		

		# If mouse held down, charge/fire laser
		if input["mouse_down"]:
			# If laser just started to charge, start playing charge sound
			if self.chargePercent == 0:
				self.sndLaserCharge.play(loops=-1, fade_ms = 2000)
		
			# Increase charge percent
			self.prevChargePercent = self.chargePercent
			self.chargePercent += 1
		
			# If laser just reached max charge, start playing fire sound
			if self.prevChargePercent < 100 and self.chargePercent >= 100:
				self.sndLaserFire.play(loops=-1, fade_ms = 200)

			# Prevent charge percent from exceeding 100
			if self.chargePercent > 100:
				self.chargePercent = 100
		else:
			# Otherwise, rotate sprite based on relative mouse position
			self.dir = ptDir(self.x,self.y, input['mouse_x'],input['mouse_y'])
			self.spriteAngle = self.dir - 45

			# If was charged, fade out charge/firing sounds
			if self.chargePercent > 0:
				self.sndLaserCharge.fadeout(500)
				self.sndLaserFire.fadeout(50)

			# Set charge percent to 0
			self.chargePercent = 0

	def draw(self, screen):	
		if self.chargePercent > 0:
			ranF = self.chargePercent/20
			ran = random.randint(0, int(ranF) )
			if self.chargePercent == 100:
				ran *= 2
			ranX = random.randint(-ran,ran)
			ranY = random.randint(-ran,ran)
			ranSc = random.random()*ranF/40
		else:
			ranX = 0
			ranY = 0
			ranSc = 0
	
		# Modify position/scale for shaking effect
		self.x += ranX
		self.y += ranY
		self.spriteScale += ranSc
		self.r = self.sprite.w*self.spriteScale/2

		# Draw sprite
		super(Deathstar, self).draw(screen)
		
		# If charging, draw triangle beams building up laser
		if self.chargePercent > 0:
			dir = self.dir
			
			dx = lenX(1, dir)
			dy = lenY(1, dir)
			
			fov = 20
			# Position where segments meet
			p0 = (self.x + dx*(self.r+16),	self.y + dy*(self.r+16))
			# Three prongs of laser
			p1 = (self.x + lenX(self.r-16, dir-fov),self.y + lenY(self.r-16, dir-fov))
			p2 = (self.x + lenX(self.r-16, dir+fov),self.y + lenY(self.r-16, dir+fov))
			p3 = (self.x + lenX(self.r-30, dir),	self.y + lenY(self.r-30, dir))
			
			# Draw triangle beams		
			segW = 3
			drawPulseLine(screen, green, p1, p0, segW)
			drawPulseLine(screen, green, p2, p0, segW)
			drawPulseLine(screen, green, p3, p0, segW)

			# If firing laser, then draw laser
			if self.chargePercent == 100:
				# Accelerate backwards from sheer power of laser
				self.vx -= dx*.2
				self.vy -= dy*.2
			
				# Get earth
				earth = self.gs.earth
				hit = False
				

				# Raycast position where laser would be colliding with earth
				p4 = raycastCircle(p0[0],p0[1],self.dir, earth.x,earth.y,earth.r)

				# If does not hit or the earth is dead, calculate some position REALLY far away so the laser is going offscreen
				if not p4 or earth.isDead():
					p4 = (self.x + lenX(1000, dir),	self.y + lenY(1000, dir))
				# Otherwise, damage the earth
				else:
					earth.damage(1)
					hit = True

				# Draw line
				pygame.draw.line(screen, green, p0, p4, 1)
				
				# If hit, draw fire animation at spot of collision
				if hit:
					self.imgLaserHit.draw(screen,  p4[0]+ranX,p4[1]+ranY, self.laserHitFrame, scale=1+random.random()*.5, angle=random.random()*360, special_flags = BLEND_RGBA_ADD)

		# Return position/scale to normal
		self.x -= ranX
		self.y -= ranY
		self.spriteScale -= ranSc
		self.r = self.sprite.w*self.spriteScale/2
