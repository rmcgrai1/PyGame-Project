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
from laser			import *
import canv3d


class Arwing(Drawable):
	model = canv3d.loadObj("Arwing.obj");

	def __init__(self, gameSpace, x,y,z):
		super(Arwing, self).__init__(gameSpace, x,y,z, x,y,z+1, 0,1,0)

	
		self.jetTex = pygame.surfarray.pixels2d(pygame.image.load("img/jet.png").convert_alpha())
		self.jetTexWidth = 128
		self.jetTexHeight = 128
		
		self.dpos = numpy.array([x, y, z, 1.])		
		self.dtoPos = numpy.array([x, y, z-1, 1.])		
		self.dupNorm = numpy.array([0,1,0,0.])
		
		self.speed = 5
		self.roll = 0
		self.pitch = 0
		self.yaw = 0
		
		self.sndEngine = pygame.mixer.Sound("engine.ogg")
		self.sndSingleShot = pygame.mixer.Sound("singleshot.ogg")
		
	
	def tick(self, input):
		super(Arwing, self).tick(input)
		
	def draw(self, screen):
		canv3d.setMatIdentity(MAT_T)
		canv3d.addMatTranslation(MAT_T, self.ori[0],self.ori[1],self.ori[2])

		spd = 8
		for i in range(0,3):
			self.dpos[i] += (self.ori[i] - self.dpos[i])/spd;
			self.dtoPos[i] += (self.ori[3+i] - self.dtoPos[i])/spd;
			self.dupNorm[i] += (self.ori[6+i] - self.dupNorm[i])/spd;
		
		nX = self.dtoPos[0]-self.dpos[0]
		nY = self.dtoPos[1]-self.dpos[1]
		nZ = self.dtoPos[2]-self.dpos[2]
		
		canv3d.addMatAntiLook(MAT_T, 0,0,0,		nX,nY,nZ,		self.dupNorm[0],self.dupNorm[1],self.dupNorm[2]);
		canv3d.addMatRotationX(MAT_T, self.pitch)
		canv3d.addMatRotationY(MAT_T, self.yaw)
		canv3d.addMatRotationZ(MAT_T, self.roll)
		canv3d.addMatTranslation(MAT_T, 0,-5,0)
		
		canv3d.addMatScale(MAT_T,.25,.25,.25);
		canv3d.compileMats()
		
	
		canv3d.drawObj(Arwing.model);
		canv3d.setTexture(self.jetTex, self.jetTexWidth, self.jetTexHeight)
		
		xs = 50 * (1 + .5*rnd()) 
		ys = xs * .8
		up = 10
		back = -80
		canv3d.draw3dFloor(-xs,up-ys,xs,up+ys,back);

		#s = 25 * (1 + .5*rnd()) 
		#spc = 35
		#up = 10
		#back = -55
		#canv3d.draw3dFloor(-spc-s,up-s,-spc+s,up+s,back);
		#canv3d.draw3dFloor(spc-s,up-s,spc+s,up+s,back);
