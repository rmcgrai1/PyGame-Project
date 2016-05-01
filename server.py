# Ryan McGrail
# 4/22/16
# PROXY

from twisted.internet.defer	import DeferredQueue
from twisted.internet.protocol	import Protocol, ClientFactory, Factory
from twisted.internet		import reactor
from twisted.protocols.basic	import LineReceiver
from twisted.internet.tcp	import Port
from sys			import *


PROXY_HOST = "127.0.0.1"
PROXY_PORT = 40076

SERVER_HOST = "student02.cse.nd.edu"
SERVER_PORT = 40001


toClientQueue = DeferredQueue()
toServerQueue = DeferredQueue()

class ProxyToServerConn(Protocol):
	def __init__(self, addr):
		self.addr = addr

	def dataReceived(self, data):
		"""Overwrites Protocol's method for handling when data is received from the connected address. Any data received is put into the 'toClientQueue', and will be passed along to the client."""
		toClientQueue.put(data)

	def toServerCallback(self, data):
		"""Callback that runs for each item in the 'toServerQueue'. Any data in the queue came from the client, and will automatically be passed along to the server."""
		self.transport.write(data)
		toServerQueue.get().addCallback(self.toServerCallback)

	def connectionMade(self):
		"""Overwrites Protocol's method for handling when a connection is made. It prints a line about the connected address, and then attaches the callback to 'toServerQueue'."""
		print "connection made to", SERVER_HOST, "port", SERVER_PORT
		toServerQueue.get().addCallback(self.toServerCallback)

	def connectionLost(self, reason):
		"""Overwrites Protocol's method for handling when a connection is lost. When the connection to the server is lost, it automatically disconnects the connection to the client."""
		toClientFactory.conn.transport.loseConnection()

class ProxyToServerConnFactory(ClientFactory):
	def buildProtocol(self, addr):
		"""Overwrites ClientFactory's method for building Protocols. It creates a ProxyToServerConn Protocol and adds it to the factory object so the other factory can access it."""
		self.conn = ProxyToServerConn(addr)
		return self.conn


class ProxyToClientConn(Protocol):
	def __init__(self, addr):
		self.addr = addr

	def dataReceived(self, data):
		"""Overwrites Protocol's method for handling when data is received from the connected address. Any data received is put into the 'toServerQueue', and will be passed along to the server."""
		toServerQueue.put(data)

	def toClientCallback(self, data):
		"""Callback that runs for each item in the 'toClientQueue'. Any data in the queue came from the server, and will automatically be passed along to the client."""		
		self.transport.write(data)
		toClientQueue.get().addCallback(self.toClientCallback)

	def connectionMade(self):
		"""Overwrites Protocol's method for handling when a connection is made. It prints a line about the connected address, and then attaches the callback to 'toClientQueue'. Lastly, the connection to the server is started!"""
		print "connection received from", self.addr
		toClientQueue.get().addCallback(self.toClientCallback)
		reactor.connectTCP(SERVER_HOST, SERVER_PORT, toServerFactory)

	def connectionLost(self, reason):
		"""Overwrites Protocol's method for handling when a connection is lost. When the connection to the client is lost, it automatically prints a message and stops the reactor."""
		print "connection lost from", self.addr
		reactor.stop()

class ProxyToClientConnFactory(Factory):
	def buildProtocol(self, addr):
		"""Overwrites ClientFactory's method for building Protocols. It creates a ProxyToClientConn Protocol and adds it to the factory object so the other factory can access it."""
		self.conn = ProxyToClientConn(addr)
		return self.conn


if __name__ == '__main__':
	toServerFactory = ProxyToServerConnFactory()
	toClientFactory = ProxyToClientConnFactory()

	reactor.listenTCP(PROXY_PORT, toClientFactory)
	reactor.run()
