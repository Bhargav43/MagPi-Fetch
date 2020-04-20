import requests
import sys, os
from TextPrinter import threadstart, threadquit

global_selectionlist = dict()

def writePDF(name, url, loc):
    global global_selectionlist
    if global_selectionlist[name]:
        threadstart('Writing '+name)
        reqObj = requests.get(url, stream=True)
        with open(os.path.join(loc, name), 'wb') as f:
            f.write(reqObj.content)
        threadquit()