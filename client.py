import sys
import os
import pygame
import math
import time
import random
from pygame.locals				import *
from drawable					import *
from player						import *
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
from hud						import *
from laser						import *
import json
import gfx2d
from  asteroid import *

SERVER_HOST = "student00.cse.nd.edu"
SERVER_PORT_A = 40076
SERVER_PORT_B = 40064

#toServerQueue = DeferredQueue()

laserInsts = {};

class ClientConnection(LineReceiver):
	def __init__(self, addr):
		self.rogue_shot = -1;
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
			temp_aster = jso['asteroids']
			gs.addMessage("You are player " + str(gs.id) + ".")

			for player_id in player_ids:
				if not (player_id == gs.id):
					gs.arwingInsts[player_id] = gs.instanceAppend(Arwing(gs, 0,0,0))
					#print "INIT APPEND", player_id
#			for i in range(0, jso['num_players']):
#				gs.arwingInsts.append(  gs.instanceAppend(Arwing(gs, 0,0,0))  )
			gs.arwingInsts[gs.id] = gs.player;
			
			for asteroid in temp_aster:
				
				gs.instancePrepend(Asteroid(asteroid[0], asteroid[1], asteroid[2], asteroid[3], asteroid[4], asteroid[5], asteroid[6], asteroid[7]));

			self.transport.write(json.dumps({
				"type": type,
				"result": "ok"
			}) + "\r\n");
		elif type == 'pos':
			all_dict = jso['all'] #all is a dictionary
			
#			le = len(all)
#			leA = len(gs.arwingInsts)
			
#			while leA < le:
#				gs.arwingInsts.append(  gs.instanceAppend(Arwing(gs, 0,0,0))  )
#				leA += 1
			
#			i = 0;
			firstTime = (len(all_dict) == 0)

			for player_id in all_dict:
				if not(int(player_id) == gs.id):
					if int(player_id) not in gs.arwingInsts.keys():
						gs.arwingInsts[int(player_id)] = (gs.instanceAppend(Arwing(gs, 0,0,0)))
						
						if not firstTime:
							gs.addMessage("Player " + player_id + " joined the game.")

						
						#print "APPEND: gs id:", gs.id, "player_id", player_id;
						#print "pos json:", jso
					
					inst = gs.arwingInsts[int(player_id)];
					allInst = all_dict[player_id]
					for ii in range(0, 9):
						inst.ori[ii] = allInst[ii];		
			self.transport.write(json.dumps({
				"type": type,
				"one": gs.player.ori.tolist()
			}) + "\r\n");
		elif type == 'del':
			pid = int(jso['id'])
			arw = gs.arwingInsts[pid];
			gs.instanceRemove(arw);
			del gs.arwingInsts[pid];				  

			gs.addMessage("Player " + str(pid) + " left the game.")
			
		elif type == 'laser':
			oriSpeed = jso["oriSpeed"];
			maxAge = jso["maxAge"]
			lid = jso["lid"];
			if (self.rogue_shot == lid):
				print "Stopped Rogue Shot from firing"
				self.rogue_shot = -1;
			else:
				laserInsts[lid] = gs.instanceAppend(Laser(gs, oriSpeed[0], maxAge,
									oriSpeed[1],oriSpeed[2],oriSpeed[3],
									oriSpeed[4]+oriSpeed[1],
									oriSpeed[5]+oriSpeed[2],
									oriSpeed[6]+oriSpeed[3],
									oriSpeed[7],oriSpeed[8],oriSpeed[9]
			))
		elif type == 'playerDmg':
			damaged = int(jso['damaged'])
			attacker = int(jso['attacker'])
			lid = int(jso['lid'])
			try:
				gs.arwingInsts[damaged].hurt();
			except KeyError as ex:
				print "The damaged ship has left the game!"
			try: 
				#Update points here
				gs.arwingInsts[attacker].addPoints(10);
				if (gs.arwingInsts[damaged].hp <= 0):
					gs.arwingInsts[attacker].addPoints(50);
					if (damaged == gs.id):
						self.transport.write(json.dumps(
						{
							"type" : "destroyed"
						}) + "\r\n");
						#send message to server
			except KeyError as ex:
				print "The attacker has left the game!"
			
			try:
				las = laserInsts[lid];
				gs.instanceRemove(las);
				del laserInsts[lid];
			except KeyError as ex:
				print "Rogue Shot Created, lid:", lid
				self.rogue_shot = lid;
			#print "Removed Laser"
		elif type == "colDmg":
			damaged = int(jso['damaged']);
			gs.arwingInsts[damaged].hurt();
			if (damaged == gs.id):
				if (gs.arwingInsts[damaged].hp <= 0):
					self.transport.write(json.dumps(
							{"type" : "destroyed" }) + "\r\n");

			
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
		self.arwingInsts = {};

		pygame.init()
		pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)		
		
		# Load music, and play it
		self.musFight = pygame.mixer.Sound("snd/musicLoop.ogg")
		self.musFight.set_volume(.35)
		self.musFight.play(-1)

				
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
               
		#Ryan is True, Jacob is False.
		self.connectChoice = False;        
		self.connectTimerMax = 75
		self.connectDiv = 16
		
		#1. Initialize game space		
		self.resolution = self.width,self.height = (640,480)
		self.screen = pygame.display.set_mode(self.resolution)
		gfx2d.init()


		self.instanceList = []
		
		self.keyHDir = 0
		self.keyVDir = 0
		self.mDown = False
		self.brake = False
		self.brakeLock = False
		self.respawn = False;
		self.barrel_roll = False;

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
				elif(event.key == pygame.K_c):
					if not self.brakeLock:
						self.brakeLock = True;
						self.brake = True;
					else:
						self.brakeLock = False;
						self.brake = False;
				elif(event.key == pygame.K_r):
					self.respawn = True;
				elif(event.key == pygame.K_b):
					self.barrel_roll = True;

		#6. Tick updating and polling

		input = {
			"mouse_down": self.mDown,
			"mouse_dy": mdy,
			"mouse_dx": mdx,
			"mouse_d_adjust": md_adjust,
			"key_hdir": self.keyHDir,
			"key_vdir": self.keyVDir,
			"brake" : False,
			"freeze_signal" : self.brake,
			"respawn" : self.respawn,
			"barrel_roll" : self.barrel_roll
		}
		self.respawn = False;
		self.barrel_roll = False;
			

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
		canv3d.addMatPerspective(MAT_P, .75)
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
		self.hud.blitToScreen(self.screen)
		
		pygame.display.flip()
	
	def addMessage(self, txt):
		self.hud.addMessage(txt)
			
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
