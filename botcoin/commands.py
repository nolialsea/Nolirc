botNick = ["bc"]
_commandChar = [".", ":"]

command = {
	"getMoney": {
		"alias": ["getMoney", "getm"],
		"args": None,
		"description": "PM you your money amount"
	},
	"showMoney": {
		"alias": ["showMoney", "showm"],
		"args": None,
		"description": "Show your money amount in the channel"
	},
	"giveMoney": {
		"alias": ["giveMoney", "givem"],
		"args": "<receiver> <amount>",
		"description": "Give money to someone"
	},
	"mine": {
		"alias": ["mine"],
		"args": None,
		"description": "Mine some botcoins ( while random() < 0.5 { amount ++ } )"
	},
	"craftItem": {
		"alias": ["craftItem", "craft"],
		"args": "<title>#<description>",
		"description": "Craft an item with specific title and description, costs 1 botcoin"
	},
	"showItem": {
		"alias": ["showItem", "showi"],
		"args": "<itemId>",
		"description": "Show the specified item in the channel"
	},
	"getItem": {
		"alias": ["getItem", "geti"],
		"args": "<itemId>",
		"description": "Show you the specified item"
	},
	"setItemForSale": {
		"alias": ["setItemForSale", "setifs", "sifs"],
		"args": "<id> <false?>",
		"description": "Enable/disable the item forSale value. If it's enabled, other players can see it and buy it"
	},
	"buyItem": {
		"alias": ["buyItem", "buy"],
		"args": "<seller> <itemId>",
		"description": "Buy an item from someone"
	},
	"giveItem": {
		"alias": ["giveItem", "givei"],
		"args": "<receiver> <itemId>",
		"description": "Give an item to someone"
	},
	"help": {
		"alias": ["help"],
		"args": "<command?>",
		"description": "Show the help menu"
	}
}


def init( botNick_ ):
	botNick.append(botNick_)


def getMoney( msg, canal ):
	_alias = command["getMoney"]["alias"]
	return isCommand(msg, canal, _alias)


def showMoney( msg, canal ):
	_alias = command["showMoney"]["alias"]
	return isCommand(msg, canal, _alias)


def mine( msg, canal ):
	_alias = command["mine"]["alias"]
	return isCommand(msg, canal, _alias)


def giveMoney( msg, canal ):
	_alias = command["giveMoney"]["alias"]
	return isCommand(msg, canal, _alias)


def craftItem( msg, canal ):
	_alias = command["craftItem"]["alias"]
	return isCommand(msg, canal, _alias)


def help( msg, canal ):
	_alias = command["help"]["alias"]
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
