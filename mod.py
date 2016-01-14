class ModWizz:
	def __init__(self, bot):
		self.bot = bot

	def step(self, event):
		if event.type == "channel" and event.msg == self.bot.nick + " getNames":
			self.bot.getChannelNames()
			print("Getting channel NAMES...")
		if event.type == "channel" and event.msg == self.bot.nick + " wizzAll":
			self.bot.send("\x01ACTION Wizz " + str(self.bot.connected) + "\x01")
			print("WizzAll")


class ModControl:
	def __init__(self, bot):
		self.bot = bot
		pass

	def step(self, event):
		if event.type == "private" and event.msg == "quit()":
			print("End Program")
			quit()
		if event.type == "channel" and event.msg == self.bot.nick + " quit()":
			self.bot.send("\x01ACTION headbutt everyone before dying\x01")
			print("End Program")
			quit()


class ModLog:
	def __init__(self, bot):
		self.bot = bot
		pass

	@staticmethod
	def step(event):
		if event.type == "channel":
			print("[{2}] {0}: {1}".format(event.nick, event.msg, event.chan))
		elif event.type == "private":
			print("[private] {0}: {1}".format(event.nick, event.msg))

		elif event.type == "nick":
			print("{0} changed nick to {1} in channel {2}".format(event.nick, event.msg, event.chan))
		elif event.type == "join":
			print("{0} join {1}".format(event.nick, event.chan))
		elif event.type == "quit":
			print("{0} quit {1}".format(event.nick, event.chan))
		elif event.type == "part":
			print("{0} part {1}".format(event.nick, event.chan))