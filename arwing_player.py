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
		
		# Loop engine sound
		Arwing.SND_ENGINE.play(loops=-1)
		
		# Temp Array for Rotation
		self.rotateAxis = numpy.array([0., 0., 0., 0.])
		
		self.deathAnimation = -1
		self.cameraOri = numpy.array([x+0.,y,z, x,y,z+1, 0,1,0])
		
		self.laserOri = self.ori.copy()
		

	def roll(self, vec, offset, amt):
		# Calculate forward acis
		self.rotateAxis[0] = vec[3]-vec[0]
		self.rotateAxis[1] = vec[4]-vec[1]
		self.rotateAxis[2] = vec[5]-vec[2]
		
		# Rotate about forward axis
		canv3d.rotateVecAboutAxis(vec, offset, amt, self.rotateAxis);

		
	def pitch(self, vec, offset, amt):
		# Calculate forward axis (and normalize)
		vec[3] = fX = vec[3]-vec[0]
		vec[4] = fY = vec[4]-vec[1]
		vec[5] = fZ = vec[5]-vec[2]

		# Get up axis (pre-normalized)
		upX = vec[6]
		upY = vec[7]
		upZ = vec[8]
		
		# Rotate Laser w/ Pitch
		self.rotateAxis[0] = upZ*fY - upY*fZ
		self.rotateAxis[1] = upX*fZ - upZ*fX
		self.rotateAxis[2] = upY*fX - upX*fY
		
		# Rotate 
		canv3d.rotateVecAboutAxis(vec,offset, amt, self.rotateAxis)
		
		
		
	def tick(self, input):
		super(ArwingPlayer, self).tick(input)

		if self.hp == 0:
			if self.deathAnimation == -1:	
				self.deathAnimation = 0
				self.explode();
			else:
				self.deathAnimation = 1

			return
			
		if (not self.mDownPrev) and (input['mouse_down']):			
			x = self.ori[0]
			y = self.ori[1]
			z = self.ori[2]
			
			atX = self.ori[3]
			atY = self.ori[4]
			atZ = self.ori[5]
			
			# Calculate forward axis (pre-normalized)
			fX = atX-x
			fY = atY-y
			fZ = atZ-z

			# Get up axis (pre-normalized)
			upX = self.ori[6]
			upY = self.ori[7]
			upZ = self.ori[8]

			# Calculate side axis
			sX = upZ*fY - upY*fZ
			sY = upX*fZ - upZ*fX
			sZ = upY*fX - upX*fY
			
			self.laserOri[0] = x
			self.laserOri[1] = y
			self.laserOri[2] = z
			self.laserOri[3] = atX
			self.laserOri[4] = atY
			self.laserOri[5] = atZ
			self.laserOri[6] = upX
			self.laserOri[7] = upY
			self.laserOri[8] = upZ

			# Rotate laser to match pitch
			self.pitch(self.laserOri,3, self.drawPitch)

			
			# Rotate Laser w/ Yaw
			self.rotateAxis[0] = self.laserOri[6]
			self.rotateAxis[1] = self.laserOri[7]
			self.rotateAxis[2] = self.laserOri[8]

			# Rotate laser to match yaw
			canv3d.rotateVecAboutAxis(self.laserOri,3, self.drawYaw, self.rotateAxis)

			if self.gs.isConnected:
				self.gs.mainQueue.put(self.laserOri);
			else:
				self.gs.instanceAppend( Laser(self.gs,30, 60*10,
					self.laserOri[0],self.laserOri[1],self.laserOri[2],
					self.laserOri[3],
					self.laserOri[4],
					self.laserOri[5],
					self.laserOri[6],self.laserOri[7],self.laserOri[8]
				));

		# Update previous mouse down value
		self.mDownPrev = input['mouse_down']
		
		# Find speed fraction
		speedFrac = .6 + .4 * self.speed / Arwing.SPD_BASE

		# Get input values
		dx = input['mouse_dx'] * speedFrac
		dy = input['mouse_dy'] * speedFrac
		hDir = input['key_hdir']
		vDir = input['key_vdir']
		adjust = input['mouse_d_adjust']
		
	
		# Roll sideways when A/D held
		self.roll(self.ori, 6, -2*hDir);


		# If holding boost, speed up and play sound
		if vDir == -1:
			if self.vDirPrev != -1:
				Arwing.SND_BRAKE.stop()
				Arwing.SND_BOOST.play()
			toSpeed = Arwing.SPD_MAX
			
		# If holding brake, slow down and play sound
		elif vDir == 1:
			if self.vDirPrev != 1:
				Arwing.SND_BOOST.stop()
				Arwing.SND_BRAKE.play()
			toSpeed = Arwing.SPD_MIN
			
		# Otherwise, fly as normal
		else:
			toSpeed = Arwing.SPD_BASE
			
		# Update previous hold vertical direction
		self.vDirPrev = vDir
			
			
		# Smoothly interpolate values to new ones
		self.speed += (toSpeed - self.speed)/20.;
		
		toRoll = -12*dx*adjust * 2
		toYaw = -12*dx*adjust  * 2
		toPitch = 12*dy*adjust * 2
		
		self.drawRoll += (toRoll - self.drawRoll)/5
		self.drawYaw += (toYaw - self.drawYaw)/5
		self.drawPitch += (toPitch - self.drawPitch)/5
		
		
		# Rotate arwing based on mouse control
		canv3d.turn(self.ori,0, self.ori,3, self.ori,6, -dx*adjust,-dy*adjust);


		# Determine camera position
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
		
		self.cameraOri[0] = x - aX
		self.cameraOri[1] = y - aY
		self.cameraOri[2] = z - aZ
		self.cameraOri[3] = toX - aX
		self.cameraOri[4] = toY - aY
		self.cameraOri[5] = toZ - aZ
		self.cameraOri[6] = self.ori[6]
		self.cameraOri[7] = self.ori[7]
		self.cameraOri[8] = self.ori[8]

		canv3d.camera(self.cameraOri[0],self.cameraOri[1],self.cameraOri[2],
			self.cameraOri[3],self.cameraOri[4],self.cameraOri[5],
			self.cameraOri[6],self.cameraOri[7],self.cameraOri[8]);
		
	def draw(self, screen):
		# If alive and well, draw arwing
		if self.deathAnimation < 1:
			super(ArwingPlayer, self).draw(screen)
