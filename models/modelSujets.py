from models import modelReponses


def save(db, data):
	collection = db.sujets

	for m in data:
		sujet = collection.find_one({"reference": m["reference"]})
		if sujet == None:
			m['scrapped'] 	= False
			m['changed'] 	= False
			m['deleted'] 	= False
			m['scrapped-finish'] = False
			collection.insert_one(m)
		else:
			m['scrapped'] 	= sujet['scrapped']
			m['changed'] 	= False if (m['nbReponse'] == sujet['nbReponse']) else True
			m['deleted'] 	= sujet['deleted']
			m['scrapped-finish'] = sujet['scrapped-finish']
			collection.delete_one({'_id': sujet["_id"]})
			collection.insert_one(m)

	return (True, None)


def setScrapped(db, refSujet, val):
	try:
		sujets = db.sujets
		sujet = sujets.find_one({"reference": refSujet})
		if sujet != None:
			sujets.update({'_id':sujet["_id"]}, {'$set':{'scrapped' : val}})
	except Exception as e:
		raise e


def setScrappedFinish(db, refSujet, val):
	try:
		sujets = db.sujets
		sujet = sujets.find_one({"reference": refSujet})
		if sujet != None:
			sujets.update({'_id':sujet["_id"]}, {'$set':{'scrapped-finish' : val}})
	except Exception as e:
		raise e


def setChanged(db, refSujet, val):
	try:
		sujets = db.sujets
		sujet = sujets.find_one({"reference": refSujet})
		if sujet != None:
			sujets.update({'_id':sujet["_id"]}, {'$set':{'changed' : val}})
	except Exception as e:
		raise e



def setDeleted(db, refSujet, val):
	try:
		sujets = db.sujets
		sujet = sujets.find_one({"reference": refSujet})
		if sujet != None:
			sujets.update({'_id':sujet["_id"]}, {'$set':{'deleted' : val}})
	except Exception as e:
		raise e


def getNotScrapped(db):
	try:
		sujets = db.sujets
		sujet = sujets.find_one({'$and': [{'scrapped': False},{'deleted': False},{'scrapped-finish': False}]})
		if sujet != None:
			sujet["nbReponses"] = modelReponses.countNbReponsesScrapped(db, sujet['reference'])
			return sujet

		sujet = sujets.find_one({'$and': [{'changed': True},{'deleted': False}]})
		if sujet != None:
			sujet["nbReponses"] = modelReponses.countNbReponsesScrapped(db, sujet['reference'])
			return sujet

		return None		
	except Exception as e:
		raise e	