def curxecute( sql, args ):
	return sql, args


cursorExecute = curxecute


def init( cursorExecute_ ):
	global cursorExecute
	cursorExecute = cursorExecute_


def craftItem( title, description, creator, price = 1 ):
	return cursorExecute(
			"INSERT INTO Item (title, description, creator, owner, price) VALUES (?, ?, ?, ?, ?)",
			(title, description, creator, creator, price)
	)


def getItem( id ):
	return cursorExecute(
			"SELECT * FROM Item WHERE id = ?",
			(id,)
	)

def getItems( userId ):
	return cursorExecute(
			"SELECT * FROM Item WHERE owner = ?",
			(userId,)
	)
