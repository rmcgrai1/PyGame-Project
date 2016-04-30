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
from numpy	import *


MAT_MV = 0
MAT_P = 1
MAT_T = 2

class Screen(object):
	def __init__(self, gs, resW, resH, outW, outH):
		self.gs = gs
		
		self.resolutionWidth,self.resolutionHeight = resW,resH
		self.aspect = resW/resH
		
		self.drawResolution = self.drawWidth,self.drawHeight = outW,outH

		self.tex = pygame.image.load("img/photo.jpg").convert_alpha()
		self.texW = self.tex.get_width()
		self.texH = self.tex.get_height()

		
		self._img = pygame.Surface( (self.resolutionWidth,self.resolutionHeight) ).convert_alpha()
		self.rect = self._img.get_rect()
		
		self.far = 5000
		
		self.pixels = pygame.surfarray.pixels2d(self._img);
		canv3d.init(resW, resH, .1, self.far, 0, self.pixels);
			
		self.skS = 512
		self.rt = pygame.image.load("img/orbital-element_rt.jpg").convert_alpha()
		self.rtP = pygame.surfarray.pixels2d(self.rt)
		
		self.bk = pygame.image.load("img/orbital-element_bk.jpg").convert_alpha()
		self.bkP = pygame.surfarray.pixels2d(self.bk)
		self.dn = pygame.image.load("img/orbital-element_dn.jpg").convert_alpha()
		self.dnP = pygame.surfarray.pixels2d(self.dn)
		self.ft = pygame.image.load("img/orbital-element_ft.jpg").convert_alpha()
		self.ftP = pygame.surfarray.pixels2d(self.ft)
		self.lf = pygame.image.load("img/orbital-element_lf.jpg").convert_alpha()
		self.lfP = pygame.surfarray.pixels2d(self.lf)
		self.up = pygame.image.load("img/orbital-element_up.jpg").convert_alpha()
		self.upP = pygame.surfarray.pixels2d(self.up)
		
		#self.starship = canv3d.loadObj("starship.obj");
		self.starship = canv3d.loadObj("Arwing.obj");

		canv3d.setTexture(pygame.surfarray.pixels2d(self.tex), self.texW, self.texH);
                
		self.radians = 0;
		self.mouse_dx = 0;
		self.mouse_dy = 0;
		self.speed = 0;
        

	def tick(self, input):
		self.mouse_dx = input["mouse_dx"];
		self.mouse_dy = input["mouse_dy"];
		self.speed += input["key_vdir"]/60.0;
					
	def finalize(self):

		canv3d.clear();
		
		lookDis = -100;

		#Camera Setting
		canv3d.cameraTurn(-self.mouse_dx/6.0, self.mouse_dy/6.0);
		canv3d.cameraForwards(self.speed);

		canv3d.cameraForwards(-lookDis);

		canv3d.setMatIdentity(MAT_MV)
		canv3d.setMatCamera(MAT_MV);
		#canv3d.addMatCameraRotation(MAT_MV);

		#Initialize Perspective and Transform
		canv3d.setMatIdentity(MAT_P)
		canv3d.setMatIdentity(MAT_T)
		
		canv3d.compileMats()
		
		
		
		
		pl = self.gs.player
		
		frX = pl.x
		frY = pl.y
		frZ = pl.z		
		
		# PROJECTION
		canv3d.addMatTranslation(MAT_P, self.resolutionWidth/2, self.resolutionHeight/2,0)
		canv3d.addMatScale(MAT_P, .5,.5,-1)
		canv3d.addMatPerspective(MAT_P, 1) #45


		sk = self.far/2
		
		#Skybox
		canv3d.setMatCameraPosition(MAT_T)
		canv3d.compileMats()

		canv3d.setRGB(255,255,255)
                

		canv3d.setTexture(self.upP, self.skS,self.skS);		
		canv3d.draw3dFloor(-sk,sk,sk,-sk, sk)

		canv3d.setTexture(self.ftP, self.skS,self.skS);		
		canv3d.draw3dWall(sk,-sk,sk, sk,sk, -sk)

		canv3d.setTexture(self.lfP, self.skS,self.skS);		
		canv3d.draw3dWall(sk,sk,sk, -sk,sk, -sk)

		canv3d.setTexture(self.rtP, self.skS,self.skS);		
		canv3d.draw3dWall(-sk,-sk,sk, sk,-sk, -sk)

 		canv3d.setTexture(self.bkP, self.skS,self.skS);		
		canv3d.draw3dWall(-sk,sk,sk, -sk,-sk, -sk)

		canv3d.setTexture(self.dnP, self.skS,self.skS);
		canv3d.draw3dFloor(-sk,-sk,sk,sk, -sk)



		canv3d.setMatIdentity(MAT_T)
		canv3d.addMatCameraPosition(MAT_T)

		canv3d.cameraForwards(-lookDis);
		canv3d.setMatIdentity(MAT_MV)
		canv3d.setMatCamera(MAT_MV);


		#canv3d.addMatRotationY(MAT_T, 50*epoch())
		canv3d.addMatCameraRotation(MAT_T);
		#canv3d.addMatScale(MAT_T, 50,50,50)
		canv3d.addMatScale(MAT_T, .25,.25,.25)
		canv3d.compileMats()
		canv3d.drawObj(self.starship)
		
		
		canv3d.cameraForwards(lookDis);	
		canv3d.setMatIdentity(MAT_MV)
		canv3d.setMatCamera(MAT_MV);



		t = 50
		s = 30
		canv3d.setMatIdentity(MAT_T)
		canv3d.compileMats()

		canv3d.setTexture(pygame.surfarray.pixels2d(self.tex), self.texW, self.texH);
		canv3d.draw3dWall(-t,-t,-t, -t,t,t)
		
		
		
		canv3d.addMatTranslation(MAT_T, 0,0,150)		
		canv3d.addMatRotationZ(MAT_T, epoch()*50)
		
		canv3d.compileMats()
		
		canv3d.setRGB(0,0,255);
		canv3d.draw3dWall(-s,-s,-s, s,-s,s)
		canv3d.draw3dWall(-s,s,-s, s,s,s)
		canv3d.draw3dWall(-s,-s,-s, -s,s,s)
		canv3d.draw3dWall(s,-s,-s, s,s,s)
		
		canv3d.setRGB(0,255,0);
		canv3d.draw3dFloor(-s,-s,s,s, -s)				
		canv3d.draw3dFloor(-s,-s,s,s, s)
		
		
		# WHERE THE MAGIC HAPPENS
		self.img = pygame.transform.scale(self._img, self.drawResolution) #smoothscale
		self.rect = self.img.get_rect()
		
		canv3d.cameraForwards(lookDis);


		
	def draw(self, screen):
		self.finalize()
		screen.blit(self.img, self.rect)
