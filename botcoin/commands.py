

"commands : getMoney, showMoney, mine, giveMoney <receiver> <amount>, help"

botNick = None
_commandChar = [".", ": "]

aliases = {
	"getMoney": ["getMoney", "getm"],
	"showMoney": ["showMoney", "showm"],
	"mine": ["mine", "Mine"],
	"giveMoney": ["giveMoney", "givem"],
	"help": ["help"],
}

def init(botNick_):
	global botNick
	botNick = botNick_

def getMoney(msg, canal):
	_alias = aliases["getMoney"]
	return isCommand(msg, canal, _alias)
	
def showMoney(msg, canal):
	_alias = aliases["showMoney"]
	return isCommand(msg, canal, _alias)
	
def mine(msg, canal):
	_alias = aliases["mine"]
	return isCommand(msg, canal, _alias)
	
def giveMoney(msg, canal):
	_alias = aliases["giveMoney"]
	return isCommand(msg, canal, _alias)
	
def help(msg, canal):
	_alias = aliases["help"]
	return isCommand(msg, canal, _alias)
	
def isCommand(msg_, canal, alias_):
	msg = msg_.lower()
	for alias in alias_:
		alias = alias.lower()
		for commandChar in _commandChar:
			if (msg.find(botNick + commandChar + alias) == 0 and canal == False) or (msg.find(alias) == 0 and canal != False):
				return True
	return False