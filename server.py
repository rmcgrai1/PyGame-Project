from twisted.internet.defer	import DeferredQueue
from twisted.internet.protocol	import Protocol, ClientFactory, Factory
from twisted.internet		import reactor
from twisted.protocols.basic	import LineReceiver
from twisted.internet.tcp	import Port
from twisted.internet.task 		import LoopingCall
from sys			import *
import time
import json
import random

SERVER_HOST = "student00.cse.nd.edu"
SERVER_PORT = 40064

#toServerQueue = DeferredQueue()
serverDmgQueue = DeferredQueue()

class MovingObject(object):
        def __init__(self, oriSpeed):
                """dirX, dirY, dirZ should create a unit vector. oriSpeed is a list of [speed, x, y, z, dirX, dirY, dirZ, upX, upY, upZ]"""
                #self.ori = {'x': x, 'y': y, 'z': z, 'dirX': dirX, 
                self.oriSpeed = oriSpeed;
                
        def tick(self):
                self.oriSpeed[1] -= self.oriSpeed[4]*self.oriSpeed[0];
                self.oriSpeed[2] -= self.oriSpeed[5]*self.oriSpeed[0];
                self.oriSpeed[3] -= self.oriSpeed[6]*self.oriSpeed[0];

        def checkCollide(self, otherXYZ, radius):
		"""OtherXYZ is a list of [x, y, z]. Checks if otherXYZ is within radius of this object's center"""
		#1 vs 0 , 2 vs 1, 3 vs 2 is intentional.
		dx = self.oriSpeed[1] - otherXYZ[0];
		dy = self.oriSpeed[2] - otherXYZ[1];
		dz = self.oriSpeed[3] - otherXYZ[2];
		dist_squared = dx*dx + dy*dy + dz*dz;
		if (dist_squared < (radius * radius)):
			return True
		else:
			return False

# Each player has one entry, their id.
# newLaserList[self.id] = [a list of all the lasers self.id doesn't know exist yet]
newLaserList = {}
laserList = []
posDict = {};
deathDict = {};

#Asteroids have size, position, orientation
asteroidList = [];

class Asteroid(object):
	def __init__(self, a_id, radius, posXYZ, rotXYZ):
		self.a_id = a_id;
		self.radius = radius;
		self.x = posXYZ[0];
		self.y = posXYZ[1];
		self.z = posXYZ[2];
		self.rotX = rotXYZ[0];
		self.rotY = rotXYZ[1];
		self.rotZ = rotXYZ[2];
		self.cooldown = 0;

	def tick(self):
		if (self.cooldown > 0):
			self.cooldown -= 1;
	
	def checkCollide(self, otherXYZ):
		if not (self.cooldown > 0):
			dx = self.x - otherXYZ[0];
			dy = self.y - otherXYZ[1];
			dz = self.z - otherXYZ[2];
			dist_squared = dx*dx + dy*dy + dz*dz;
			if (dist_squared < (self.radius * self.radius)):
				self.cooldown = 60;
				return True;
			else:
				return False;
	def toList(self):
		"""returns [a_id, radius, x, y, z, rotX, rotY, rotZ]"""
		return [self.a_id, self.radius, self.x, self.y, self.z, self.rotX, self.rotY, self.rotZ]


def generateAsteroids():
	random.seed();
	size_range = [200, 400]
	pos_range = [-2000, 2000];
	rot_range = [0, 360];
	start_radius = 200;
	for astero_id in xrange(5):
		pos = [0, 0, 0];
		while ((pos[0] <= start_radius) and (pos[1] <= start_radius) and (pos[2] <= start_radius)):
			for size_iter in xrange(3):
				pos[size_iter] = random.randint(pos_range[0], pos_range[1]);
		rot = [0, 0, 0];
		for rot_iter in xrange(3):
			rot[rot_iter] = random.randint(rot_range[0], rot_range[1]);
		asteroidList.append(Asteroid(astero_id, 
				random.randint(size_range[0], size_range[1]),
				pos, rot));
				

class Laser(MovingObject):
        
        def __init__(self, lid, creator, maxAge, oriSpeed):
                """oriSpeed is a list of [speed, x, y, z, dirX, dirY, dirZ, upX, upY, upZ]"""
                super(Laser,self).__init__(oriSpeed);
                self.creator = creator;
                self.age = 0;
                self.maxAge = maxAge;
		self.lid = lid

        def tick(self):
		super(Laser, self).tick();
                self.age += 1;
                if (self.age > self.maxAge):
                        self.remove();
	
	def remove(self):
		del laserList[laserList.index(self)];

	def checkCollide(self, otherXYZ, radius, attacker_id):
		if not (attacker_id == self.creator):
			return super(Laser, self).checkCollide(otherXYZ, radius)
                
def serverLoop():
	"""All collision detection goes here; the server is in charge of synced events like this"""
        for laser in laserList:
                laser.tick();
		for player in posDict:
			if not deathDict[player]:
				if laser.checkCollide(posDict[player][:3], 50, player):
				        #print 'You hit player', player;
				        #print posDict[player][:3]
					serverDmgQueue.put(['playerShot',player, laser.creator, laser.lid]);
					laser.remove();
				

	for asteroid in asteroidList:
		asteroid.tick();
		for player in posDict:
			if not deathDict[player]:
				if asteroid.checkCollide(posDict[player][:3]):
					serverDmgQueue.put(['asterCollide', player])

class ServerConn(LineReceiver):
	def __init__(self, parent, id, addr):
		self.parent = parent
		self.id = int(id)
		self.addr = addr
		self.lost = False;
		self.subpos = [0,0,0, 0,0,1, 0,1,0]
		posDict[self.id] = self.subpos;
		deathDict[self.id] = False;
                newLaserList[self.id] = [];
		self.currentLaserID = 0;
		
	def lineReceived(self, data):
		"""Overwrites Protocol's method for handling when data is received from the connected address. Any data received is put into the 'toServerQueue', and will be passed along to the server."""
		#toServerQueue.put(data)
		#print data

		jso = json.loads(data)
		type = jso['type']

		if type == 'pos':
			otherSubPos = jso['one']

			for i in range(0, 9):
				self.subpos[i] = otherSubPos[i]

		if type == 'pos' or type == 'init':
			#temporary: convert dict to list
			#tempPosList = [];
			#for player in posDict.values():
			#	tempPosList.append(player)
			self.transport.write(json.dumps({
				"type": "pos",
				"all": posDict
			}) + "\r\n")
                elif type == 'laser':
			#print "I'm a firing mah lazorz"
                        oriSpeed = jso['oriSpeed'];
                        maxAge = int(jso['maxAge']);
                        laserList.append(Laser(self.currentLaserID, self.id, maxAge, oriSpeed[:]));
                        for player in newLaserList.values():
                                player.append([self.currentLaserID,maxAge, oriSpeed]);
			self.currentLaserID += 1;
				#print "Appending!"
			
		elif type == "destroyed":
			deathDict[self.id] = True;

		#print newLaserList;
		playerLasers = [];
		playerLasers = newLaserList[self.id];
		
		for laser in playerLasers:
			#print "This should really only happen once"
			self.transport.write(json.dumps({
						"type" : "laser",
						"lid" : laser[0],
						"maxAge" : laser[1],
						"oriSpeed" : laser[2]
						}) + "\r\n");
			del playerLasers[playerLasers.index(laser)];

	def toClientCallback(self, data):
		"""Callback that runs for each item in the 'toClientQueue'. Any data in the queue came from the server, and will automatically be passed along to the client."""		
		self.transport.write(data)
		#toClientQueue.get().addCallback(self.toClientCallback)

	def connectionMade(self):
		"""Overwrites Protocol's method for handling when a connection is made. It prints a line about the connected address, and then attaches the callback to 'toClientQueue'. Lastly, the connection to the server is started!"""
		print "connection received from", self.addr
		tempAsteroids = [];
		for asteroid in asteroidList:
			tempAsteroids.append(asteroid.toList())
		self.transport.write(json.dumps({
			"type":	"init",
			"id" : self.id,
			"all_ids":  posDict.keys(),
			"asteroids" : tempAsteroids 
		}) + "\r\n")

		print "id: " + str(self.id)

		#toClientQueue.get().addCallback(self.toClientCallback)

	def connectionLost(self, reason):
		"""Overwrites Protocol's method for handling when a connection is lost. When the connection to the client is lost, it automatically prints a message and stops the reactor."""
		print "connection lost from", self.addr

		s = json.dumps({
			"type": "del",
			"id": self.id
		})+"\r\n"

#		self.lost = True;
#		try:
#			print "deleting", self.id
		del posDict[self.id]
		del deathDict[self.id];
		del newLaserList[self.id];
#		except KeyError:
#			print "Key error when deleting from posDict or newLaserList. Key was", self.id, "length of newLaserList was", len(newLaserList), "length of posDict was", len(posDict);

#		print "There are now ", len(newLaserList), "objects in newLaserList"

		for conn in self.parent.conns.values():
			if not (conn == self):
				conn.transport.write(s)
		
		del self.parent.conns[self.id]
		#self.parent.conns.remove(self)
		self.parent = None

class ServerConnFactory(Factory):
	def __init__(self):
		self.currentID = 0;
		self.conns = {}
		serverDmgQueue.get().addCallback(self.sendDamage);
		generateAsteroids();
	def sendDamage(self, data):
		"""data is a list of [damageType, damageArgs]. asterCollide has damaged_id, playerShot has damaged_id, attacker_id, lid"""
		if (data[0] == 'playerShot'):
			s = json.dumps( {
					'type' : 'playerDmg',
					'damaged' : data[1],
					'attacker' : data[2],
					'lid' : data[3]
					}) + "\r\n"
		elif (data[0] == 'asterCollide'):
			s = json.dumps( {
					'type' : 'colDmg',
					'damaged' : data[1]
					}) + "\r\n"
		for conn in self.conns.values():
			conn.transport.write(s)
		serverDmgQueue.get().addCallback(self.sendDamage);

	def buildProtocol(self, addr):
		"""Overwrites ClientFactory's method for building Protocols. It creates a ProxyToClientConn Protocol and adds it to the factory object so the other factory can access it."""
		conn = ServerConn(self, self.currentID, addr)
		self.conns[self.currentID] = conn
		self.currentID = self.currentID + 1;
		return conn


if __name__ == '__main__':
        lc = LoopingCall(serverLoop);
        lc.start(1./60);

	reactor.listenTCP(SERVER_PORT, ServerConnFactory())
	reactor.run()
