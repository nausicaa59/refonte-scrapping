from cerberus import Validator
from verifications import helpers
from verifications.errors import *

class VerificationConnect:
	def __init__(self, data):
		self.data = data
		self.schema = {
			'date'			: {'type': 'string', 'empty': False,'required' : True},
			'nbConnect'		: {'type': 'integer', 'empty': False, 'required' : True},
		}


	def controle(self):
		v = Validator(self.schema, allow_unknown = True)
		if v.validate(self.data) == False :
			raise ExceptionControle("Invalide data : " + str(v.errors))

		(valide, err) = helpers.dateIsValide(self.data["date"])
		if valide == False:
			raise ExceptionControle("Invalide date : " + err)


	def prepare(self):
		self.data["date"] = helpers.parseDate(self.data["date"])