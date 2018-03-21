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


class Worker():
	def __init__(self, parser):
		self.parser = parser
		self.db = None


	def initDBConnection(self):
		try:
			self.db = MongoClient(env.DB_USER, env.DB_PORT, serverSelectionTimeoutMS=1)
			self.db.server_info()
			return self.db[env.DB_BASE]
		except Exception as e:
			raise AssertionError("la connection a mongodb à échouer (" + str(e) + ")")	



	def closeDBConnection(self):
		self.db.close()


	def run(self):
		raise NotImplementedError()


	def parse(self, html):
		return self.parser.parse(html)


	def runGetQuery(self, url):
		r = requests.get(url)
		print(r.status_code)
		if r.status_code == 200:
			return r.text
		if r.status_code == 410:
			raise AssertionError("La page à été supprimée")	
		if r.status_code == 404:
			raise AssertionError("La page est introuvable (ou supprimer)")		
		if r.status_code == 500:
			raise AssertionError("Erreur du serveurs du site")




