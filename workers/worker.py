import sys
import requests
import time
import random
import pika
import json
import datetime
from tools import generateurUrl
from pymongo import MongoClient
from env import env


class ExceptionAnyUrl(Exception):
    pass


class Exception410(Exception):
    pass


class ExceptionParse(Exception):
    pass


class ExceptionPersiste(Exception):
    pass



class Worker():
	def __init__(self, parser):
		self.parser = parser
		self.client = None
		self.db = None


	def initDBConnection(self):
		try:
			self.client = MongoClient(env.DB_USER, env.DB_PORT, serverSelectionTimeoutMS=1)
			self.client.server_info()
			self.db = self.client[env.DB_BASE]
		except Exception as e:
			raise AssertionError("la connection a mongodb à échouer (" + str(e) + ")")	


	def closeDBConnection(self):
		self.client.close()


	def retryConnect(self):
		for i in range(5):
			try:
				self.initDBConnection()
				return True
			except Exception as e:
				print("Nouvelle tentative de reconnection " + str(i))
				time.sleep(1)

		raise AssertionError("Les tentative de reconnection on toute échouer, fin du programme")


	def run(self):
		raise NotImplementedError()


	def parse(self, html):
		return self.parser.parse(html)


	def runGetQuery(self, url):
		r = requests.get(url)
		if r.status_code == 200:
			return r.text
		if r.status_code == 410:
			raise Exception410("La page à été supprimée")	
		if r.status_code == 404:
			raise AssertionError("La page est introuvable (ou supprimer)")		
		if r.status_code == 500:
			raise AssertionError("Erreur du serveurs du site")




