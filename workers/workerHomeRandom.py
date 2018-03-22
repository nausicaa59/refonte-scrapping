import sys
import time
from tools import generateurUrl
from worker import Worker
from parseurs.factoryParseur import FactoryParseur
from pymongo.errors import ServerSelectionTimeoutError
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
				self.initDBConnection()
				link = generateurUrl.homePageRandom(env.WORKER_HOMERANDOM_MIN, env.WORKER_HOMERANDOM_MAX)
				html = self.runGetQuery(link)
				(sujets, nbConnect) = self.parse(html)
				self.persiste(sujets, nbConnect)
				self.notify(link, sujets, nbConnect)
			except ServerSelectionTimeoutError as e:
				self.retryConnect()
			except Exception as e:
				print("Erreur : " + str(e))
			finally:
				time.sleep(env.WORKER_FREQ)


	def persiste(self, sujets, nbConnect):
		#Persiste sujets...
		validator = VerificationSujets(sujets)
		validator.controle()
		validator.prepare()
		modelSujets.save(self.db, validator.data)

		#Persiste Pseudo found
		for d in validator.data:
			modelProfil.saveNotScrapped(self.db, d["auteur"])

		#Persite NbConnect
		validator = VerificationConnect(nbConnect)
		validator.controle()
		validator.prepare()
		modelConnect.save(self.db, validator.data)



	def notify(self, link, sujets, nbConnect):
		if env.WORKER_VERBOSE :
			print("Type : home-random")
			print("Url : " + link)
			print("Nb Sujets trouvé : " + str(len(sujets)))
			print("Nb connectés trouvé : " + str(nbConnect["nbConnect"]))
			print("-----------")