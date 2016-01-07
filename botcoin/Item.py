from time import time, sleep
import math

cursorExecute = None

def init(cursorExecute_):
	global cursorExecute
	cursorExecute = cursorExecute_
	#createItem("Test", "test", 1, 1000)
	#print(getItem(int(1)))

def createItem(title, description, creator, price = 0):
	return cursorExecute(
		"INSERT INTO Item (title, description, creator, owner) VALUES (?, ?, ?, ?)",
		(title, description, creator, creator)
	)
	
def getItem(id):
	return cursorExecute(
		"SELECT * FROM Item WHERE id = ?",
		(id,)
	)