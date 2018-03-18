import re
import datetime
from bs4 import BeautifulSoup
from parseurs.parseur import Parseur



class ParseurTopic(Parseur):
	def parse(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		return (self.getPagination(soup), self.getReponses(soup))


	def getReponses(self, soup):
		ouput = []
		reponses = soup.select(".bloc-message-forum")

		for reponse in reponses:
			try:
				ouput.append({
					"auteur": self.getPseudoReponse(reponse),
					"date": self.getDateReponse(reponse),
					"reference" : self.getReferenceReponse(reponse),
					"contenu" :self.getReponseContenu(reponse)				
				})
			except Exception as e:
				print("erreur lors l'extration")

		return ouput



	def getReponseContenu(self, reponse):
		data = {
			"content" : "",
			"citation" : [],
			"images" : { "smileys" : [], "other" : [] }
		}

		corps = reponse.select(".bloc-contenu")
		if corps == []:
			return ""
		
		#delete signature
		self.deleteElementBySelect(corps[0], ".signature-msg")

		# search auteur citation + delete
		data["citation"] = self.getReponseCitationAuteur(corps[0])
		self.deleteElementBySelect(corps[0], ".blockquote-jv")

		# get images
		imagesAll = self.getReponseImg(corps[0])
		data["images"]["smileys"] = [x for x in imagesAll if x.find("smileys") != -1]
		data["images"]["other"]   = [x for x in imagesAll if x.find("smileys") == -1]

		# delete liens
		self.deleteElementBySelect(corps[0], "a")
		self.deleteElementBySelect(corps[0], ".JvCare")
		self.deleteElementBySelect(corps[0], "img")
		self.deleteElementBySelect(corps[0], "b")
		self.deleteElementBySelect(corps[0], "i")

		for p in corps[0].select("p"):
			data["content"] += " " + p.get_text()

		return data


	def getReponseImg(self, html):
		images = html.select("img")
		if images == []:
			return []

		return [x["src"] for x in images if x.has_attr("src")]



	def getReponseCitationAuteur(self, reponse):
		regexGetPseudo = "\d{2}:\d{2}:\d{2}\s+(.+)\s+a écrit"
		citations = reponse.select(".text-enrichi-forum > .blockquote-jv")
		if citations == []:
			return []

		head = [x.select("> p:nth-of-type(1)")[0] for x in citations]
		if head == []:
			return []

		auteur = [x.get_text() for x in head]
		if auteur == []:
			return []

		reg = re.compile(regexGetPseudo)
		match = [reg.findall(x) for x in auteur]
		return [self.cleanEspace(x[0]) for x in match if len(x) > 0]



	def getReferenceReponse(self, reponse):
		if reponse.has_attr("data-id"):
			return reponse["data-id"]
		else:
			return False

	def getPseudoReponse(self, reponse):
		try:
			pseudo = reponse.select(".bloc-pseudo-msg")[0]
			return self.cleanEspace(pseudo.get_text())
		except Exception as e:
			print("Erreur extraction pseudo", str(e))
			return "inconnu"

	
	def getDateReponse(self, reponse):
		try:
			dateNode = reponse.select(".bloc-date-msg span")
			if dateNode == []:
				dateNode = reponse.select(".bloc-date-msg")

			date = dateNode[0].get_text().strip()
			return self.converteDate(date)
		except Exception as e:
			print("Erreur extraction date reponse", str(e))
			raise "0000-00-00 00:00:00"


	def converteDate(self, c):
		d = c.replace(' à ', ' ')
		d = d.replace("janvier", "01")
		d = d.replace('janvier', '01')
		d = d.replace('février', '02')
		d = d.replace('mars', '03')
		d = d.replace('avril', '04')
		d = d.replace('mai', '05')
		d = d.replace('juin', '06')
		d = d.replace('juillet', '07')
		d = d.replace('août', '08')
		d = d.replace('septembre', '09')
		d = d.replace('octobre', '10')
		d = d.replace('novembre', '11')
		d = d.replace('décembre', '12')
		return datetime.datetime.strptime(d, "%d %m %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

	def getPagination(self, soup):
		pagination = []
		navs = soup.select(".bloc-liste-num-page")
		if len(navs) == 0:
			return pagination

		itemsNav = navs[0].select("span")
		if len(itemsNav) == 1:
			return pagination

		currentPagePass = False
		for item in itemsNav:
			if item.has_attr("class"):
				if "page-active" in item["class"]:
					currentPagePass = True
			else:
				if currentPagePass == True:
					pagination.append('http://www.jeuxvideo.com' + item.select("a")[0]["href"])
		
		return pagination