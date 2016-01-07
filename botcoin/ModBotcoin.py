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
		self.pingInterval = 10
		self.lastPing = time() - self.pingInterval + 1
		self.bot.send('Botcoin started ! Type "' + self.bot.nick + '.help()" to view the commands')

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
			delta = time() - user[3]
			if delta>60 * 60 * 24:
				delta = 60 * 60 * 24
			delta = math.floor(delta)
			amount = 1 / 86400 * delta
			while True:
				if random()<0.5:
					amount += 1 / 86400 * delta
				else:
					break
			if amount>0:
				User.addMoney(event.nick, amount)

			message = event.nick + " has mined " + str(amount) + " botcoin in " + secondsToTime(delta)
			if amount>=2: message += "s"
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

	def step( self, event ):
		if event:
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
			elif commands.help(event.msg, canal):
				self.bot.send("commands : getMoney, showMoney, mine, giveMoney <receiver> <amount>, help", canal)

		else:
			# Auto mining
			if time() - self.lastPing>self.pingInterval:
				self.lastPing = time()
				for connected in self.bot.connected:
					if connected != self.bot.nick:
						User.createUser(connected)
						User.addMoney(connected, 1 / 86400 * self.pingInterval)

				self.bot.getChannelNames()
