import math
from time import time


def curxecute( sql, args ):
	return sql, args


cursorExecute = curxecute


def init( cursorExecute_ ):
	global cursorExecute
	cursorExecute = cursorExecute_


# createUser("Noli")
# print(getUserByNick("Noli"))

def createUser( nick, lastMining = math.floor(time()) ):
	return cursorExecute(
			"INSERT INTO User (nick, lastMining) VALUES (?, ?)",
			(nick, lastMining)
	)


def getUserByNick( nick ):
	result = cursorExecute(
			"SELECT * FROM User WHERE nick = ?",
			(nick,)
	)
	if result and result != []:
		result = result[0]
		user = {
			"id": result[0],
			"nick": result[1],
			"money": result[2],
			"lastMining": result[3],
			"lastCraft": result[4]
		}
		return user
	return None


def getMoney( nick ):
	result = None
	user = getUserByNick(nick)
	if user:
		return user["money"]
	return None


def giveMoney( nickSender, nickReveiver, amount ):
	result = None
	sender = getUserByNick(nickSender)
	receiver = getUserByNick(nickReveiver)
	if sender and receiver:
		if sender["money"] < amount:
			amount = sender["money"]
		cursorExecute(
				"INSERT INTO MoneyTransaction (sender, receiver, amount) VALUES (?, ?, ?)",
				(nickSender, nickReveiver, amount)
		)
		addMoney(nickSender, -amount)
		addMoney(nickReveiver, amount)
		result = amount
	return result


def addMoney( nick, amount ):
	result = None
	user = getUserByNick(nick)
	if user:
		result = cursorExecute(
				"UPDATE User SET money = ? WHERE nick = ?",
				(user["money"] + amount, nick)
		)
	return result


def updateLastMining( nick ):
	result = cursorExecute(
			"UPDATE User SET lastMining = ? WHERE nick = ?",
			(time(), nick)
	)
	return result
