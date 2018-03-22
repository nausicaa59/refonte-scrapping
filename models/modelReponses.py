def checkIfExist(db, reference):
	collection = db.reponses
	sujet = collection.find_one({"reference": reference})
	if sujet == None:
		return False
	return True


def save(db, data):
	try:
		data = [x for x in data if checkIfExist(db, x['reference']) == False]
		reponses = db.reponses
		for m in data:
			reponses.insert_one(m)			
		return (True, None)
	except Exception as e:
		return (False, str(e))


def countNbReponsesScrapped(db, refSujet):
	try:
		collection = db.reponses
		return collection.find({"sujet":refSujet}).count()
	except Exception as e:
		raise e