# Jacob Kassman & Ryan McGrail
# laser.py
# Defines the laser class, which is fired by players and deals damage. (Collisions are done on the server.)

import sys
import os
import pygame
import math
import random
from pygame.locals	import *
from math2			import *
from drawable		import *
from mat			import *
import canv3d


class Laser(Drawable):
	MOD_LASER = None;
	SND_SINGLE_SHOT = None
	
	@staticmethod
	def init():
		Laser.MOD_LASER = canv3d.loadObj("laser.obj");
		Laser.SND_SINGLE_SHOT = pygame.mixer.Sound("snd/singleshot.ogg")
	
	def __init__(self, gameSpace, speed, maxAge, x,y,z, atX,atY,atZ, upX,upY,upZ):
		super(Laser, self).__init__(gameSpace, x,y,z, atX,atY,atZ, upX,upY,upZ)
		self.speed = speed
		self.maxAge = maxAge;
		self.age = 0;

		# Play sound when created
		Laser.SND_SINGLE_SHOT.play()

		
	def tick(self, input):
		super(Laser, self).tick(input)
		
		# Age, destroy if too old
		self.age = self.age + 1;
		if (self.age > self.maxAge):
			super(Laser, self).destroy();

			
	def draw(self, screen):	
		canv3d.setMatTranslation(MAT_T, self.ori[0],self.ori[1],self.ori[2])
		
		nX = self.ori[3]-self.ori[0]
		nY = self.ori[4]-self.ori[1]
		nZ = self.ori[5]-self.ori[2]

		# Rotate laser to direction
		canv3d.addMatAntiLook(MAT_T, 0,0,0,		nX,nY,nZ,		self.ori[6],self.ori[7],self.ori[8]);
		# Translate laser model into place
		canv3d.addMatTranslation(MAT_T, 0,-5,0)

		# Compile matrices into single matrix
		canv3d.compileMats()
		
		# Disable texture
		canv3d.unsetTexture()
		
		# Draw model
		canv3d.drawObj(Laser.MOD_LASER)
