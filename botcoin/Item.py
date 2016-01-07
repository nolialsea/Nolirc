def curxecute( sql, args ):
	return sql, args


cursorExecute = curxecute


def init( cursorExecute_ ):
	global cursorExecute
	cursorExecute = cursorExecute_


def craftItem( title, description, creator ):
	cursorExecute(
			"INSERT INTO Item (title, description, creator, owner) VALUES (?, ?, ( SELECT id FROM User WHERE nick = ? ), ( SELECT id FROM User WHERE nick = ? ))",
			(title, description, creator, creator)
	)
	item = cursorExecute(
			"SELECT * FROM Item WHERE creator = (SELECT id FROM User WHERE nick = ?) ORDER BY id DESC LIMIT 1",
			(creator,)
	)
	if item:
		item = item[0]
		item = {
			"id": item[0],
			"title": item[1],
			"description": item[2],
			"creator": item[3],
			"dateCreation": item[4],
			"owner": item[5],
			"price": item[6],
			"priceMultiplier": item[7],
			"forSell": item[8]
		}
		return item
	return None

def getItem( id ):
	return cursorExecute(
			"SELECT * FROM Item WHERE id = ?",
			(id,)
	)

def getItemsByUserNick( userNick ):
	return cursorExecute(
			"SELECT * FROM Item WHERE owner = ( SELECT id FROM User WHERE nick = ?)",
			(userNick,)
	)
