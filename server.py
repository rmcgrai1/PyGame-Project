from twisted.internet.defer	import DeferredQueue
from twisted.internet.protocol	import Protocol, ClientFactory, Factory
from twisted.internet		import reactor
from twisted.protocols.basic	import LineReceiver
from twisted.internet.tcp	import Port
from twisted.internet.task 		import LoopingCall
from sys			import *
import time
import json

SERVER_HOST = "student00.cse.nd.edu"
SERVER_PORT = 40064

#toServerQueue = DeferredQueue()


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

class Laser(MovingObject):
        
        def __init__(self, creator, maxAge, oriSpeed):
                """oriSpeed is a list of [speed, x, y, z, dirX, dirY, dirZ, upX, upY, upZ]"""
                super(Laser,self).__init__(oriSpeed);
                self.creator = creator;
                self.age = 0;
                self.maxAge = maxAge;

        def tick(self):
		super(Laser, self).tick();
                self.age += 1;
                if (self.age > self.maxAge):
                        self.remove();
	
	def remove(self):
		del laserList[laserList.index(self)];

	def checkCollide(self, otherXYZ, radius, player_id):
		if not (player_id == self.creator):
			return super(Laser, self).checkCollide(otherXYZ, radius)
                
def serverLoop():
        for laser in laserList:
                laser.tick();
		for player in posDict:
			if laser.checkCollide(posDict[player][:3], 50, player):
				print 'You hit player', player;
				print posDict[player][:3]
				laser.remove();
				


class ServerConn(LineReceiver):
	def __init__(self, parent, id, addr):
		self.parent = parent
		self.id = int(id)
		self.addr = addr
		self.lost = False;
		self.subpos = [0,0,0, 0,0,1, 0,1,0]
		posDict[self.id] = self.subpos;
                newLaserList[self.id] = [];

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
                        laserList.append(Laser(self.id, maxAge, oriSpeed[:]));
                        for player in newLaserList.values():
                                player.append([maxAge, oriSpeed]);
				#print "Appending!"
                        
		#print newLaserList;
		if self.lost:
			print "WTF, MATE"
		playerLasers = [];
		try:
			playerLasers = newLaserList[self.id];
		except:
			print "DERRRR", self.addr;
		for laser in playerLasers:
			#print "This should really only happen once"
			self.transport.write(json.dumps({
						"type" : "laser",
						"maxAge" : laser[0],
						"oriSpeed" : laser[1],
						}) + "\r\n");
			del playerLasers[playerLasers.index(laser)];

	def toClientCallback(self, data):
		"""Callback that runs for each item in the 'toClientQueue'. Any data in the queue came from the server, and will automatically be passed along to the client."""		
		self.transport.write(data)
		#toClientQueue.get().addCallback(self.toClientCallback)

	def connectionMade(self):
		"""Overwrites Protocol's method for handling when a connection is made. It prints a line about the connected address, and then attaches the callback to 'toClientQueue'. Lastly, the connection to the server is started!"""
		print "connection received from", self.addr
		self.transport.write(json.dumps({
			"type":	"init",
			"id" : self.id,
			"all_ids":  posDict.keys()
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
		del newLaserList[self.id];
#		except KeyError:
#			print "Key error when deleting from posDict or newLaserList. Key was", self.id, "length of newLaserList was", len(newLaserList), "length of posDict was", len(posDict);

#		print "There are now ", len(newLaserList), "objects in newLaserList"

		for conn in self.parent.conns:
			if not (conn == self):
				conn.transport.write(s)

		self.parent.conns.remove(self)
		self.parent = None

class ServerConnFactory(Factory):
	def __init__(self):
		self.currentID = 0;
		self.conns = []

	def buildProtocol(self, addr):
		"""Overwrites ClientFactory's method for building Protocols. It creates a ProxyToClientConn Protocol and adds it to the factory object so the other factory can access it."""
		conn = ServerConn(self, self.currentID, addr)
		self.conns.append(conn)
		self.currentID = self.currentID + 1;
		return conn


if __name__ == '__main__':
        lc = LoopingCall(serverLoop);
        lc.start(1./60);

	reactor.listenTCP(SERVER_PORT, ServerConnFactory())
	reactor.run()
