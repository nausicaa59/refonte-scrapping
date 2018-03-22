import datetime

def save(db, data):
	try:
		abonnes = db.abonne
		profilAbonnes = abonnes.find_one({"pseudo": data["pseudo"]})
		if profilAbonnes != None:
			data['abonnes'] += [x for x in profilAbonnes['abonnes'] if  x not in data['abonnes']]
			abonnes.delete_one({'_id': profilAbonnes["_id"]})

		abonnes.insert_one(data)
		return (True, None)
	except Exception as e:
		return (False, str(e))
