import json
import os
from functions import *

siFile = "line search/dictionaries/siLines.json"
sFile = "line search/dictionaries/sLines.json"


siDict = {
    
}

sDict = {
    
}

for dictionary in [siDict, sDict]:
    for ion in dictionary:
        dictionary[ion] = [eVtoA(x) for x in dictionary[ion]]

for file,dic in {siFile:siDict, sFile:sDict}.items():
    if os.path.exists(file):
        pass
    else:
        dataEntryDict(dic, file, eVtoA, True)


