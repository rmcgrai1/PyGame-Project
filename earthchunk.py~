import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2			import *
from drawable 		import Drawable


class EarthChunk(Drawable):
	def __init__(self, gameSpace, x, y, dir):
		super(EarthChunk, self).__init__(gameSpace, x,y, "img/chunk" + str(random.randint(1,3)) + ".png", 1,1)
	
		# Randomize spinning speed
		self.spriteAngleSpeed = (random.random()-.5)*80

		# Randomize velocity and scale
		f = (.5 + .5*random.random())
		self.vx = f*lenX(20,dir)
		self.vy = f*lenY(20,dir)
		self.spriteScale = (.5 + .5*random.random()) * .3;
		
				
	def tick(self, input):
		super(EarthChunk, self).tick(input)
		self.spriteAngle += self.spriteAngleSpeed

	def draw(self, screen):
		super(EarthChunk, self).draw(screen)
