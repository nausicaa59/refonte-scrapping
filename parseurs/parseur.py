import re
import datetime


class Parseur:
	def parse(self, html):
		raise NotImplementedError()
	

	def decryptageUrl(self, candidat):
		base16 = "0A12B34C56D78E9F";
		str_ = ""
		rurl = "" 
		ch = 0
		cl = 0
		j = 0
		
		fragments = candidat.split(" ")
		for fragment in fragments:
			if len(fragment) > len(str_):
				str_ = fragment
		

		for i in range(0,len(str_)-1,2):
			ch = base16.find(str_[i])
			cl = base16.find(str_[i+1])
			rurl += chr((ch*16) + cl)

		return rurl


	def deleteElementBySelect(self, x, selection):
		elements = x.select(selection)
		if elements != []:
			for e in elements:
				e.decompose()	


	def cleanEspace(self, x):
		s = x.replace("\\n", "")
		s = s.replace(" ", "")
		s = s.strip()
		return s
