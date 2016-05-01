import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2			import *
from sprite 		import Sprite
import numpy
from numpy	import *

class Drawable(object):
	def __init__(self, gameSpace, x,y,z):
		self.gs = gameSpace

		self.pos = numpy.array([x, y, z, 1.])		
		self.toPos = numpy.array([x, y, z-1, 1.])		
		self.upNorm = numpy.array([0,1,0,0.])
		
		self.speed = 0
	
	def destroy(self):
		self.gs.instanceRemove(self)
		
	def tick(self, input):
		# Move (x,y,z) based on velocity
		aX = self.speed * (self.toPos[0] - self.pos[0])
		aY = self.speed * (self.toPos[1] - self.pos[1])
		aZ = self.speed * (self.toPos[2] - self.pos[2])

		self.pos[0] += aX;
		self.pos[1] += aY;
		self.pos[2] += aZ;
		self.toPos[0] += aX;
		self.toPos[1] += aY;
		self.toPos[2] += aZ;
		
	def draw(self, screen):		
		pass
