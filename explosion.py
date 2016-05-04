import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2		import *
from drawable 		import Drawable


class Explosion(Drawable):
	def __init__(self, gameSpace, x, y):	
		super(Explosion, self).__init__(gameSpace, 0,0,0, 0,0,1, 0,1,0)
		
		self.sprite = Sprite("img/explosion.png", 13,1)
		
		self.spriteIndex = 0		
		self.spriteSpeed = .2
		
				
	def tick(self, input):
		super(Explosion, self).tick(input)	
		self.spriteIndex += self.spriteSpeed

	def draw(self, screen):
		# Play animation
		if self.spriteIndex < self.sprite.frameNum:
			self.sprite.draw(screen, self.x, self.y, self.spriteIndex, self.spriteAngle, self.spriteScale, special_flags = BLEND_RGBA_ADD)
		# Once done, destroy object
		else:
			self.destroy()
