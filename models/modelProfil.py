import datetime

def save(db, data):
	try:
		auteurs = db.auteurs
		pseudoIsOnlyInsert = auteurs.find_one({"pseudo": data["pseudo"]})
		if pseudoIsOnlyInsert != None:
			data['scrapped-abonne'] = pseudoIsOnlyInsert['scrapped-abonne']
			auteurs.delete_one({'_id': pseudoIsOnlyInsert["_id"]})
		else:
			data['scrapped-profil'] = True

		auteurs.insert_one(data)
		return (True, None)
	except Exception as e:
		return (False, str(e))


def saveNotScrapped(db, pseudo):
	try:
		auteurs = db.auteurs
		pseudoIsOnlyInsert = auteurs.find_one({"pseudo": pseudo.lower()})
		if pseudoIsOnlyInsert == None:
			auteurs.insert_one({
				'pseudo'			: pseudo.lower(),
				'dateInscription'	: datetime.datetime(1980, 1, 1, 0, 0),
				'nbMessages'		: 0,
				'imgLien'			: 0,
				'nbRelation'		: 0,
				'banni'				: 0,
				'scrapped-profil'	: False,
				'scrapped-abonne'	: False,
			})
	except Exception as e:
		raise e


def setScrapped(db, pseudo, isScrapped):
	try:
		auteurs = db.auteurs
		auteur = auteurs.find_one({"pseudo": pseudo})
		if auteur != None:
			auteurs.update({'_id':auteur["_id"]}, {'$set':{'scrapped' : isScrapped}})
	except Exception as e:
		raise e



