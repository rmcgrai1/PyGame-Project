import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2			import *
from sprite 		import Sprite


class Drawable(object):
	def __init__(self, gameSpace, x,y,z):
		self.gs = gameSpace

		self.x = x
		self.y = y
		self.z = z
				
		self.speed = 0
		
		
		
		
	def destroy(self):
		self.gs.instanceRemove(self)
		
	def tick(self, input):
		
		
		# Move (x,y,z) based on velocity
		self.x += speed * (self.lookAt[0] - self.pos[0])
		self.y += speed * (self.lookAt[1] - self.pos[1])
		self.z += speed * (self.lookAt[2] - self.pos[2])
		
	def draw(self, screen):		
		pass
