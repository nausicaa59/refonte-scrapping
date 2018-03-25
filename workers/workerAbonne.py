import sys
import time
from tools import generateurUrl
from worker import Worker
from worker import Exception410
from parseurs.factoryParseur import FactoryParseur
from pymongo.errors import ServerSelectionTimeoutError
from verifications.verificationAbonne import VerificationAbonne
from models import modelAbonne
from models import modelProfil
from env import env



class WorkerAbonne(Worker):
	def __init__(self):
		super(WorkerAbonne, self).__init__(FactoryParseur.make('abonne'))


	def run(self):
		while True:
			try:
				self.initDBConnection()
				auteur = modelProfil.getNotScrappedAbonne(self.db)
				pseudo = auteur["pseudo"]
				self.getAbonne(pseudo)
			except Exception as e:
				time.sleep(env.WORKER_FREQ)
				


	def getAbonne(self, pseudo):
		nextUrl = generateurUrl.userAbonne(pseudo)
		while nextUrl != None :	
			try:
				self.initDBConnection()
				html = self.runGetQuery(nextUrl)			
				(pagination, abonnes) = self.parse(html)
				data = {"pseudo" : pseudo, "abonnes" : abonnes}
				self.notify(pseudo, nextUrl, data)
				self.persiste(data)			
				nextUrl = pagination[0] if len(pagination) > 0 else None
			except ServerSelectionTimeoutError as e:
				self.retryConnect()
			except Exception as e:
				nextUrl = None
			finally:
				modelProfil.setScrappedAbonne(self.db, pseudo, True)	
				time.sleep(env.WORKER_FREQ)


	def persiste(self, reponses):
		validator = VerificationAbonne(reponses)
		validator.controle()	
		validator.prepare()
		modelAbonne.save(self.db, validator.data)



	def notify(self, pseudo, url, data):
		if env.WORKER_VERBOSE :
			print("-----------")
			print("Type : abonne")
			print("Pseudo : " + pseudo)
			print("Url : " + str(url))
			print("Nb abonnée trouvé", data)

