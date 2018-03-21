from cerberus import Validator
from verifications import helpers


class VerificationReponses:
	def __init__(self, data):
		self.data = data
		self.schema = {
			'auteur'		: {'type': 'string', 'empty': False,'required' : True},
			'date'			: {'type': 'string', 'empty': False, 'required' : True},
			'reference'		: {'type': 'string', 'empty': False, 'required' : True},
			'contenu'		: {'required' : True},
			'sujet'			: {'type': 'string', 'empty': False, 'required' : True},
		}
		self.schemaContenu = {
			'content'		: {'required' : True},
			'citation'		: {'required' : True},
			'images'		: {'required' : True}
		}
		self.schemaImages = {
			'smileys'		: {'required' : True},
			'other'			: {'required' : True}
		}


	def controle(self):
		v = Validator(self.schema, allow_unknown = True)
		self.data = [x for x in self.data if v.validate(x)]

		v = Validator(self.schemaContenu, allow_unknown = True)
		self.data = [x for x in self.data if v.validate(x['contenu'])]
		
		v = Validator(self.schemaImages, allow_unknown = True)
		self.data = [x for x in self.data if v.validate(x['contenu']['images'])]

		return (True, None)


	def prepare(self):
		for i in range(len(self.data)):
			self.data[i]['auteur'] = self.data[i]['auteur'].lower()
			self.data[i]['date'] = helpers.parseDate(self.data[i]['date'])
			self.data[i]['contenu']['citation'] = [x.lower() for x in self.data[i]['contenu']['citation']]

		return (True, None)