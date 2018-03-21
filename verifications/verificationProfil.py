from cerberus import Validator
import helpers


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
			return (False, v.errors)

		(valide, err) = helpers.dateIsValide(self.data["dateInscription"])
		if valide == False:
			return (False, {"dateInscription" : err})


		return (True, None)



	def prepare(self):
		try:
			self.data["pseudo"] = self.data["pseudo"].lower()
			self.data['scrapped-profil'] = True
			self.data['scrapped-abonne'] = False
			self.data["dateInscription"] = helpers.parseDate(self.data["dateInscription"])
		except Exception as e:
			return(False, str(e))
		
		return (True, None)