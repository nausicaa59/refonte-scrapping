import sys
import time
from worker import Worker
from parseurs.factoryParseur import FactoryParseur
from verifications.verificationReponses import VerificationReponses
from models import modelReponses
from models import modelProfil
from models import modelSujets
from env import env


class WorkerTopic(Worker):
	def __init__(self):
		super(WorkerTopic, self).__init__(FactoryParseur.make('topic'))

		
	def run(self):
		while True:			
			cible = {
				"start" : "http://www.jeuxvideo.com/forums/42-51-50884417-1-0-1-0-un-mmo-plus-surcote-que-la-vie.htm",
				"ref" : "50884417"
			}
			
			self.extractReponseTopic(cible)
			time.sleep(env.WORKER_FREQ)


	def extractReponseTopic(self, cible):
		nextUrl = cible["start"]

		try:
			while nextUrl != None :
				html = self.runGetQuery(nextUrl)
				(paggination, data) = self.parse(html)
				for i in range(len(data)):
					data[i]["sujet"] = cible["ref"]

				self.persiste(data)
				self.notify(cible["ref"], nextUrl, data)
				nextUrl = paggination[0] if len(paggination) > 0 else None
				time.sleep(env.WORKER_FREQ)
		except Exception as e:
			print(str(e))


	def persiste(self, reponses):
		#init
		db = self.initDBConnection()

		#Persiste sujets...
		validator = VerificationReponses(reponses)
		(valide, err) = validator.controle()
		if valide == False:
			raise AssertionError("La vérification des réponses a échouer" + str(err))	

		(valide, err) = validator.prepare()
		if valide == False:
			raise AssertionError("La preparation des réponses a échouer" + str(err))

		(valide, err) = modelReponses.save(db, validator.data)
		if valide == False:
			raise AssertionError("La sauvegarde des réponses a échouer" + str(err))

		for d in validator.data:
			modelProfil.saveNotScrapped(db, d["auteur"])

		if len(validator.data) > 0:
			modelSujets.setScrapped(db, validator.data[0]["sujet"], True)

		#clear
		self.closeDBConnection()


	def notify(self, ref, url, data):
		if env.WORKER_VERBOSE :
			print("-----------")
			print("Type : sujet")
			print("Num sujet : " + str(ref))
			print("Url courante : " + url)
			print("Nb Sujets trouvé : " + str(len(data)))		

