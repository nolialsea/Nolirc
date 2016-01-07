botNick = ["bc"]
_commandChar = [".", ":"]

aliases = {
	"getMoney": ["getMoney", "getm"],
	"showMoney": ["showMoney", "showm"],
	"mine": ["mine"],
	"giveMoney": ["giveMoney", "givem"],
	"craftItem": ["craftItem", "craft"],
	"help": ["help"],
}


def init( botNick_ ):
	botNick.append(botNick_)


def getMoney( msg, canal ):
	_alias = aliases["getMoney"]
	return isCommand(msg, canal, _alias)


def showMoney( msg, canal ):
	_alias = aliases["showMoney"]
	return isCommand(msg, canal, _alias)


def mine( msg, canal ):
	_alias = aliases["mine"]
	return isCommand(msg, canal, _alias)


def giveMoney( msg, canal ):
	_alias = aliases["giveMoney"]
	return isCommand(msg, canal, _alias)


def craftItem( msg, canal ):
	_alias = aliases["craftItem"]
	return isCommand(msg, canal, _alias)


def help( msg, canal ):
	_alias = aliases["help"]
	return isCommand(msg, canal, _alias)


def isCommand( msg_, canal, alias_ ):
	msg = msg_.lower()
	for alias in alias_:
		alias = alias.lower()
		for commandChar in _commandChar:
			for nick in botNick:
				if (msg.find(nick + commandChar + alias) == 0 and not canal) or (msg.find(alias) == 0 and canal):
					return True
	return False
