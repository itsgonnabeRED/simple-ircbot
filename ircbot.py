import socket
import atexit

class IrcBot:
	def __init__(self, name, network, port):
		self.name = name
		self.network = network
		self.port = port
		self.running = False
		""" Hooks """
		# Called on server connect. no params
		self.OnServerConnect = None
		# Called every time there is a chance to do something
		self.OnTick = None
		self.OnJoin = None
		self.OnMessage = None
	
	"""
	Connects to the irc server and begins accepting and sending messages
	"""
	def run(self):
		self.connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.connection.connect( (self.network, self.port) )
		self.running = True
		atexit.register(self.stop)
		# Read intro data (motd, etc)
		self.connection.recv(4096)
		self.change_nick(self.name)
		self.__send_raw_message('USER %s %s %s :%s' % (self.name, self.name, self.name, self.name))
		self.__loop()

	"""
	Sends and receives messages
	"""
	def __loop(self):
		self.__OnServerConnect()
		while self.running:
			data = self.connection.recv(4096)
			self.__OnTick()
			# Heartbeat
			if data.find('PING') != -1:
				self.__send_raw_message('PONG ' + data.split()[1])
			else:
				self.__handle_input(data)
	
	"""
	Searches for known protocol messages and calls the appropriate hooks
	"""
	def __handle_input(self, data):
		#print data
		data = data.strip(' \n\r')
		print data
		if data.find('PRIVMSG') != -1:
			nick = data.split('!')[0][1:]
			message = ' '.join(data.split(' ')[3:])[1:] 
			destination = data.split(' ')[2]
			self.__OnMessage(nick, message, destination)
		elif data.find('JOIN') != -1:
			name = data.split('!')[0][1:]
			channel = data.split(' ')[-1]
			self.__OnJoin(name, channel)

	"""
	Changes the bot's nickname
	"""
	def change_nick(self, name):
		self.__send_raw_message('NICK %s' % (name))
		self.name = name

	"""
	Sends a messsage to a channel (EX: #Irc) or a user
	"""
	def send_message(self, destination, message):
		self.__send_raw_message('PRIVMSG %s :%s' % (destination, message))

	def __OnServerConnect(self):
		if self.OnServerConnect:
			self.OnServerConnect()
	def __OnTick(self):
		if self.OnTick:
			self.OnTick()
	def __OnMessage(self, sender, message, dest):
		if self.OnMessage:
			self.OnMessage(sender, message, dest)
	def __OnJoin(self, name, channel):
		if self.OnJoin:
			self.OnJoin(name, channel)

	def join_channel(self, channel_id):
		self.__send_raw_message('JOIN %s' % (channel_id))

	def __send_raw_message(self, message):
		self.connection.sendall(message + '\r\n')

	def stop(self, reason="Bot shutting down."):
		if self.connection:
			self.__send_raw_message('QUIT :%s' % (reason))
			self.running = False
			self.connection.close()
			self.connection = None
