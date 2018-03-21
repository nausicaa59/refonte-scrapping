import sys
import time
from tools import generateurUrl
from worker import Worker
from parseurs.factoryParseur import FactoryParseur
from verifications.verificationSujets import VerificationSujets
from verifications.verificationConnect import VerificationConnect
from models import modelSujets
from models import modelConnect
from models import modelProfil
from env import env



class WorkerHomeRandom(Worker):
	def __init__(self):
		super(WorkerHomeRandom, self).__init__(FactoryParseur.make('sujet'))

		
	def run(self):
		while True:
			try:
				link = generateurUrl.homePageRandom(env.WORKER_HOMERANDOM_MIN, env.WORKER_HOMERANDOM_MAX)
				html = self.runGetQuery(link)
				(sujets, nbConnect) = self.parse(html)
				self.persiste(sujets, nbConnect)
				self.notify(link, sujets, nbConnect)
			except Exception as e:
				print("Erreur : " + str(e))	
			time.sleep(env.WORKER_FREQ)


	def persiste(self, sujets, nbConnect):
		#init
		db = self.initDBConnection()

		#Persiste sujets...
		validator = VerificationSujets(sujets)
		(valide, err) = validator.controle()
		if valide == False:
			raise AssertionError("La vérification des sujet a échouer" + str(err) + "[data : " + str(nbConnect) + "]")	

		(valide, err) = validator.prepare()
		if valide == False:
			raise AssertionError("La preparation des sujet a échouer" + str(err) + "[data : " + str(nbConnect) + "]")

		modelSujets.save(db, validator.data)


		#Persiste Pseudo found
		for d in validator.data:
			modelProfil.saveNotScrapped(db, d["auteur"])


		#Persite NbConnect
		validator = VerificationConnect(nbConnect)
		(valide, err) = validator.controle()
		if valide == False:
			raise AssertionError("L'item nb connection est invalide" + str(err) + "[data : " + str(nbConnect) + "]")	

		(valide, err) = validator.prepare()
		if valide == False:
			raise AssertionError("La preparation du nb connection a échouer" + str(err) + "[data : " + str(nbConnect) + "]")

		modelConnect.save(db, validator.data)


		#clear
		self.closeDBConnection()



	def notify(self, link, sujets, nbConnect):
		if env.WORKER_VERBOSE :
			print("Type : home-random")
			print("Url : " + link)
			print("Nb Sujets trouvé : " + str(len(sujets)))
			print("Nb connectés trouvé : " + str(nbConnect["nbConnect"]))
			print("-----------")