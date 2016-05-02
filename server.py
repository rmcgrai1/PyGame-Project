from twisted.internet.defer	import DeferredQueue
from twisted.internet.protocol	import Protocol, ClientFactory, Factory
from twisted.internet		import reactor
from twisted.protocols.basic	import LineReceiver
from twisted.internet.tcp	import Port
from sys			import *
import time
import json

SERVER_HOST = "student00.cse.nd.edu"
SERVER_PORT = 40064

#toServerQueue = DeferredQueue()


class MovingObject(Object):
        def __init__(self, oriSpeed):
                """dirX, dirY, dirZ should create a unit vector. oriSpeed is a list of [speed, x, y, z, dirX, dirY, dirZ, upX, upY, upZ]"""
                #self.ori = {'x': x, 'y': y, 'z': z, 'dirX': dirX, 
                self.oriSpeed = oriSpeed;
                
        def tick(self):
                self.ori[1] += self.ori[4]*self.speed;
                self.ori[2] += self.ori[5]*self.speed;
                self.ori[3] += self.ori[6]*self.speed;

        def checkCollide(self, other_stuff):
                pass;

newLaserList = []
laserList = []

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
                        del laserList[laserList.index(self)];
                
def serverLoop():
        for laser in laserList:
                laser.tick();

posList = []
class ServerConn(Protocol):
	def __init__(self, parent, id, addr):
		self.parent = parent
		self.id = id
		self.addr = addr
		self.subpos = [0,0,0, 0,0,1, 0,1,0]
		posList.append(self.subpos)
                newLaserList.append([])

	def dataReceived(self, data):
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
			self.transport.write(json.dumps({
				"type": "pos",
				"all": posList
			}) + "\r\n")
                elif type == 'laser':
                        oriSpeed = jso['oriSpeed'];
                        maxAge = jso['maxAge'];
                        laserList[self.id].append(Laser(self.id, maxAge, oriSpeed.copy()));
                        for player in newLaserList:
                                newLaserList.append([maxAge, oriSpeed]);
                        for laser in newLaserList[self.id]:
                                self.transport.write(json.dumps({
                                        "type" : "laser",
                                        "maxAge" : laser[0],
                                        "oriSpeed" : laser[1],
                                        }) + "\r\n";
                                del laser;
                        

	def toClientCallback(self, data):
		"""Callback that runs for each item in the 'toClientQueue'. Any data in the queue came from the server, and will automatically be passed along to the client."""		
		self.transport.write(data)
		#toClientQueue.get().addCallback(self.toClientCallback)

	def connectionMade(self):
		"""Overwrites Protocol's method for handling when a connection is made. It prints a line about the connected address, and then attaches the callback to 'toClientQueue'. Lastly, the connection to the server is started!"""
		print "connection received from", self.addr
		self.transport.write(json.dumps({
			"type":	"init",
			"id": 	self.id
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

		del posList[self.id]

		for conn in self.parent.conns:
			if not (conn == self):
				if conn.id > self.id:
					conn.id -= 1

				conn.transport.write(s)

		self.parent.conns.remove(self)
		self.parent = None

class ServerConnFactory(Factory):
	def __init__(self):
		self.conns = []

	def buildProtocol(self, addr):
		"""Overwrites ClientFactory's method for building Protocols. It creates a ProxyToClientConn Protocol and adds it to the factory object so the other factory can access it."""
		conn = ServerConn(self, len(self.conns), addr)
		self.conns.append(conn)
		return conn


if __name__ == '__main__':
        lc = LoopingCall(serverLoop);
        lc.start(1./60);

	reactor.listenTCP(SERVER_PORT, ServerConnFactory())
	reactor.run()
