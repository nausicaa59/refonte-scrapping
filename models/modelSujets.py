def save(db, data):
	collection = db.sujets

	for m in data:
		sujet = collection.find_one({"reference": m["reference"]})
		if sujet == None:
			m['scrapped'] 	= False
			m['changed'] 	= False
			collection.insert_one(m)
		else:
			m['scrapped'] 	= sujet['scrapped']
			m['changed'] 	= False if (m['nbReponse'] == sujet['nbReponse']) else True
			collection.delete_one({'_id': sujet["_id"]})
			collection.insert_one(m)

	return (True, None)


def setScrapped(db, idSujet, isScrapped):
	try:
		sujets = db.sujets
		sujet = sujets.find_one({"reference": idSujet})
		if sujet != None:
			sujets.update({'_id':sujet["_id"]}, {'$set':{'scrapped' : isScrapped}})
	except Exception as e:
		raise e


def setOrderSend(db, idSujet, isSend):
	try:
		sujets = db.sujets
		sujet = sujets.find_one({"reference": idSujet})
		if sujet != None:
			sujets.update({'_id':sujet["_id"]}, {'$set':{'ordersend' : isSend}})
	except Exception as e:
		raise e