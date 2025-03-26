import json
import os
from functions import *

siFile = "line search/siLines.json"
sFile = "line search/sLines.json"


siDict = {
    "He-like Si XIII": [1853.67, 1839.33],
    "Li-like Si XII": [1845.09],
    "Be-like Si XI": [1828.29, 1824.15],
    "B-like Si X": [1809.02, 1806.02],
    "Li-like Si XI": [],
    "C-like Si IX": [1794.0, 1790.34, 1786.85],
    "N-like Si VIII": [1774.29, 1770.5, 1766.9],
    "O-like Si VII": [1758.7, 1756.0, 1751.4],
    "F-like Si VI": [1742.88],
    "Ne-like Si V": [1765.18],
    "Na–Si-like Si I–IV": [1740.04]
}



sDict = {
    "Li-like S XIV": [2450.0, 2447.02, 2437.797, 2414.7],
    "He-like S XV": [2430.380],
    "Be-like S XIII": [2418.51, 2412.0],
    "B-like S XII": [2395.51, 2391.36],
    "C-like S XI": [2378.26, 2373.25, 2368.83],
    "N-like S X": [2354.33, 2349.94, 2345.6],
    "O-like S IX": [2335.6, 2331.82, 2327.2],
    "F-like S VIII": [2315.00],
    "Na-like S VI": [2311.22],
    "B-like S XII": [2306.9]
}

for dictionary in [siDict, sDict]:
    for ion in dictionary:
        dictionary[ion] = [eVtoA(x) for x in dictionary[ion]]

for file,dic in {siFile:siDict, sFile:sDict}.items():
    if os.path.exists(file):
        pass
    else:
        dataEntryDict(dic, file, eVtoA, False)


