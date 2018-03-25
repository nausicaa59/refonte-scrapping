import datetime

def save(db, data):
	auteurs = db.auteurs
	data['scrapped-profil'] = True
	pseudoIsOnlyInsert = auteurs.find_one({"pseudo": data["pseudo"]})
	if pseudoIsOnlyInsert != None:		
		data['scrapped-abonne'] = pseudoIsOnlyInsert['scrapped-abonne']
		auteurs.delete_one({'_id': pseudoIsOnlyInsert["_id"]})
	auteurs.insert_one(data)


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


def setScrappedProfil(db, pseudo, isScrapped):
	auteurs = db.auteurs
	auteur = auteurs.find_one({"pseudo": pseudo})
	if auteur != None:
		auteurs.update({'_id':auteur["_id"]}, {'$set':{'scrapped-profil' : isScrapped}})


def setScrappedAbonne(db, pseudo, isScrapped):
	auteurs = db.auteurs
	auteur = auteurs.find_one({"pseudo": pseudo})
	if auteur != None:
		auteurs.update({'_id':auteur["_id"]}, {'$set':{'scrapped-abonne' : isScrapped}})


def getNotScrapped(db):
	auteurs = db.auteurs
	auteur = auteurs.find_one({'scrapped-profil': False})
	if auteur == None:
		raise AssertionError("Aucun pseudo trouvé")
	return auteur


def getNotScrappedAbonne(db):
	auteurs = db.auteurs
	auteur = auteurs.find_one({'scrapped-abonne': False})
	if auteur == None:
		raise AssertionError("Aucun pseudo trouvé")
	return auteur