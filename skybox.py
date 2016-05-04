# Jacob Kassman & Ryan McGrail
# skybox.py
# Defines class for drawing skyboxes.

import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from pygame.gfxdraw	import *
from math2			import *
from drawable 		import Drawable
import canv3d
import numpy
from mat			import *
from numpy			import *

class Skybox(Drawable):
	def __init__(self, gameSpace, leftName, rightName, frontName, backName, upName, downName):
		super(Skybox, self).__init__(gameSpace, 0,0,0, 0,0,1, 0,1,0)

		# Get max possible size based on far distance in canv3d
		self.boxSize = gameSpace.canv3d_far / 2

		# Load all 6 sides of skyboz
		self.imgSize = 512
		self.lf = pygame.image.load(leftName).convert_alpha()
		self.lfP = pygame.surfarray.pixels2d(self.lf)
		self.rt = pygame.image.load(rightName).convert_alpha()
		self.rtP = pygame.surfarray.pixels2d(self.rt)
		self.ft = pygame.image.load(frontName).convert_alpha()
		self.ftP = pygame.surfarray.pixels2d(self.ft)
		self.bk = pygame.image.load(backName).convert_alpha()
		self.bkP = pygame.surfarray.pixels2d(self.bk)
		self.up = pygame.image.load(upName).convert_alpha()
		self.upP = pygame.surfarray.pixels2d(self.up)
		self.dn = pygame.image.load(downName).convert_alpha()
		self.dnP = pygame.surfarray.pixels2d(self.dn)
        
	def tick(self, input):
		pass;
		
	def draw(self, screen):
		# Translate to position of camera
		canv3d.setMatCameraPosition(MAT_T)
		# Compile matrices into single matrix
		canv3d.compileMats()

		# Revert drawing color back to white if not already white
		canv3d.setRGB(255,255,255)


		# Draw top
		canv3d.setTexture(self.upP, self.imgSize,self.imgSize);		
		canv3d.draw3dFloor(-self.boxSize,self.boxSize,self.boxSize,-self.boxSize, self.boxSize)
		# Draw front
		canv3d.setTexture(self.ftP, self.imgSize,self.imgSize);		
		canv3d.draw3dWall(self.boxSize,-self.boxSize,self.boxSize, self.boxSize,self.boxSize, -self.boxSize)
		# Draw left
		canv3d.setTexture(self.lfP, self.imgSize,self.imgSize);		
		canv3d.draw3dWall(self.boxSize,self.boxSize,self.boxSize, -self.boxSize,self.boxSize, -self.boxSize)
		# Draw right
		canv3d.setTexture(self.rtP, self.imgSize,self.imgSize);		
		canv3d.draw3dWall(-self.boxSize,-self.boxSize,self.boxSize, self.boxSize,-self.boxSize, -self.boxSize)
		# Draw back
 		canv3d.setTexture(self.bkP, self.imgSize,self.imgSize);		
		canv3d.draw3dWall(-self.boxSize,self.boxSize,self.boxSize, -self.boxSize,-self.boxSize, -self.boxSize)
		# Draw bottom
		canv3d.setTexture(self.dnP, self.imgSize,self.imgSize);
		canv3d.draw3dFloor(-self.boxSize,-self.boxSize,self.boxSize,self.boxSize, -self.boxSize)