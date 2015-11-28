import socket, string, time, select

class Nolirc:
	def __init__(self):
		self.host = "irc.mibbit.net"
		self.port = 6667
		self.password = "noli_lib_irc"
		self.nick = "NoliBot"
		self.identity = "noli_lib_irc"
		self.realname = "noli_lib_irc_by_Nolialsea"
		self.channel = "#nolichan"
		self.chan = self.channel
		
		self.timeout = 1
		
		self.message_connexion = ""
		self.message_quit = ""
		
		self.sock = None
		self.connected = []
		
		self.readbuffer = ""
		
	def setServer(self, host, port):
		self.host = host
		self.port = port
		
	def setLogin(self, nick, password, identity = "", realname = ""):
		self.nick = nick
		self.password = password
		
		self.identity = identity if identity != "" else self.identity
		self.realname = realname if realname != "" else self.realname
	
	def connect(self, host=None, port=None, nick=None, password=None, identity=None, realname=None, channel = None):
		self.host = host if host != None else self.host
		self.port = port if port != None else self.port
		
		self.nick = nick if nick != None else self.nick
		self.password = password if password != None else self.password
		self.identity = identity if identity != None else self.identity
		self.realname = realname if realname != None else self.realname
		
		self.connectToServer()
		if channel != None:
			self.connectToChannel(channel)
		
	def connectToServer(self):
		self.sock = socket.socket()
		if (self.host != "") and (self.port != 0):
			self.sock.connect((self.host, self.port))
			self.sock.setblocking(0)
		else:
			print("error : no sock and/or port definied")
			return None
		
		self.sock.send(bytes("PASS %s\r\n" % self.password, "UTF-8"))
		self.sock.send(bytes("NICK %s\r\n" % self.nick, "UTF-8"))
		self.sock.send(bytes("USER %s %s bla :%s\r\n" % (self.identity, self.host, self.realname), "UTF-8"))
		time.sleep(1)
		
		self.readbuffer = self.readbuffer+self.sock.recv(1024).decode("utf-8")
		temp = self.readbuffer.split ("\n")
		self.readbuffer = temp.pop()
		
		for line in temp:
			line= line.rstrip()
			line= line.split()
			
			msg = getMsgFromLine(line)
			nick = getNickFromLine(line)
			
			if(line[0]=="PING"):
				self.sock.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
		
		return self.sock
		
	def disconnect(self, reason = ""):
		if reason != "":
			self.send(reason)
		else:
			self.send(self.message_quit)
			
		time.sleep(1)
		self.sock.send(bytes("QUIT \r\n", "UTF-8"))
		time.sleep(1)
		print("Disconnected from server")
		self.sock.close()
		self.sock = None
		
	def connectToChannel(self, chan = False):
		self.sock.send(bytes("PART %s\r\n" % self.channel, "UTF-8"))
		time.sleep(0.5)
		if (chan != False):
			self.channel = chan
		self.sock.send(bytes("JOIN %s\r\n" % self.channel, "UTF-8"))
		if (self.message_connexion != ""):
			time.sleep(0.5)
			self.sock.send(bytes("PRIVMSG %s %s\r\n" % (self.channel, self.message_connexion), "UTF-8"))
			self.sock.send(bytes("WHO %s\r\n" % self.channel, "UTF-8"))
	
	def disconnectChannel(self, chan = None):
		if (chan != None):
			self.sock.send(bytes("PART %s\r\n" % chan, "UTF-8"))
		else:
			self.sock.send(bytes("PART %s\r\n" % self.channel, "UTF-8"))
			
	def getChannelNames(self):
		self.sock.send(bytes("NAMES %s\r\n" % self.channel, "UTF-8"))
	
	def send(self, msg, chan = False):
		if (chan == False): 
			chan = self.channel
		self.sock.send(bytes("PRIVMSG %s %s\r\n" % (chan, msg), "UTF-8"))
		
	def step(self, timeout = None):
		if (self.sock != None):
		
			ready = select.select([self.sock], [], [], self.timeout if timeout == None else timeout)
			if ready[0]:
				self.readbuffer = self.readbuffer+self.sock.recv(1024).decode("utf-8")
			else:
				return None
			
			#self.readbuffer=self.readbuffer+self.sock.recv(1024).decode("utf-8")
			temp=self.readbuffer.split("\n")
			self.readbuffer=temp.pop( )
			for line in temp:
				line=line.rstrip()
				line=line.split()
				
				#print(line)
				
				msg = getMsgFromLine(line)
				nick = getNickFromLine(line)
				identity = getIdentityFromLine(line)
				chan = ""
				if len(line) > 2:
					if len(line[2]) > 2:
						if line[2][0] != ":":
							chan = line[2]
						else:
							chan = line[2][1:]
				
				#Ping message
				if(line[0]=="PING"):
					self.sock.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
					
				#Join message
				if (line[1] == "JOIN"):
					self.connected.append(nick)
					return MsgEvent("join", (nick, identity), "", chan)
				
				#Quit message
				elif(line[1] == "QUIT"):
					for i in range(len(self.connected)):
						if (self.connected[i] == nick):
							self.connected.pop(i)
							break
					return MsgEvent("quit", (nick, identity), msg, chan)
					
				#Part message
				elif(line[1] == "PART"):
					for i in range(len(self.connected)):
						if (self.connected[i] == nick):
							self.connected.pop(i)
							break
					return MsgEvent("part", (nick, identity), msg, chan)
					
				#Nick message
				elif(line[1] == "NICK"):
					s = line[2]
					if (s[0] == ":" or s[0] == "&" or s[0] == "@" or s[0] == "~"):
						s = s[1:]
					for i in range(len(self.connected)):
						if (self.connected[i] == nick):
							self.connected[i] = s
					return MsgEvent("nick", (nick, identity), s, chan)
						
				#List of users
				elif(line[1] == "353"):
					l = line[5:]
					connected = []
					for i in range(len(l)):
						s = l[i]
						if (s[0] == ":" or s[0] == "&" or s[0] == "@"):
							l[i] = s[1:]
						connected.append(l[i])
					self.connected = connected
				
				#Messages
				if (len(line) > 2):
					#Message Channel
					if (line[2].lower() == self.channel.lower()):
						return MsgEvent("channel", (nick, identity), msg, chan)
					#Message Private
					elif (line[2] == self.nick):
						if (nick != "NickServ"):
							if (nick == "IRC"):
								print("Connected to the server")
							else:
								if (nick != self.nick and nick != ""):
									return MsgEvent("private", (nick, identity), msg, nick)
			return None

class MsgEvent():
	def __init__(self, type, id, msg, chan = False):
		self.type = type
		self.id = id
		self.msg = msg
		self.message = msg
		self.nick = id[0]
		self.identity = id[1]
		self.ip = self.identity
		self.chan = chan
		self.channel = self.chan
			
	def get(self):
		return (self.type, self.id, self.msg)
		
class Bot(Nolirc):
	def __init__(self, nick, host, port, login, password, identity, realname, channel = None, autoconnect = True):
		Nolirc.__init__(self)
		
		self.identity = identity
		self.realname = realname
		
		self.nick = nick
		self.host = host
		self.port = port
		self.login = login
		self.password = password
		self.channel = channel
		
		self.setServer(host, port)
		self.setLogin(login, password)
		
		if self.channel != None and autoconnect == True:
			self.connectToServer()
			self.connectToChannel(self.channel)
										
def getMsgFromLine(line):
	msg = list(line)
	msg = msg[3:]
	msg = " ".join(msg)
	if (len(msg) > 0):
		if (msg[0] == ":"):
			msg = msg[1:]
	return msg
	
def getIdentityFromLine(line):
	identity = ""
	begin = False
	for letter in line[0]:
		if begin:
			identity += letter
			
		if letter == "!":
			begin = True
	return identity
	
def getNickFromLine(line):
	nick = ""
	i = 1
	while i:
		s = str(line[0])
		if (i < len(s)):
			if (s[i] != "!"):
				nick+= s[i]
				i+=1
			else: 
				return nick
		else: 
			return ""