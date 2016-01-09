botNick = ["bc"]
_commandChar = [".", ":"]

commands = {
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
		"description": "Mine some botcoins"
	},
	"craftItem": {
		"alias": ["craftItem", "craft"],
		"args": "<title>#<description>",
		"description": "Craft an item with specific title and description, costs 1 botcoin"
	},
	"showItemsForSale": {
		"alias": ["showItemsForSale", "showifs"],
		"args": None,
		"description": "Show your items for sale in the channel"
	},
	"showItems": {
		"alias": ["showItems", "showis"],
		"args": None,
		"description": "Show your inventory in the channel"
	},
	"showItem": {
		"alias": ["showItem", "showi"],
		"args": "<itemID>",
		"description": "Show the specified item in the channel"
	},
	"getItems": {
		"alias": ["getItems", "getis"],
		"args": "<player>",
		"description": "Show you your inventory"
	},
	"getItem": {
		"alias": ["getItem", "geti"],
		"args": "<itemID>",
		"description": "Show you the specified item"
	},
	"buyItem": {
		"alias": ["buyItem", "buy"],
		"args": "<seller> <itemID>",
		"description": "Buy an item from someone"
	},
	"giveItem": {
		"alias": ["giveItem", "givei"],
		"args": "<receiver> <itemID>",
		"description": "Give an item to someone"
	},
	"setItemForSale": {
		"alias": ["setItemForSale", "setifs"],
		"args": "<itemID> <false?>",
		"description": "Enable/disable the item forSale value. If it's enabled, other players can see it and buy it"
	},
	"setPriceMultiplier": {
		"alias": ["setPriceMultiplier", "setpm"],
		"args": "<itemID> <value>",
		"description": "Set the price multiplier for one item, multiplier must be a real between 0 and 2"
	},
	"setForSale": {
		"alias": ["setForSale", "setfs"],
		"args": "<itemID> <false?>",
		"description": "Set if the item should be visible/buyable by other players"
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
	_alias = commands["getMoney"]["alias"]
	return isCommand(msg, canal, _alias)


def showMoney( msg, canal ):
	_alias = commands["showMoney"]["alias"]
	return isCommand(msg, canal, _alias)


def mine( msg, canal ):
	_alias = commands["mine"]["alias"]
	return isCommand(msg, canal, _alias)


def giveMoney( msg, canal ):
	_alias = commands["giveMoney"]["alias"]
	return isCommand(msg, canal, _alias)


def craftItem( msg, canal ):
	_alias = commands["craftItem"]["alias"]
	return isCommand(msg, canal, _alias)


def help( msg, canal ):
	_alias = commands["help"]["alias"]
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
