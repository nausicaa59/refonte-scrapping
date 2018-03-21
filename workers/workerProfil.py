import sys
import time
from tools import generateurUrl
from worker import Worker
from parseurs.factoryParseur import FactoryParseur
from env import env



class WorkerProfil(Worker):
	def __init__(self):
		super(WorkerProfil, self).__init__(FactoryParseur.make('profil'))


	def run(self):
		while True:	
			pseudo = "meego"
			self.getProfil(pseudo)
			time.sleep(env.WORKER_FREQ)


	def getProfil(self, pseudo):
		try:
			url = generateurUrl.userAbonne(pseudo)
			html = self.runGetQuery(url)
			profil = self.parse(html)
			profil['pseudo'] = pseudo
			self.notify(pseudo, url, profil)
		except Exception as e:
			raise e



	def notify(self, pseudo, url, profil):
		if env.WORKER_VERBOSE :
			print("-----------")
			print("Type : profil")
			print("Pseudo : " + pseudo)
			print("Resultat", profil)
