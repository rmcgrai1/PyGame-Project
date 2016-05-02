import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2			import *
from sprite 		import Sprite
from drawable		import *
from mat			import *
import canv3d


class Laser(Drawable):
	def __init__(self, gameSpace, x,y,z, atX,atY,atZ, upX,upY,upZ):
		super(Laser, self).__init__(gameSpace, x,y,z, atX,atY,atZ, upX,upY,upZ)
		self.speed = 30
	
	def tick(self, input):
		super(Laser, self).tick(input)
		
	def draw(self, screen):	
		canv3d.setMatIdentity(MAT_T)
		canv3d.addMatTranslation(MAT_T, self.ori[0],self.ori[1],self.ori[2])
		
		nX = self.ori[3]-self.ori[0]
		nY = self.ori[4]-self.ori[1]
		nZ = self.ori[5]-self.ori[2]
		
		canv3d.addMatAntiLook(MAT_T, 0,0,0,		nX,nY,nZ,		self.ori[6],self.ori[7],self.ori[8]);
		canv3d.addMatTranslation(MAT_T, 0,-5,0)
		
		canv3d.addMatScale(MAT_T,.25,.25,.25);
		canv3d.compileMats()
		
		canv3d.unsetTexture()
		
		l = 100
		w = 8
		canv3d.draw3dFloor(-l,-l, l,l, 0);
		canv3d.drawTriangle(
			0,0,1,0,0,
			-w,0,l,0,0, 
			w,0,l,0,0)