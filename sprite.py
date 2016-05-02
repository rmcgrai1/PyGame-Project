import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2			import *

class Sprite:
	transparent = (0,0,0,0)
	
	def __init__(self, fileName, frameNumX, frameNumY):
		# Load base image, with all frames
		self.__img = pygame.image.load(fileName).convert_alpha()	

		# Get frames along x/y axes, and total number of frames
		self.frameNumX = frameNumX
		self.frameNumY = frameNumY
		self.frameNum = frameNumX*frameNumY

		# Get width/height
		self.w = (pygame.Surface.get_width(self.__img) / self.frameNumX)
		self.h = (pygame.Surface.get_height(self.__img) / self.frameNumY)
		
		# Create Surface for storing current subframe
		self._img = self.img = pygame.Surface( (self.w,self.h) ).convert_alpha()
		self.rect = self._img.get_rect()
		
		self.currentFrame = -1


	def get(self, x, y, frame = 0, angle = 0, scale = 1, alpha = 1):
		# Ensure frame is within bounds
		frame %= self.frameNum
		_frame = int(frame)

		# If frame is not already in _img, copy it into _img
		if self.currentFrame != frame:
			self.currentFrame = frame
			
			xFr = _frame % self.frameNumX
			yFr = (_frame - xFr)/self.frameNumY
			
			subRect = (self.w*xFr,self.h*yFr,self.w*(xFr+1),self.h*(yFr+1))
			self._img.fill(Sprite.transparent)
			self._img.blit(self.__img, (0,0), subRect)
		
		# Transform _img based on scale & angle, and put into img
		oldCenter = self.rect.center
		self.img = pygame.transform.smoothscale(self._img, (int(scale*self.w),int(scale*self.h)) )
		self.img = pygame.transform.rotate(self.img, angle)
		self.rect = self.img.get_rect()
		self.rect.center = (x, y)
		
		# Set img's alpha
		self.img.set_alpha(alpha)
		
		# Return image & rect
		return (self.img, self.rect)
				

	def draw(self, screen, x, y, frame = 0, angle = 0, scale = 1, alpha = 1, special_flags = 0):
		# Get given frame w/ given angle and scale
		self.get(x, y, frame, angle, scale)

		# Blit frame to screen
		screen.blit(self.img, self.rect, special_flags = special_flags)
