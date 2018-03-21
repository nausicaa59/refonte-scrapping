import sys
import time
from tools import generateurUrl
from workers.workerHomeRandom import WorkerHomeRandom
from parseurs.factoryParseur import FactoryParseur
from env import env



class WorkerHomeNav(WorkerHomeRandom):
	def run(self):
		num = env.WORKER_HOMENAV_START
		url = generateurUrl.homePageById(num)

		try:
			while True:
				html = self.runGetQuery(url)
				(sujets, nbConnect) = self.parse(html)
				self.persiste(sujets, nbConnect)
				self.notify(url, num, sujets)
				(num, url) = generateurUrl.homePageNext(num , env.WORKER_HOMENAV_LEFT)
				if num <= 0:
					break
				time.sleep(env.WORKER_FREQ)
		except Exception as e:
			print(str(e))


	def notify(self, link, numPage, sujets):
		if env.WORKER_VERBOSE :
			print("-----------")
			print("Type : home-nav")
			print("Id Page : " + str(numPage))
			print("Url : " + link)
			print("Nb Sujets trouvé : " + str(len(sujets)))	