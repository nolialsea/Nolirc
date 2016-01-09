from time import time
from botcoin import database, User, Item, commands
from random import random
import math

cursorExecute = database.cursorExecute

database.init()
User.init(cursorExecute)
Item.init(cursorExecute)


def secondsToTime( seconds ):
	result = ""
	atLeastOneMinute = False
	arLeastOneHour = False
	if math.floor(seconds / 3600)>0:
		arLeastOneHour = True
		result += str(math.floor(seconds / 3600)) + " hour"
		if math.floor(seconds / 3600)>=2: result += "s"
		seconds = math.floor(seconds % 3600)
	if math.floor(seconds / 60)>0:
		atLeastOneMinute = True
		if arLeastOneHour:
			result += ", "
		result += str(math.floor(seconds / 60)) + " minute"
		if math.floor(seconds / 60)>=2: result += "s"
		seconds = math.floor(seconds % 60)
	if atLeastOneMinute:
		result += " and "
	result += str(seconds) + " second"
	if seconds>=2: result += "s"
	return result


class ModBotcoin:
	def __init__( self, bot ):
		self.bot = bot
		commands.init(self.bot.nick)
		self.pingInterval = 20
		self.botcoinPerSecond = 1 / 86400
		self.lastPing = time() - self.pingInterval + 1
		self.bot.send('Botcoin started ! Type "' + self.bot.nick + '.help" to view the commands')

	def getMoney( self, event, canal ):
		money = User.getMoney(event.nick)
		if not money:
			return
		message = "You have " + str(money) + " botcoin"
		if money>=2:
			message += "s"
		self.bot.send(message, event.nick)

	def showMoney( self, event, canal ):
		money = User.getMoney(event.nick)
		message = event.nick + " have " + str(money) + " botcoin"
		if money>=2:
			message += "s"
		self.bot.send(message)

	def mine( self, event, canal ):
		user = User.getUserByNick(event.nick)
		print(user)
		if user:
			delta = time() - user["lastMining"]
			if delta > 60 * 60 * 24:
				delta = 60 * 60 * 24
			delta = math.floor(delta)
			if delta == 0:
				return
			amount = (self.botcoinPerSecond * delta) + (self.botcoinPerSecond * delta * random())
			nbTrigger = 1
			while True:
				if random() < 0.5:
					nbTrigger += 1
					amount += self.botcoinPerSecond * delta * random()
				else:
					break
			if amount > 0:
				User.addMoney(event.nick, amount)

			message = event.nick + " has mined " + str(amount) + " botcoin in " + secondsToTime(delta)
			message += " in "+ str(nbTrigger) +" hit"
			message += "s" if nbTrigger > 1 else ""
			if amount >= 2:
				message += "s"
			message += " at multiplier x" + str(amount * 86400 / delta)
			User.updateLastMining(event.nick)
			self.bot.send(message, canal)

	def giveMoney( self, event, canal ):
		msg = event.msg.split(" ")
		if len(msg) == 3:
			amount = msg[2]
			try:
				amount = float(msg[2])
			except Exception as e:
				self.bot.send(
						'Transaction failed, use like this : "' + self.bot.nick + '.giveMoney <receiver> <amount>"',
						canal)
				return

			result = User.giveMoney(event.nick, msg[1], amount)
			if result:
				message = event.nick + ' gives ' + str(result) + ' botcoin'
				if result>=2: message += "s"
				message += " to " + msg[1]
				self.bot.send(message, canal)
				if canal:
					self.bot.send(message, msg[1])
			else:
				self.bot.send(
						'Transaction failed, use like this : "' + self.bot.nick + '.giveMoney <receiver> <amount>"',
						canal)
		else:
			self.bot.send(
					'Invalid command, use like this : "' + self.bot.nick + '.giveMoney <receiver> <amount>"',
					canal)

	def craftItem( self, event, canal ):
		msg = event.msg.split(" ",1)[1]
		if len(msg.split("#", 1)) == 2:
			user = User.getUserByNick(event.nick)
			if user:
				if user["money"] >= 1:
					User.addMoney(event.nick, -1)
					msg = event.msg.split(" ", 1)[1]
					itemTitle = msg.split("#")[0]
					itemDescription = msg.split("#")[1]
					item = Item.craftItem(itemTitle, itemDescription, event.nick)
					if item:
						message = "You" if canal else event.nick
						message += " have crafted [" + item["title"] + "] for 1 botcoin"
						self.bot.send(message, canal)
				else:
					message = "You" if canal else event.nick
					message += " dont' have enough money"
					message += ", you need at least 1 botcoin" if canal else ""
					message += " to do that"
					self.bot.send(message, canal)
			else:
				self.bot.send("Something went wrong... Sorry", canal)
		else:
			self.bot.send("Use like this : \"botcoin.craftItem <title>#<description>\"", canal)

	def help(self, event, canal):
		message = ""
		userMsg = event.msg.split(" ", 1)
		userMsg = userMsg[1] if len(userMsg) > 1 else userMsg[0]
		for key, command in commands.commands.items():
			description = command["description"]
			alias = command["alias"]
			for a in alias:
				if userMsg == a:
					message += a + " "
					message += str(command["args"]) if command["args"] else ""
					message += " : " + description
					self.bot.send(message, canal)
					message = "Alias : " + ", ".join(alias)
					self.bot.send(message, canal)
					return
		command = list(commands.commands.keys())
		lstCommands = []
		for c in command:
			lstCommands.append(c)
		self.bot.send("commands : " + ", ".join(lstCommands), canal)

	def step( self, event ):
		if event:
			if event.type == "join":
				User.createUser(event.nick)
				return
			canal = event.nick
			if event.type == "channel":
				canal = False
			if commands.getMoney(event.msg, canal):
				self.getMoney(event, canal)
			elif commands.showMoney(event.msg, canal):
				self.showMoney(event, canal)
			elif commands.mine(event.msg, canal):
				self.mine(event, canal)
			elif commands.giveMoney(event.msg, canal):
				self.giveMoney(event, canal)
			elif commands.craftItem(event.msg, canal):
				self.craftItem(event, canal)
			elif commands.help(event.msg, canal):
				self.help(event, canal)

		else:
			# Auto mining
			if time() - self.lastPing>self.pingInterval:
				self.lastPing = time()
				for connected in self.bot.connected:
					if connected != self.bot.nick:
						User.createUser(connected)
						User.addMoney(connected, 1 / 86400 * self.pingInterval)

				self.bot.getChannelNames()
