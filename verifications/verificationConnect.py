from cerberus import Validator
from verifications import helpers


class VerificationConnect:
	def __init__(self, data):
		self.data = data
		self.schema = {
			'date'			: {'type': 'string', 'empty': False,'required' : True},
			'nbConnect'		: {'type': 'integer', 'empty': False, 'required' : True},
		}


	def controle(self):
		try:
			v = Validator(self.schema, allow_unknown = True)
			if v.validate(self.data) == False :
				return (False, v.errors)

			(valide, err) = helpers.dateIsValide(self.data["date"])
			if valide == False:
				return (False, {"date" : err})
		except Exception as e:
			return(False, str(e))
		
		return (True, None)


	def prepare(self):
		try:
			self.data["date"] = helpers.parseDate(self.data["date"])
		except Exception as e:
			return(False, str(e))
		
		return (True, None)