import sqlite3


def init(database, cursor, guild=None, add_conf=None, val=None):
	
	cursor.execute('CREATE TABLE IF NOT EXISTS songs_cache(id TEXT, title TEXT)')
	database.commit()

	if add_conf:
		cursor.execute(f'INSERT INTO TABLE {guild} values(?,?)', (add_conf,val))
		database.commit()
	elif guild:
		for g in guild:
			cursor.execute(f'CREATE TABLE IF NOT EXISTS {g}(col1 TEXT, col2 TEXT)')
			database.commit()