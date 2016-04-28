import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2			import *
from drawable 		import Drawable
from sprite 		import Sprite


class Player(object):
	def __init__(self, gameSpace, x,y,z):
		self.x = x
		self.y = y
		self.z = z
		self.vx = 0
		self.vy = 0
		self.vz = 0
		self.dir = 0
		
	
	def tick(self, input):
		# Update radius based on sprite width and sprite scale
		#self.r = self.sprite.w*self.spriteScale/2

		# Accelerate based on currently held key
		#self.vx += input['key_hdir']*.2
		#self.vy += input['key_vdir']*.2
		
		self.dir -= 4*input['key_hdir']
		
		amt = 3*input['key_vdir']
		self.x -= lenX(amt, self.dir)
		self.y += lenY(amt, self.dir)

	def draw(self, screen):
		pass