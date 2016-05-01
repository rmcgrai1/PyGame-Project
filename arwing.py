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


class Arwing(Drawable):
	def __init__(self, gameSpace, x,y,z):
		super(Arwing, self).__init__(gameSpace, x,y,z)

		self.model = canv3d.loadObj("Arwing.obj");
		
		self.dpos = numpy.array([x, y, z, 1.])		
		self.dtoPos = numpy.array([x, y, z-1, 1.])		
		self.dupNorm = numpy.array([0,1,0,0.])

        
	def tick(self, input):
		super(Arwing, self).tick(input)
		
		canv3d.turn(self.pos, self.toPos, self.upNorm, input['mouse_dx']*input['mouse_d_adjust'], -input['mouse_dy']*input['mouse_d_adjust']);
		
		x = self.pos[0]
		y = self.pos[1]
		z = self.pos[2]
		toX = self.toPos[0]
		toY = self.toPos[1]
		toZ = self.toPos[2]
		
		dis = -200

		aX = dis*(toX-x)
		aY = dis*(toY-y)
		aZ = dis*(toZ-z)
		
		eyeX = x - aX
		eyeY = y - aY
		eyeZ = z - aZ
		toX -= aX
		toY -= aY
		toZ -= aZ
				
		canv3d.camera(eyeX,eyeY,eyeZ,toX,toY,toZ,self.upNorm[0],self.upNorm[1],self.upNorm[2]);
		
	def draw(self, screen):
		canv3d.setMatIdentity(MAT_T)
		canv3d.addMatTranslation(MAT_T, self.pos[0],self.pos[1],self.pos[2])

		spd = 8
		for i in range(0,3):
			self.dpos[i] += (self.pos[i] - self.dpos[i])/spd;
			self.dtoPos[i] += (self.toPos[i] - self.dtoPos[i])/spd;
			self.dupNorm[i] += (self.upNorm[i] - self.dupNorm[i])/spd;
		
		nX = self.dtoPos[0]-self.dpos[0]
		nY = self.dtoPos[1]-self.dpos[1]
		nZ = self.dtoPos[2]-self.dpos[2]
		
		canv3d.addMatAntiLook(MAT_T, 0,0,0,		nX,nY,nZ,		self.dupNorm[0],self.dupNorm[1],self.dupNorm[2]);
		
		canv3d.addMatScale(MAT_T,.25,.25,.25);
		canv3d.compileMats()
		
				
		canv3d.drawObj(self.model);
