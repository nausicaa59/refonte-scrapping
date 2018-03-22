import sys
import time
from worker import Worker
from worker import Exception410
from worker import ExceptionParse
from worker import ExceptionPersiste
from worker import ExceptionAnyUrl
from pymongo.errors import ServerSelectionTimeoutError
from parseurs.factoryParseur import FactoryParseur
from verifications.verificationReponses import VerificationReponses
from models import modelReponses
from models import modelProfil
from models import modelSujets
from tools import generateurUrl
from env import env



class WorkerTopic(Worker):
	def __init__(self):
		super(WorkerTopic, self).__init__(FactoryParseur.make('topic'))

		
	def run(self):
		while True:
			try:
				self.initDBConnection()
				cible = self.getUrlNotScrap()
				self.extractReponseTopic(cible)
				modelSujets.setScrappedFinish(self.db, cible["reference"], True)
				modelSujets.setChanged(self.db, cible["reference"], False)
			except ServerSelectionTimeoutError as e:
				self.retryConnect()
			except ExceptionAnyUrl as e:
				print("plus aucune url a scrapper");
			finally:
				time.sleep(env.WORKER_FREQ)


	def extractReponseTopic(self, cible):
		nextUrl = cible["url"]
		while nextUrl != None :
			try:
				html = self.runGetQuery(nextUrl)
				(paggination, reponses) = self.parse(html)
				self.notify(cible["reference"], nextUrl, reponses)
				nextUrl = paggination[0] if len(paggination) > 0 else None
				self.persiste(reponses, cible["reference"])				
			except Exception410 as e:
				modelSujets.setDeleted(self.db, cible["reference"], True)
				print("Topic mort !", cible["reference"])
			finally:				
				time.sleep(env.WORKER_FREQ)


	def persiste(self, reponses, refTopic):
		for i in range(len(reponses)):
			reponses[i]["sujet"] = refTopic

		validator = VerificationReponses(reponses)
		validator.controle()
		validator.prepare()
		modelReponses.save(self.db, validator.data)

		for d in validator.data:
			modelProfil.saveNotScrapped(self.db, d["auteur"])

		if len(validator.data) > 0:
			modelSujets.setScrapped(self.db, validator.data[0]["sujet"], True)


	def notify(self, ref, url, data):
		if env.WORKER_VERBOSE :
			print("-----------")
			print("Type : sujet")
			print("Num sujet : " + str(ref))
			print("Url courante : " + str(url))
			print("Nb reponses trouvées : " + str(len(data)))		


	def getUrlNotScrap(self):
		cible = modelSujets.getNotScrapped(self.db)
		if cible == None:
			raise ExceptionAnyUrl()
		
		modelSujets.setScrapped(self.db, cible["reference"], True)			
		cible["url"] = generateurUrl.startTopicPage(cible["url"], cible["nbReponses"])
		return cible
