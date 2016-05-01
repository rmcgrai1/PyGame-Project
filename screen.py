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
	def __init__(leftName, rightName, frontName, backName, upName, downName):
		self.skS = 512
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