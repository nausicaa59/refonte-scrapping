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
"""

class WorkerHomeNav(Worker):
	def __init__(self):
		super(WorkerHomeNav, self).__init__(FactoryParseur.make('sujet'))
		self.start 	= env.WORKER_HOMENAV_START
		self.left 	= env.WORKER_HOMENAV_LEFT


	def run(self):
		num = self.start
		url = generateurUrl.homePageById(num)

		try:
			while True:
				html = self.runGetQuery(url)
				(sujets, nbConnect) = self.parse(html)
				self.notify(url, num, sujets)
				self.sendMsg("sujets", sujets)
				(num, url) = generateurUrl.homePageNext(num , self.left)
				if num <= 0:
					break
				time.sleep(self.freq)
		except Exception as e:
			print(str(e))


	def getOption(self):
		Worker.getOption(self)
		for arg in sys.argv:
			if arg.find("-start=") is not -1:
				self.start = int(arg.replace("-start=",""))
			if arg.find("-left=") is not -1:
				sens = arg.replace("-left=","")
				self.left = False if sens.lower() == "false" else True


	def notify(self, link, numPage, sujets):
		if self.verbose :
			print("-----------")
			print("Type : home-nav")
			print("Id Page : " + str(numPage))
			print("Url : " + link)
			print("Nb Sujets trouvé : " + str(len(sujets)))	