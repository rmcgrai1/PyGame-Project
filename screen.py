import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from pygame.gfxdraw	import *
from math2		import *
from drawable 		import Drawable
import canv3d
import numpy
from numpy	import *


MAT_M = 0
MAT_V = 1
MAT_P = 2

class Screen(object):
	def __init__(self, gs, resW, resH, outW, outH):
		self.gs = gs
		
		self.resolutionWidth,self.resolutionHeight = resW,resH
		self.aspect = resW/resH
		
		self.drawResolution = self.drawWidth,self.drawHeight = outW,outH

		self.tex = pygame.image.load("img/test.bmp").convert_alpha()
		self.texW = self.tex.get_width()
		self.texH = self.tex.get_height()

		
		self._img = pygame.Surface( (self.resolutionWidth,self.resolutionHeight) ).convert_alpha()
		self.rect = self._img.get_rect()
		
		self.pixels = pygame.surfarray.pixels2d(self._img);
		canv3d.init(resW, resH, .1, 300, 1, self.pixels);
		
		canv3d.setTexture(pygame.surfarray.pixels2d(self.tex), self.texW, self.texH);
		
	def tick(self, input):
		pass
					
	def finalize(self):
		canv3d.clear();
		
		canv3d.setMatIdentity(MAT_M)
		canv3d.setMatIdentity(MAT_V)
		canv3d.setMatIdentity(MAT_P)
		
		pl = self.gs.player
		
		frX = pl.x
		frY = pl.y
		frZ = pl.z
		
		#setMatLook(MAT_V, frX,frY,frZ, toX,toY,toZ, 0,0,1)
		#addMatRotationZ(MAT_V, 90)
		
		# CAMERA ROTATION
		#canv3d.addMatRotationX(MAT_V, 90)
		canv3d.addMatRotationY(MAT_V, -pl.dir)
		#canv3d.addMatRotationZ(MAT_V, -90)
		canv3d.addMatTranslation(MAT_V, -pl.y,-pl.z,-pl.x)
		#canv3d.addMatRotationZ(MAT_V, 90)
		
		
		# PROJECTION
		canv3d.addMatTranslation(MAT_P, self.resolutionWidth/2, self.resolutionHeight/2,0)
		canv3d.addMatScale(MAT_P, 1,1,-1)
		canv3d.addMatPerspective(MAT_P, 1) #45

		t = 50
		s = 30
		canv3d.compileArrays()


		canv3d.draw3dWall(-t,-t,t, -t,t, -s)
		
		
		
		canv3d.addMatTranslation(MAT_M, 0,0,150)		
		#addMatRotationX(MAT_M, epoch()*40)
		#addMatRotationY(MAT_M, epoch()*50)
		canv3d.addMatRotationZ(MAT_M, epoch()*50)
		
		canv3d.compileArrays()
		
		canv3d.setRGB(0,0,255);
		canv3d.draw3dWall(-s,-s,-s, s,-s,s)
		canv3d.draw3dWall(-s,s,-s, s,s,s)
		canv3d.draw3dWall(-s,-s,-s, -s,s,s)
		canv3d.draw3dWall(s,-s,-s, s,s,s)
		
		canv3d.setRGB(0,255,0);
		canv3d.draw3dFloor(-s,-s,s,s, -s)				
		canv3d.draw3dFloor(-s,-s,s,s, s)
		
		#canv3d.test();
		
		#canv3d.clearStatic();

		
		# WHERE THE MAGIC HAPPENS
		self.img = pygame.transform.scale(self._img, self.drawResolution) #smoothscale
		self.rect = self.img.get_rect()

		
	def draw(self, screen):
		self.finalize()
		screen.blit(self.img, self.rect)