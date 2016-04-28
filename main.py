# 1:30p - 2:05p on 4/23
# 4:00p - 5:00p on 4/23
# 5:00p - 6:00p on 4/23
# 7:37p - 8:37p on 4/23

import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from src		import *
from drawable	import *
from deathstar	import *
from earth		import *
from player		import *
from earthchunk	import *

from sprite	import *

from math2	import *

from explosion	import *

from screen	import *
from oscreen	import *

	

class GameSpace:
	def instanceAppend(self, inst):
		self.instanceList.append(inst)
		return inst
	def instancePrepend(self, inst):
		self.instanceList.insert(0, inst)
		return inst
	def instanceRemove(self, inst):
		try:
			del self.instanceList[self.instanceList.index(inst)]
		except:
			pass

	def main(self):
		#1. Initialize game space

		pygame.init()
		pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=1024) #4096

		size = self.width,self.height = (640,480)
		screen = pygame.display.set_mode(size)
		black = (0,0,0)

		keyHDir = 0
		keyVDir = 0
		mDown = False

		self.instanceList = []


		#2. Create game objects

		self.clock = pygame.time.Clock()
		#self.deathstar = self.instanceAppend(Deathstar(self, 150,150))
		#self.earth = self.instancePrepend(Earth(self, 500,400))
		
		self.player = self.instanceAppend(Player(self, 0,0,0))
		#self.oscreen = self.instanceAppend(OScreen(self, 80,60, 640, 480)) #80,60
		self.screen = self.instanceAppend(Screen(self, 320,240, 640, 480)) #80,60

		#3. Game loop
		while True:
			#4. Tick regulation
			self.clock.tick(60);

			#5. User input reading
			
			(mx, my) = pygame.mouse.get_pos()
			mDown = pygame.mouse.get_pressed()[0]
			
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.mixer.quit()
					sys.exit()
				elif event.type == KEYDOWN:
					if(event.key == pygame.K_a):
						keyHDir -= 1
					elif(event.key == pygame.K_d):
						keyHDir += 1
					elif(event.key == pygame.K_w):
						keyVDir -= 1
					elif(event.key == pygame.K_s):
						keyVDir += 1
				elif event.type == KEYUP:
					if(event.key == pygame.K_a):
						keyHDir += 1
					elif(event.key == pygame.K_d):
						keyHDir -= 1
					elif(event.key == pygame.K_w):
						keyVDir += 1
					elif(event.key == pygame.K_s):
						keyVDir -= 1



			#6. Tick updating and polling

			input = {
				"mouse_down": mDown,
				"mouse_x": mx,
				"mouse_y": my,
				"key_hdir": keyHDir,
				"key_vdir": keyVDir
			}
			
			for d in self.instanceList:
				d.tick(input)
			

			#7. Display

			screen.fill(black)

			for d in self.instanceList:
				d.draw(screen)
			
			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
