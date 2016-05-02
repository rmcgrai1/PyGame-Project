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
from arwing			import *
import numpy


class ArwingPlayer(Arwing):
	def __init__(self, gameSpace, x,y,z):
		super(ArwingPlayer, self).__init__(gameSpace, x,y,z)
		self.mDownPrev = False
		self.vDirPrev = 0
		
		Arwing.SND_ENGINE.play(loops=-1)
		
		self.forwardAxis = numpy.array([0., 0., 0., 0.])
		
			
	def tick(self, input):
		super(ArwingPlayer, self).tick(input)
		
		if (not self.mDownPrev) and (input['mouse_down']):
			Arwing.SND_SINGLE_SHOT.play()
			if (self.gs.isConnected):
				self.gs.mainQueue.put(self.ori);
			else:
				self.gs.instanceAppend( Laser(self.gs, ) )

		self.mDownPrev = input['mouse_down']
		
		dx = input['mouse_dx']
		dy = input['mouse_dy']
		hDir = input['key_hdir']
		vDir = input['key_vdir']
		adjust = input['mouse_d_adjust']
		
		self.forwardAxis[0] = self.ori[3]-self.ori[0]
		self.forwardAxis[1] = self.ori[4]-self.ori[1]
		self.forwardAxis[2] = self.ori[5]-self.ori[2]
				
		#canv3d.rotateVecAboutAxis(self.ori,6, hDir, self.forwardAxis);

		
		if vDir == -1:
			if self.vDirPrev != -1:
				Arwing.SND_BOOST.play()
			toSpeed = Arwing.SPD_MAX
		elif vDir == 1:
			if self.vDirPrev != 1:
				Arwing.SND_BRAKE.play()
			toSpeed = Arwing.SPD_MIN
		else:
			toSpeed = Arwing.SPD_BASE
		self.vDirPrev = vDir
			
		self.speed += (toSpeed - self.speed)/20.;
		
		toRoll = -12*dx*adjust * 2
		toYaw = -12*dx*adjust  * 2
		toPitch = 12*dy*adjust * 2
		
		self.roll += (toRoll - self.roll)/5
		self.yaw += (toYaw - self.yaw)/5
		self.pitch += (toPitch - self.pitch)/5
		
		
		canv3d.turn(self.ori,0, self.ori,3, self.ori,6, -dx*adjust,-dy*adjust);
		
		x = self.ori[0]
		y = self.ori[1]
		z = self.ori[2]
		toX = self.ori[3]
		toY = self.ori[4]
		toZ = self.ori[5]
				
		dis = -200 * (.5 + .5*self.speed/Arwing.SPD_BASE )

		aX = dis*(toX-x)
		aY = dis*(toY-y)
		aZ = dis*(toZ-z)
		
		eyeX = x - aX
		eyeY = y - aY
		eyeZ = z - aZ
		toX -= aX
		toY -= aY
		toZ -= aZ
				
		canv3d.camera(eyeX,eyeY,eyeZ,toX,toY,toZ,self.ori[6],self.ori[7],self.ori[8]);
		
	def draw(self, screen):
		super(ArwingPlayer, self).draw(screen)
