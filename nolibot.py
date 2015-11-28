import nolirc, conf
import mod

#nolirc.Bot(nick, host, port, login, password, identity, realname, channel = None, autoconnect = True)
bot = nolirc.Bot(conf.nick, conf.host, conf.port, conf.login, conf.password, conf.identity, conf.realname, channel = conf.channel)
bot.timeout = 1

#List of mods you want to use
#async are called every step
module_async = [
	#mod.ModVote(bot)
]

#sync are called every step ONLY if a message is received
module_sync = [
	mod.ModWizz(bot),
	mod.ModLog(bot),
	mod.ModControl(bot)
]

#Main loop
while True:
	msgEvent = bot.step()
	#Bot.step() returns a MsgEvent object if a message is received, else None
	#Bot.step() wait for a message for Bot.timeout seconds (default 1), then return None if no message is received
	#You can use Bot.step(timeout) as well, timeout must be a positive int or float value
	"""
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
	"""

	if msgEvent != None:
		for m in module_sync:
			m.step(msgEvent)
			
	for m in module_async:
		m.step(msgEvent)