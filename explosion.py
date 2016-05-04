import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2		import *
from drawable 		import Drawable
import canv3d
from sprite 		import *
from mat			import *



class Explosion(Drawable):
	def __init__(self, gameSpace, x, y, z):	
		super(Explosion, self).__init__(gameSpace, x,y,z, x,y,z+1, 0,1,0)
		
		self.sprite = Sprite("img/explosion.png", 13,1)
		
		self.spriteIndex = 0		
		self.spriteSpeed = .6
		
		# Build numpy arrays for each image
		self.spritePixels = []
		
		w = self.sprite.w
		h = self.sprite.h
		for i in range(0,13):
			pixs = pygame.surfarray.pixels2d(self.sprite.get(0,0,frame=i)[0].copy())			
			self.spritePixels.append(pixs)
		
	def tick(self, input):
		super(Explosion, self).tick(input)	
		self.spriteIndex += self.spriteSpeed

	def draw(self, screen):
		# Play animation
		if self.spriteIndex < self.sprite.frameNum:
			canv3d.setMatTranslation(MAT_T, self.ori[0],self.ori[1],self.ori[2])
			canv3d.addMatCameraAntiRotation(MAT_T)
			canv3d.compileMats()
		
			s = 96
			canv3d.setTexture(self.spritePixels[int(self.spriteIndex)], self.sprite.w, self.sprite.h)
			canv3d.draw3dFloor(-s,-s, s,s, 0)
		# Once done, destroy object
		else:
			self.destroy()
