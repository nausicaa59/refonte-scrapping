import sys
import time
from worker import Worker
from parseurs.factoryParseur import FactoryParseur
from env import env


"""
Message Output
=============
reponses
	dateCreated
	type
	data
		[
		auteur
		date
		reference
		sujet
		contenu
			content
			citation
			images
				smileys
				other					
		]
"""


class WorkerTopic(Worker):
	def __init__(self):
		super(WorkerTopic, self).__init__(FactoryParseur.make('topic'))

	def callback(self, ch, method, properties, body):
		print(body)

		
	def run(self):
		while True:			
			cible = {
				"start" : "http://www.jeuxvideo.com/forums/42-51-50884417-1-0-1-0-un-mmo-plus-surcote-que-la-vie.htm",
				"ref" : "50884417"
			}
			
			self.extractReponseTopic(cible)
			time.sleep(self.freq)


	def extractReponseTopic(self, cible):
		nextUrl = cible["start"]

		try:
			while nextUrl != None :
				html = self.runGetQuery(nextUrl)
				(paggination, data) = self.parse(html)
				for i in range(len(data)):
					data[i]["sujet"] = cible["ref"]

				self.sendMsg("reponses", data)
				self.sendMsgIsOk("reponses")
				self.notify(cible["ref"], nextUrl, data)
				nextUrl = paggination[0] if len(paggination) > 0 else None
				time.sleep(self.freq)
		except Exception as e:
			print(str(e))
	

	def getOption(self):
		Worker.getOption(self)


	def notify(self, ref, url, data):
		if self.verbose :
			print("-----------")
			print("Type : sujet")
			print("Num sujet : " + str(ref))
			print("Url courante : " + url)
			print("Nb Sujets trouvé : " + str(len(data)))		

