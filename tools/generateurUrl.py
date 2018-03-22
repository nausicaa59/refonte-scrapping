import random

NB_TOPIC_BY_PAGE = 25
PATH_DRIVER_GOOGLE = "C:/piloteweb/chromedriver.exe"
PATH_INIT_PAGE_LISTE = "http://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm"
PATH_DEFAULT_AVATAR = "http://image.jeuxvideo.com/avatar-md/default.jpg"
PATERN_PATH_PAGE_LISTE = "http://www.jeuxvideo.com/forums/0-51-0-1-0-[X]-0-blabla-18-25-ans.htm"
PATERN_PATH_AUTEUR_PROFIL = "http://www.jeuxvideo.com/profil/[X]?mode=infos"
PATERN_PATH_AUTEUR_FAVORIS = "http://www.jeuxvideo.com/profil/[X]?mode=favoris"
PATERN_PATH_AUTEUR_ABONNES = "http://www.jeuxvideo.com/profil/[X]?mode=abonne"
PATERN_PATH_RECHERCHE_AUTEUR_TOPIC = "http://www.jeuxvideo.com/recherche/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm?search_in_forum=[X]&type_search_in_forum=auteur_topic"
PATERN_PATH_RECHERCHE_AUTEUR_MESSAGE = "http://www.jeuxvideo.com/recherche/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm?search_in_forum=[X]&type_search_in_forum=texte_message"


def homePageById(id):
	return PATERN_PATH_PAGE_LISTE.replace("[X]", str(id))


def homePageRandom(minV = 0, maxV = 10):
	if minV >= maxV:
		minV = 0
		maxV = 10
	
	page = random.randint(minV, maxV)
	nbTopic = (NB_TOPIC_BY_PAGE*page) + 1
	urlPage = homePageById(nbTopic)
	return urlPage


def homePageNext(currentNb, left = True):
	newNb = currentNb - NB_TOPIC_BY_PAGE if left else currentNb + NB_TOPIC_BY_PAGE
	newNb = newNb if newNb > 0 else 0
	return (newNb, homePageById(newNb))


def homePage(id):
	return PATERN_PATH_PAGE_LISTE.replace("[X]", str(id))


def userProfil(pseudo):
	return PATERN_PATH_AUTEUR_PROFIL.replace("[X]", pseudo)


def userAbonne(pseudo):
	return PATERN_PATH_AUTEUR_ABONNES.replace("[X]", pseudo)


def startTopicPage(url, nbReponse):
	if nbReponse == 0:
		return url

	segments = url.split("/")
	if len(segments) <= 0:
		return url

	fragments = segments[-1].split("-")
	if len(fragments) <= 4:
		return url

	numPage = (nbReponse // 20)
	if numPage <= 0:
		return url

	fragments[3] = str(numPage)
	segments[-1] = '-'.join(fragments)
	return '/'.join(segments)
