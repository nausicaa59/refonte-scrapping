#----------------------
# Init app
#----------------------
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/parseurs")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/workers")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/tools")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/global")


#----------------------
# Go !
#----------------------
from workers.factoryWorker import FactoryWorker

typeObj = None
for arg in sys.argv:
	if arg.find("-type=") is not -1:
		typeObj = arg.replace("-type=","")

w = FactoryWorker.make(typeObj)
w.getOption()
w.run()

