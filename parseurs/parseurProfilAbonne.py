import re
import datetime
from bs4 import BeautifulSoup
from parseurs.parseur import Parseur


class ParseurProfilAbonne(Parseur):
	def parse(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		abonnes = self.getAbonnes(soup)
		pagination = self.getPagination(soup)
		return (pagination, abonnes)


	def getAbonnes(self, soup):
		wrapperAbonnes = soup.select(".group-fiche-abonne .bloc-info-abonne .pseudo")
		abonnes = [x.select("a:nth-of-type(1)") for x in wrapperAbonnes]
		abonnes = [x[0].get_text() for x in abonnes if len(x) > 0]
		return [self.cleanEspace(x).lower() for x in abonnes]


	def getPagination(self, soup):
		wrapperPagination = soup.select(".bloc-pagi-default .pagi-after")
		if len(wrapperPagination) == 0:
			return []
		
		nextLink = wrapperPagination[0].select("span span:nth-of-type(1)")
		if len(nextLink) == 0:
			return []

		if nextLink[0].has_attr("class") == False:
			return []

		return [self.decryptageUrl(x) for x in nextLink[0]["class"] if len(x) > 20]

