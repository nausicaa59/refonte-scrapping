def save(db, data):
	try:
		freq = db.frequentations
		freq.insert_one(data)
		return (True, None)
	except Exception as e:
		return (False, str(e))