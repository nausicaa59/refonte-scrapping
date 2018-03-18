import re
import datetime
from bs4 import BeautifulSoup
from parseurs.parseur import Parseur


class ParseurPageListe(Parseur):
	def parse(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		return (self.getSujets(soup), self.getNbConnecte(soup))


	def getNbConnecte(self, soup):
		dictNbCo = {
			"date" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"nbConnect" : 0	
		}

		try:
			nbConnect = soup.select(".nb-connect-fofo")
			if nbConnect == []:
				return dictNbCo

			num = re.findall("(\d+)", nbConnect[0].get_text())
			if num == None:
				return dictNbCo

			dictNbCo["nbConnect"] = int(num[0])
			return dictNbCo
		except Exception as e:
			return 0


	def getSujets(self, soup):
		listSujets = []
		liste = soup.select(".topic-list li")
		for item in liste:
			if item["class"] == ['']:
				listSujets.append(self.getSujet(item))

		return listSujets


	def getSujet(self, item):
		lien = item.select("a.lien-jv.topic-title")[0]["href"]
		nbReponse = item.select(".topic-count")[0].get_text().strip()
		auteur = item.select(".topic-author")[0].get_text().strip()

		return {
			'url' : 'http://www.jeuxvideo.com' + self.cleanEspace(lien),
			'reference' : self.extractRef(lien),
			'date': self.extractDate(item),
			'nbReponse' : int(nbReponse),
			'auteur': self.cleanEspace(auteur)
		}


	def extractDate(self, item):
		date = item.select(".topic-date span")[0].get_text().strip()
		date = self.cleanEspace(date)
		
		isFullDate = re.findall("^\d{2}\/\d{2}\/\d{4}$", date)
		if len(isFullDate) > 0:
			dateObj = datetime.datetime.strptime(date, "%d/%m/%Y")
			return dateObj.strftime("%Y-%m-%d %H:%M:%S")

		isOnlyHour = re.findall("^\d{2}:\d{2}:\d{2}$", date)
		if len(isOnlyHour) > 0:
			complement = datetime.datetime.now().strftime("%Y-%m-%d ")
			return complement + date
		
		return date


	def extractRef(self, url):
		search = re.findall("^\/forums\/\d+-51-(\d+)-", url)
		if len(search) > 0:
			return search[0]
		return False


	def nbConnectes(self, html):
		d = pq(html)
		nb = d(".nb-connect-fofo").html();
		nb = tools.regexOnlyValue("([0-9]*)",nb)
		return nb
