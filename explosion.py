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
		super(Explosion, self).__init__(gameSpace, x,y, "img/explosion.png", 13,1)
		
		self.spriteSpeed = .2
		self.spriteLoop = False
		self.spriteScale = 7
		
				
	def tick(self, input):
		super(Explosion, self).tick(input)

	def draw(self, screen):
		# Play animation
		if self.spriteIndex < self.sprite.frameNum:
			self.sprite.draw(screen, self.x, self.y, self.spriteIndex, self.spriteAngle, self.spriteScale, special_flags = BLEND_RGBA_ADD)
		# Once done, destroy object
		else:
			self.destroy()
