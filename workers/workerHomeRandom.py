import sys
import time
from tools import generateurUrl
from worker import Worker
from parseurs.factoryParseur import FactoryParseur
from env import env

"""
Message Output
===============
sujets
	dateCreated
	type
	data
		[{
			url
			date
			nbReponse
			auteur
		}]

nbConnect
	dateCreated
	type
	data
		{date
		nbConnect}
"""



class WorkerHomeRandom(Worker):
	def __init__(self):
		super(WorkerHomeRandom, self).__init__(FactoryParseur.make('sujet'))
		self.min = env.WORKER_HOMERANDOM_MIN
		self.max = env.WORKER_HOMERANDOM_MAX

		
	def run(self):
		while True:
			try:
				link = generateurUrl.homePageRandom(self.min, self.max)
				html = self.runGetQuery(link)
				(sujets, nbConnect) = self.parse(html)
				self.notify(link, sujets, nbConnect)
				self.sendMsg("sujets", sujets)
				self.sendMsg("nbConnect", nbConnect)				
			except Exception as e:
				print("Erreur : " + str(e))	
			time.sleep(self.freq)


	def getOption(self):
		Worker.getOption(self)
		for arg in sys.argv:
			if arg.find("-max=") is not -1:
				self.max = int(arg.replace("-max=",""))
			if arg.find("-min=") is not -1:
				self.min = int(arg.replace("-min=",""))


	def notify(self, link, sujets, nbConnect):
		if self.verbose :
			print("Type : home-random")
			print("Url : " + link)
			print("Nb Sujets trouvé : " + str(len(sujets)))
			print("Nb connectés trouvé : " + str(nbConnect["nbConnect"]))
			print("-----------")