import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from src			import *
from drawable		import *
from deathstar		import *
from earth			import *
from player			import *
from earthchunk		import *
from sprite			import *
from math2			import *
from explosion		import *
from mat			import *
from skybox			import *
from arwing			import *

	

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

		resolution = self.width,self.height = (640,480)
		screen = pygame.display.set_mode(resolution)
		black = (0,0,0)
		white = (255,255,255)

		keyHDir = 0
		keyVDir = 0
		mDown = False

		self.instanceList = []


		#2. Create game objects

		self.canv3d_near = .1
		self.canv3d_far = 5000
		self.canv3d_width = 320
		self.canv3d_height = 240
		self.canv3d_aspect = self.canv3d_width/self.canv3d_height
		self.canv3d_doFog = 0
		
		self.clock = pygame.time.Clock()	
		self.skybox = self.instanceAppend(Skybox(self, "img/orbital-element_lf.jpg","img/orbital-element_rt.jpg","img/orbital-element_ft.jpg","img/orbital-element_bk.jpg","img/orbital-element_up.jpg","img/orbital-element_dn.jpg"))
		self.player = self.instanceAppend(Arwing(self, 0,0,0))
	
		# Create 3d Canvas
		self.canv3d_img_ = pygame.Surface((self.canv3d_width,self.canv3d_height)).convert_alpha()
		canv3d.init(self.canv3d_width,self.canv3d_height, self.canv3d_near, self.canv3d_far, self.canv3d_doFog, pygame.surfarray.pixels2d(self.canv3d_img_));
		
		mouse_center_x = self.width/2;
		mouse_center_y = self.height/2;
		pygame.mouse.set_visible(False);
		pygame.event.set_grab(True);
		#pygame.mouse.set_pos(mouse_center_x, mouse_center_y);

		#3. Game loop
		while True:
			#4. Tick regulation
			self.clock.tick(60);

			#5. User input reading
#                        (mdx, mdy) = pygame.mouse.get_rel();
                  #      if ((mx < 0) || (mx > self.width)):
                        pygame.mouse.set_pos(mouse_center_x, mouse_center_y);
                        #pygame.mouse.get_rel();
 #                       mdx, mdy = mdx/10000.0, mdy/10000.0;
  #                      print mdx, mdy;
			mDown = pygame.mouse.get_pressed()[0]
			mdx, mdy = 0, 0


			for event in pygame.event.get():
				if (event.type == pygame.MOUSEMOTION):
					mdx, mdy = event.rel;
				elif event.type == QUIT:
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
					elif(event.key == pygame.K_ESCAPE):
						pygame.mixer.quit();
						sys.exit();
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
				"mouse_dy": mdy,
				"mouse_dx": mdx,
				"key_hdir": keyHDir,
				"key_vdir": keyVDir
			}
			
				
			
			for d in self.instanceList:
				d.tick(input)
			

			#7. Display

			screen.fill(white)
			canv3d.clear();

			
			# PROJECTION
			
			
			canv3d.setMatIdentity(MAT_MV)
			canv3d.setMatIdentity(MAT_P)
			canv3d.setMatIdentity(MAT_T)		
			
			canv3d.addMatTranslation(MAT_P, self.canv3d_width/2, self.canv3d_height/2,0)
			canv3d.addMatScale(MAT_P, 1,1,-1)
			canv3d.addMatPerspective(MAT_P, 1)
			canv3d.setMatCamera(MAT_MV);
			
			canv3d.compileMats();
			
			for d in self.instanceList:
				d.draw(screen)
			
			
			# Resize 3d canvas to match screen size
			self.canv3d_img = pygame.transform.scale(self.canv3d_img_, resolution)
			self.rect = self.canv3d_img.get_rect()			

			# Blit 3d canvas to screen
			screen.blit(self.canv3d_img, self.rect);
			
			pygame.display.flip()

if __name__ == '__main__':
	gs = GameSpace()
	gs.main()
