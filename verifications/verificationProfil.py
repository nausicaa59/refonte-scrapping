from cerberus import Validator
from verifications import helpers
from verifications.errors import *


class VerificationProfil:
	def __init__(self, data):
		self.data = data
		self.schema = {
			'pseudo'			: {'type': 'string', 'empty': False,'required' : True},
			'dateInscription'	: {'type': 'string', 'empty': False,'required' : True},
			'nbMessages'		: {'type': 'integer', 'empty': False, 'required' : True},
			'imgLien'			: {'type': 'string', 'empty': False, 'required' : True},
			'nbRelation'		: {'type': 'integer', 'empty': False, 'required' : True},
			'banni'				: {'type': 'integer', 'empty': False, 'required' : True},
		}


	def controle(self):
		v = Validator(self.schema, allow_unknown = True)
		if v.validate(self.data) == False :
			raise ExceptionControle(str(v.errors))

		(valide, err) = helpers.dateIsValide(self.data["dateInscription"])
		if valide == False:
			raise ExceptionControle("date d'inscription invalide")


	def prepare(self):
		self.data["pseudo"] = self.data["pseudo"].lower()
		self.data['scrapped-profil'] = True
		self.data['scrapped-abonne'] = False
		self.data["dateInscription"] = helpers.parseDate(self.data["dateInscription"])