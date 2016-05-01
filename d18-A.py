from twisted.internet.protocol	import Protocol, ClientFactory, Factory
from twisted.internet			import reactor
from twisted.protocols.basic	import LineReceiver
from twisted.internet.tcp		import Port
from sys						import *


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 40076


class ClientConnection(Protocol):
	def dataReceived(self, data):
		"""Overwrites Protocol's method for handling data reception. When the server responds to our get request, the ClientConnection gets the response data passed to this method, and it is printed from within."""

		print 'received, ', data


	def connectionMade(self):
		"""Overwrites Protocol's method for responding to a successful connection. As soon as a connection has been made to a server, sends the GET string header to the server in order to complete the request."""

		print 'new connection made to {0} port {1}'.format(SERVER_HOST, SERVER_PORT)
		self.transport.write(GET_STRING)


	def connectionLost(self, reason):
		"""Overwrites Protocol's method for responding to a lost connection. When the connection is lost, either intentionally or unintentionally, this method will run and stop the reactor from running any longer."""

		print 'lost connection to {0} port {1}'.format(SERVER_HOST, SERVER_PORT)
		reactor.stop()



class ClientConnFactory(ClientFactory):
	def buildProtocol(self, addr):
		"""Overwrites ClientFactory's method for building protocols. Rather than use a normal Protocol, uses the ClientConnection class."""

		return ClientConnection()



if __name__ == '__main__':
	reactor.connectTCP(SERVER_HOST, SERVER_PORT, ClientConnFactory())
	reactor.run()
