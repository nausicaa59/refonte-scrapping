import sys
import time
from tools import generateurUrl
from worker import Worker
from worker import Exception410
from parseurs.factoryParseur import FactoryParseur
from pymongo.errors import ServerSelectionTimeoutError
from verifications.verificationProfil import VerificationProfil
from models import modelProfil
from env import env



class WorkerProfil(Worker):
	def __init__(self):
		super(WorkerProfil, self).__init__(FactoryParseur.make('profil'))


	def run(self):
		while True:
			try:
				self.initDBConnection()	
				auteur = modelProfil.getNotScrapped(self.db)
				pseudo = auteur["pseudo"]
				url = generateurUrl.userProfil(pseudo)
				html = self.runGetQuery(url)
				profil = self.parse(html)
				profil['pseudo'] = pseudo
				self.persiste(profil)
				self.notify(pseudo, url, profil)
			except Exception410 as e:
				auteur["banni"] = 1
				modelProfil.save(self.db, auteur)
			except ServerSelectionTimeoutError as e:
				self.retryConnect()
			except Exception as e:
				print(str(e))
			finally:
				print(env.WORKER_FREQ)
				time.sleep(env.WORKER_FREQ)




	def persiste(self, profil):
		validator = VerificationProfil(profil)
		validator.controle()
		validator.prepare()
		modelProfil.save(self.db, validator.data)


	def notify(self, pseudo, url, profil):
		if env.WORKER_VERBOSE :
			print("-----------")
			print("Type : profil")
			print("Pseudo : " + pseudo)
			print("Resultat", profil)
