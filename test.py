#----------------------
# Init app
#----------------------
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/verifications")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/models")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/parseurs")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/workers")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/tools")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/global")


#----------------------
# Go !
#----------------------
from models import modelConnect
from models import modelProfil
from models import modelReponses
from models import modelSujets
from tools import generateurUrl

print(generateurUrl.startTopicPage("http://www.jeuxvideo.com/forums/42-51-50685036-1-0-1-0-alerte-chocapic-j-ai-eu-le-petale-d-or.htm", 284))
