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

		self.ori = [x,y,z,  x,y,z-1,  0,1,0.]
		self.ori = numpy.array(self.ori)	
		
		self.speed = 0
	
	def destroy(self):
		self.gs.instanceRemove(self)
		
	def tick(self, input):
		# Move (x,y,z) based on velocity
		aX = -self.speed * (self.ori[3] - self.ori[0])
		aY = -self.speed * (self.ori[4] - self.ori[1])
		aZ = -self.speed * (self.ori[5] - self.ori[2])

		self.ori[0] += aX;
		self.ori[1] += aY;
		self.ori[2] += aZ;
		self.ori[3] += aX;
		self.ori[4] += aY;
		self.ori[5] += aZ;
		
	def draw(self, screen):		
		pass
