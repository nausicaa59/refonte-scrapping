from cerberus import Validator
from verifications import helpers
from verifications.errors import *

class VerificationAbonne:
	def __init__(self, data):
		self.data = data
		self.schema = {
			'pseudo'			: {'type': 'string', 'empty': False,'required' : True},
			'abonnes'			: {'type': ['string', 'list'], 'empty': True,'required' : True},
		}


	def controle(self):
		v = Validator(self.schema, allow_unknown = True)
		if v.validate(self.data) == False :
			raise ExceptionControle(str(v.errors))


	def prepare(self):
		try:
			self.data["pseudo"] = self.data["pseudo"].lower()
			self.data["abonnes"] = [x.lower() for x in self.data["abonnes"]]
		except Exception as e:
			raise ExceptionTransformation(str(v.errors))
