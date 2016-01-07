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

def createUser( nick, money = 0, lastMining = math.floor(time()) ):
	return cursorExecute(
			"INSERT INTO User (nick, money, lastMining) VALUES (?, ?, ?)",
			(nick, money, lastMining)
	)


def getUserByNick( nick ):
	result = cursorExecute(
			"SELECT * FROM User WHERE nick = ?",
			(nick,)
	)
	if result and result != []:
		return result[0]
	return None


def getMoney( nick ):
	result = None
	user = getUserByNick(nick)
	if user:
		return user[2]
	return None


def giveMoney( nickSender, nickReveiver, amount ):
	result = None
	userSender = getUserByNick(nickSender)
	userReceiver = getUserByNick(nickReveiver)
	if userSender and userReceiver:
		if userSender[2]<amount:
			amount = userSender[2]
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
				(user[2] + amount, nick)
		)
	return result


def updateLastMining( nick ):
	result = cursorExecute(
			"UPDATE User SET lastMining = ? WHERE nick = ?",
			(time(), nick)
	)
	return result
