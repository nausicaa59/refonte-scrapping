from cerberus import Validator
from verifications import helpers


class VerificationSujets:
	def __init__(self, data):
		self.data = data
		self.schema = {
			'url'			: {'type': 'string', 'empty': False,'required' : True},
			'reference'		: {'type': 'string', 'empty': False, 'required' : True},
			'date'			: {'type': 'string', 'empty': False, 'required' : True},
			'nbReponse'		: {'type': 'integer', 'empty': False, 'required' : True},
			'auteur'		: {'type': 'string', 'empty': False, 'required' : True},
		}


	def controle(self):
		v = Validator(self.schema, allow_unknown = True)
		self.data = [x for x in self.data if v.validate(x)]
		return (True, None)



	def prepare(self):
		for i in range(len(self.data)):
			self.data[i]['auteur'] = self.data[i]['auteur'].lower()
			self.data[i]['date'] = helpers.parseDate(self.data[i]['date'])
		
		return (True, None)