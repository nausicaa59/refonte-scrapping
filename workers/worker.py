import sys
import requests
import time
import random
import pika
import json
import datetime
from tools import generateurUrl
from env import env


class Worker():
	def __init__(self, parser):
		self.parser = parser
		self.canalSendOutput 	= env.WORKER_CANALSEND_OUTPUT
		self.canalSendIsOk 		= env.WORKER_CANALSEND_ISOK
		self.canalRead			= env.WORKER_CANALREAD
		self.serverMQ 			= env.WORKER_SERVERMQ
		self.verbose			= env.WORKER_VERBOSE
		self.freq				= env.WORKER_FREQ


	def run(self):
		raise NotImplementedError()


	def parse(self, html):
		return self.parser.parse(html)


	def getOption(self):
		for arg in sys.argv:
			if arg.find("-v") is not -1:
				self.verbose = True
			if arg.find("-freq=") is not -1:
				self.freq = int(arg.replace("-freq=",""))


	def sendMsg(self, typeMsg, data):
		msg = self.createMsg(typeMsg, data)
		connection = pika.BlockingConnection(pika.ConnectionParameters(self.serverMQ))
		channel = connection.channel()
		channel.queue_declare(queue=self.canalSendOutput)
		channel.basic_publish(exchange='', routing_key=self.canalSendOutput, body=msg)	
		connection.close()


	def sendMsgIsOk(self, typeWorker):
		msg = self.createMsgIsOk(typeWorker)
		connection = pika.BlockingConnection(pika.ConnectionParameters(self.serverMQ))
		channel = connection.channel()
		channel.queue_declare(queue=self.canalSendIsOk)
		channel.basic_publish(exchange='', routing_key=self.canalSendIsOk, body=msg)	
		connection.close()


	def createMsgIsOk(self, typeWorker):
		return json.dumps({
			"dateCreated" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"type" : typeWorker 			
		})


	def createMsg(self, typeMsg, data):
		return json.dumps({
			"dateCreated" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"type" : typeMsg, 
			"data" : data 
		})


	def runGetQuery(self, url):
		r = requests.get(url)
		if r.status_code == 200:
			return r.text
		if r.status_code == 410:
			raise AssertionError("La page à été supprimée")	
		if r.status_code == 404:
			raise AssertionError("La page est introuvable (ou supprimer)")		
		if r.status_code == 500:
			raise AssertionError("Erreur du serveurs du site")


	def makeReadCanal(self, callback, typeOrder):
		connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.serverMQ))
		channel = connection.channel()
		channel.queue_declare(queue=self.WORKER_CANALREAD+"-"+typeOrder)
		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(callback, queue=typeOrder, no_ack=True)
		channel.start_consuming()	





