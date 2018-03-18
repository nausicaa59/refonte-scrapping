from workers.workerHomeRandom import WorkerHomeRandom
from workers.workerHomeNav import WorkerHomeNav
from workers.workerTopic import WorkerTopic
from workers.workerProfil import WorkerProfil
from workers.workerAbonne import WorkerAbonne

class FactoryWorker:
	@staticmethod
	def make(type):
		if type == "home-nav":
			return WorkerHomeNav()
		if type == "home-random":
			return WorkerHomeRandom()
		if type == "topic":
			return WorkerTopic()
		if type == "profil":
			return WorkerProfil()
		if type == "abonne":
			return WorkerAbonne()
		raise AssertionError("Aucun worker trouver: " + str(type))
