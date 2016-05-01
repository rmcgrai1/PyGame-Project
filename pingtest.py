import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2		import *
from sprite 		import Sprite
from drawable		import *
from mat		import *
import canv3d


class PingTest(Drawable):
	def __init__(self, gameSpace, x,y,z):
		super(PingTest, self).__init__(gameSpace, x,y,z)		
		self.angle = 0
	
	def tick(self, input):
		pass
		
	def draw(self, screen):
		canv3d.setMatIdentity(MAT_T)
		canv3d.addMatTranslation(MAT_T, self.pos[0],self.pos[1],self.pos[2])
		canv3d.addMatRotationY(MAT_T, self.angle)
		canv3d.compileMats()
		
		s = 50 
		canv3d.draw3dFloor(-s,-s,s,s,0);
