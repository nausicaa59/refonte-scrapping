import sys
import time
from tools import generateurUrl
from worker import Worker
from parseurs.factoryParseur import FactoryParseur
from env import env

"""
Message output
============
profil
	dateCreated
	type
	data
		dateInscription
		nbMessages
		imgLien
		nbRelation
		banni
"""

class WorkerProfil(Worker):
	def __init__(self):
		super(WorkerProfil, self).__init__(FactoryParseur.make('profil'))


	def run(self):
		while True:	
			pseudo = "meego"
			self.getProfil(pseudo)
			time.sleep(self.freq)


	def getProfil(self, pseudo):
		try:
			url = generateurUrl.userAbonne(pseudo)
			html = self.runGetQuery(url)
			profil = self.parse(html)
			profil['pseudo'] = pseudo
			self.sendMsg("profil", profil)
			self.sendMsgIsOk("profil")
			self.notify(pseudo, url, profil)
		except Exception as e:
			raise e


	def getOption(self):
		Worker.getOption(self)


	def notify(self, pseudo, url, profil):
		if self.verbose :
			print("-----------")
			print("Type : profil")
			print("Pseudo : " + pseudo)
			print("Resultat", profil)
