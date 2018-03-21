import sys
import time
from tools import generateurUrl
from worker import Worker
from parseurs.factoryParseur import FactoryParseur
from env import env

"""
Message output
==========
abonne
	dateCreated
	type
	data
		pseudo
		abonnes
"""


class WorkerAbonne(Worker):
	def __init__(self):
		super(WorkerAbonne, self).__init__(FactoryParseur.make('abonne'))


	def run(self):
		pseudo = "meego"
		self.getAbonne(pseudo)


	def getAbonne(self, pseudo):
		try:
			nextUrl = generateurUrl.userAbonne(pseudo)
			while nextUrl != None :
				html = self.runGetQuery(nextUrl)			
				(pagination, abonne) = self.parse(html)	
				data = {"pseudo" : pseudo, "abonnes" : abonne}			
				self.notify(pseudo, nextUrl, data)
				nextUrl = pagination[0] if len(pagination) > 0 else None
				time.sleep(env.WORKER_FREQ)
		except Exception as e:
			raise e



	def notify(self, pseudo, url, data):
		if env.WORKER_VERBOSE :
			print("-----------")
			print("Type : abonne")
			print("Pseudo : " + pseudo)
			print("Url : " + str(url))
			print("Nb abonnée trouvé", data)

