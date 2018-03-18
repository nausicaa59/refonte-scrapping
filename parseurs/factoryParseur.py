from parseurs.parseurPageListe import ParseurPageListe 
from parseurs.parseurTopic import ParseurTopic 
from parseurs.parseurProfil import ParseurProfil 
from parseurs.parseurProfilAbonne import ParseurProfilAbonne 


class FactoryParseur:
	@staticmethod
	def make(type):
		if type == "sujet":
			return ParseurPageListe()
		if type == "topic":
			return ParseurTopic()
		if type == "profil":
			return ParseurProfil()
		if type == "abonne":
			return ParseurProfilAbonne()
		raise AssertionError("Aucun parseur trouver: " + type)