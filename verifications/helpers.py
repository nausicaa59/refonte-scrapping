import validus
import datetime


def dateIsValide(c, f = "%Y-%m-%d %H:%M:%S"):
	if validus.istime(c, f) == False:
		return (False, "La date du message n'est pas valide")		
	return (True, None)


def parseDate(s, f = "%Y-%m-%d %H:%M:%S"):
	return datetime.datetime.strptime(s, f)