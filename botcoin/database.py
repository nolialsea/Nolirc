import math
import sqlite3
from time import time

debug = True
db = sqlite3.connect('botcoin/database.db')


def init( ):
	# deleteDatabase()
	createDatabase()


def cursorExecute( sql, args = () ):
	if debug:
		print(sql)
	try:
		cursor = db.cursor()
		cursor.execute(sql, args)
		result = cursor.fetchall()
		db.commit()
		if debug: print(result)
		return result
	except Exception as e:
		if debug: print("Erreur : ", e)
		db.rollback()
		# raise e
		return None


def deleteDatabase( ):
	cursorExecute("DROP TABLE IF EXISTS User")
	cursorExecute("DROP TABLE IF EXISTS Item")
	cursorExecute("DROP TABLE IF EXISTS Sell")
	cursorExecute("DROP TABLE IF EXISTS MoneyTransaction")


def createDatabase( ):
	cursorExecute("""
		CREATE TABLE IF NOT EXISTS User(
			id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			nick TEXT UNIQUE,
			money REAL DEFAULT 0,
			lastMining INTEGER DEFAULT """ + str(math.floor(time())) + """
		)
	""")
	cursorExecute("""
		CREATE TABLE IF NOT EXISTS Item(
			id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			title TEXT,
			description TEXT,
			creator INTEGER,
			dateCreation INTEGER DEFAULT """ + str(math.floor(time())) + """,
			owner INTEGER,
			price REAL DEFAULT 0,
			forSell INTEGER DEFAULT 0
		)
	""")
	cursorExecute("""
		CREATE TABLE IF NOT EXISTS Sell(
			id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			seller INTEGER,
			buyer INTEGER,
			item INTEGER,
			price REAL,
			date INTEGER DEFAULT """ + str(math.floor(time())) + """
		)
	""")
	cursorExecute("""
		CREATE TABLE IF NOT EXISTS MoneyTransaction(
			id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			sender INTEGER,
			receiver INTEGER,
			amount REAL,
			date INTEGER DEFAULT """ + str(math.floor(time())) + """
		)
	""")
