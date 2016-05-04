import sys
import os
import pygame
import math
import time
import random
from pygame.locals				import *
from src						import *
from drawable					import *
from deathstar					import *
from earth						import *
from player						import *
from earthchunk					import *
from sprite						import *
from math2						import *
from explosion					import *
from mat						import *
from skybox						import *
from arwing						import *
from arwing_player				import *
from twisted.internet.protocol	import Protocol, ClientFactory, Factory
from twisted.internet.task 		import LoopingCall
from twisted.internet			import reactor
from twisted.protocols.basic	import LineReceiver
from twisted.internet.tcp		import Port
from twisted.internet.defer import DeferredQueue
from sys						import *
from radar						import *
from hud						import *
from laser						import *
import json
import gfx2d

SERVER_HOST = "student00.cse.nd.edu"
SERVER_PORT_A = 40076
SERVER_PORT_B = 40064

#toServerQueue = DeferredQueue()

arwingInsts = {};

class ClientConnection(LineReceiver):
	def __init__(self, addr):
		self.addr = addr;
		self.gs = GameSpace.instance
		self.gs.mainQueue.get().addCallback(self.sendLaser);

	def sendLaser(self, laserOri):
		self.transport.write(json.dumps({
			"type": "laser",
			"maxAge": 60 * 10,
			"oriSpeed": [30,
				 laserOri[0],laserOri[1],laserOri[2],
				 laserOri[3],laserOri[4],laserOri[5],
				 laserOri[6],laserOri[7],laserOri[8] ]
		})+ "\r\n");
		self.gs.mainQueue.get().addCallback(self.sendLaser);

	def lineReceived(self, data):
		#print 'received, ', data
		
		try:
			jso = json.loads(data)
		except:
			print "invalid json: " + data
			return
		type = jso['type']
		
		gs = GameSpace.instance
		
		if type == 'init':
			gs.id = int(jso['id'])
			player_ids = jso['all_ids']
			print "converted json:", jso;

			for player_id in player_ids:
				if not (player_id == gs.id):
					arwingInsts[player_id] = gs.instanceAppend(Arwing(gs, 0,0,0))
					print "INIT APPEND", player_id
#			for i in range(0, jso['num_players']):
#				arwingInsts.append(  gs.instanceAppend(Arwing(gs, 0,0,0))  )
			arwingInsts[gs.id] = gs.player;
			
			self.transport.write(json.dumps({
				"type": type,
				"result": "ok"
			}) + "\r\n");
		elif type == 'pos':
			all_dict = jso['all'] #all is a dictionary
			
#			le = len(all)
#			leA = len(arwingInsts)
			
#			while leA < le:
#				arwingInsts.append(  gs.instanceAppend(Arwing(gs, 0,0,0))  )
#				leA += 1
			
#			i = 0;
			for player_id in all_dict:
				if not(int(player_id) == gs.id):
					if int(player_id) not in arwingInsts.keys():
						arwingInsts[int(player_id)] = (gs.instanceAppend(Arwing(gs, 0,0,0)))
						#print "APPEND: gs id:", gs.id, "player_id", player_id;
						#print "pos json:", jso
					
					inst = arwingInsts[int(player_id)];
					allInst = all_dict[player_id]
					for ii in range(0, 9):
						inst.ori[ii] = allInst[ii];


#			for i in range(0, le):
#				if not (i == gs.id):
#					for ii in range(0, 9):
#						inst = arwingInsts[i]
#						allInst = all[i]
#						inst.ori[ii] = allInst[ii]
		
			self.transport.write(json.dumps({
				"type": type,
				"one": gs.player.ori.tolist()
			}) + "\r\n");
		elif type == 'del':
			pid = int(jso['id'])
			arw = arwingInsts[pid];
			gs.instanceRemove(arw);
			del arwingInsts[pid];				  

#			if id < len(arwingInsts):				
#				if id < gs.id:
#					gs.id -= 1
#					
#				arw = arwingInsts[id]
#				
#				gs.instanceRemove(arw)
#				del arwingInsts[id]
		elif type == 'laser':
			oriSpeed = jso["oriSpeed"];
			maxAge = jso["maxAge"]
			gs.instanceAppend(Laser(gs,oriSpeed[0], maxAge,
					oriSpeed[1],oriSpeed[2],oriSpeed[3],
					oriSpeed[4]+oriSpeed[1],
					oriSpeed[5]+oriSpeed[2],
					oriSpeed[6]+oriSpeed[3],
					oriSpeed[7],oriSpeed[8],oriSpeed[9]
			))
		elif type == 'takeDmg':
			pid = int(jso['id'])
			if (pid == gs.id):
				print "I, player", gs.id, "took damage!"
			else:
				print "I saw player", gs.id, "take damage!"
	def connectionMade(self):
		print 'new connection made to ' + str(self.addr)
		GameSpace.instance.isConnected = True
	def connectionLost(self, reason):
		print 'lost connection to ' + str(self.addr)
		GameSpace.instance.isConnected = False

class ClientConnFactory(ClientFactory):

	def buildProtocol(self, addr):
		self.conn = ClientConnection(addr);
		return self.conn

class GameSpace:			
	def __init__(self):
		GameSpace.instance = self
		self.clientConnFactory = ClientConnFactory()
		self.id = -1
		self.mainQueue = DeferredQueue();
				
		Laser.preload();

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

	def quitGame(self):
		if reactor.running:
			reactor.stop()
		pygame.mixer.quit()

	def main(self):
		self.isConnected = False
		self.connectTimer = 0
                #Ryan is True, Jacob is False. (Never trust a Jacob, for it is False)
		self.connectChoice = False;
                
		self.connectTimerMax = 75
		self.connectDiv = 16
		
		#1. Initialize game space

		pygame.init()
		pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096) #4096
		
		self.resolution = self.width,self.height = (640,480)
		self.screen = pygame.display.set_mode(self.resolution)
		gfx2d.init()


		self.instanceList = []
		
		self.keyHDir = 0
		self.keyVDir = 0
		self.mDown = False
		self.brake = False
		self.brakeLock = False

		#2. Create game objects

		self.canv3d_near = .1
		self.canv3d_far = 5000
		self.canv3d_width = 320
		self.canv3d_height = 240
		self.canv3d_aspect = self.canv3d_width/self.canv3d_height
		self.canv3d_doFog = 0
                
		self.mouse_center_x = self.width/2;
		self.mouse_center_y = self.height/2;
		
		self.clock = pygame.time.Clock()	
		self.skybox = self.instanceAppend(Skybox(self, "img/orbital-element_lf.jpg","img/orbital-element_rt.jpg","img/orbital-element_ft.jpg","img/orbital-element_bk.jpg","img/orbital-element_up.jpg","img/orbital-element_dn.jpg"))
		self.reticle = self.instanceAppend(Reticle(self.mouse_center_x, self.mouse_center_y));
		self.radar = self.instanceAppend(Radar(self));
		self.player = self.instanceAppend(ArwingPlayer(self, 0,0,0))
		self.hud = self.instanceAppend(Hud(self))

		# Create 3d Canvas
		self.canv3d_img_ = pygame.Surface((self.canv3d_width,self.canv3d_height)).convert_alpha()
		canv3d.init(self.canv3d_width,self.canv3d_height, self.canv3d_near, self.canv3d_far, self.canv3d_doFog, pygame.surfarray.pixels2d(self.canv3d_img_));
		
		self.cameraMethod = 2;
		if (self.cameraMethod == 1):
			pygame.mouse.set_visible(False);
			pygame.event.set_grab(True);
			#pygame.mouse.set_pos(mouse_center_x, mouse_center_y);
		elif (self.cameraMethod == 2):
			pygame.mouse.set_visible(False);

			
	
	#3. Game Loop
	def gameLoop(self):
		if not self.isConnected:
			if self.connectTimer == 0:
				if self.connectChoice:
					reactor.connectTCP(SERVER_HOST, SERVER_PORT_A, ClientConnFactory());
				else:
					reactor.connectTCP(SERVER_HOST, SERVER_PORT_B, ClientConnFactory());
				self.connectChoice = not self.connectChoice;
				self.connectTimer = self.connectTimerMax
			else:
				self.connectTimer -= 1
		
		#4. Tick regulation
		#self.clock.tick(60);

			
		#5. User input reading
		if (self.cameraMethod == 1):
				pygame.mouse.set_pos(self.mouse_center_x, self.mouse_center_y);
		self.mDown = pygame.mouse.get_pressed()[0]
		mdx, mdy = 0, 0
		md_adjust = 1;
		

		if (self.cameraMethod == 2):
				mdx, mdy = pygame.mouse.get_pos();
				mdx = mdx - self.mouse_center_x;
				mdy = mdy - self.mouse_center_y;
				md_adjust = 1.0/128;

		for event in pygame.event.get():
			if (event.type == pygame.MOUSEMOTION):
				if (self.cameraMethod == 1):
					mdx, mdy = event.rel;
					md_adjust = 1.0/6;
			elif event.type == QUIT:
				self.quitGame()
			elif event.type == KEYDOWN:
				if(event.key == pygame.K_a):
					self.keyHDir -= 1
				elif(event.key == pygame.K_d):
					self.keyHDir += 1
				elif(event.key == pygame.K_w):
					self.keyVDir -= 1
				elif(event.key == pygame.K_s):
					self.keyVDir += 1
				elif(event.key == pygame.K_v):
					self.brake = True;
					print "Braking"
				elif(event.key == pygame.K_ESCAPE):
					self.quitGame()
			elif event.type == KEYUP:
				if(event.key == pygame.K_a):
					self.keyHDir += 1
				elif(event.key == pygame.K_d):
					self.keyHDir -= 1
				elif(event.key == pygame.K_w):
					self.keyVDir += 1
				elif(event.key == pygame.K_s):
					self.keyVDir -= 1
				elif(event.key == pygame.K_v):
					if not self.brakeLock:
						self.brake = False;
				elif(event.key == pygame.K_b):
					if not self.brakeLock:
						self.brakeLock = True;
						self.brake = True;
					else:
						self.brakeLock = False;
						self.brake = False;


		#6. Tick updating and polling

		input = {
			"mouse_down": self.mDown,
			"mouse_dy": mdy,
			"mouse_dx": mdx,
			"mouse_d_adjust": md_adjust,
			"key_hdir": self.keyHDir,
			"key_vdir": self.keyVDir,
			"brake" : False,
			"freeze_signal" : self.brake
		}
			

		for d in self.instanceList:
			d.tick(input)


		#7. Display

		self.screen.fill(gfx2d.COLOR_WHITE)
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
			d.draw(self.screen)


		# Resize 3d canvas to match screen size
		self.canv3d_img = pygame.transform.scale(self.canv3d_img_, self.resolution)
		self.rect = self.canv3d_img.get_rect()			

		# Blit 3d canvas to screen
		self.screen.blit(self.canv3d_img, self.rect);
		self.reticle.blitToScreen(self.screen);
		self.radar.blitToScreen(self.screen);
		self.hud.blitToScreen(self.screen)
		
		pygame.display.flip()
			
			
class Reticle:
        def __init__(self, centerX, centerY):
                self.small = pygame.image.load("img/Crosshairs_Small.png");
                self.smallRect = self.small.get_rect();
                self.smallRect.center = (centerX, centerY);
                self.large = pygame.image.load("img/Crosshairs_Large.png");
                self.largeRect = self.large.get_rect();
                self.largeRect.center = (centerX, centerY);
                self.centerX = centerX;
                self.centerY = centerY;

        #dx and dy are the distance from the center
        def tick(self, input):
                reticleLag = 0.80;
                self.smallRect.center = (self.centerX+input['mouse_dx'], self.centerY+input['mouse_dy']);
                self.largeRect.center = (self.centerX + input['mouse_dx']*reticleLag, self.centerY + input['mouse_dy']*reticleLag);
        
        def draw(self, screen):
                pass;

        def blitToScreen(self, screen):
                screen.blit(self.small, self.smallRect);
                screen.blit(self.large, self.largeRect);

if __name__ == '__main__':
	gs = GameSpace()
	
	gs.main()
	lc = LoopingCall(gs.gameLoop)
	lc.start(1./60)
	
	reactor.run()
