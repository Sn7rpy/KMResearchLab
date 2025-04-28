import json 
from astropy.io import fits
import numpy as np
import os

def getUnits(fileName):
    par = open(fileName)
    raw_list = par.read().split('\n')
    raw_list.pop(0)
    newlist = []
    for string in raw_list[0].split(' '):
        if string != '':
            newlist.append(string)
    return newlist

def getParameterList(fileName):
    par = open(fileName)
    raw_list = par.read().split('\n')
    raw_list.pop(0)
    raw_list.pop(0)
    divided = []
    for lit in raw_list:
        newlist = []
        for string in lit.split(' '):
            if string != '':
                newlist.append(string)
        divided.append(newlist)
    divided.pop()
    return divided

def makeTable(filename):
    parametersList = getParameterList(filename)
    result = r"\begin{table}[] \begin{tabular}{l r} Parameter & Value \\ \hline "+"\n"
    for n in parametersList:
        if n[3] == '1':
            result += n[1]+"(f) & $"+n[4]+"_{"+n[5]+"}^{"+n[6]+r"} $ \\ "+"\n"
        else:
            result += n[1]+" & $"+n[4]+"_{"+n[5]+"}^{"+n[6]+r"} $ \\ "+"\n"
    
    result += r"\end{tabular} \end{table} "
    return result

def sorter(a):
    return a[2]

class parameterFrame:
    def __init__(self,listS=list):
        self.index = int(listS[0])
        self.name = listS[1]
        self.tie = listS[2]
        self.freeze = int(listS[3])
        self.value = float(listS[4])
        self.min = float(listS[5])
        self.max = float(listS[6])
        try:
            self.unit = listS[7]
        except:
            self.unit = ' '

class emissionLine:
    def __init__(self, inx, listS=list):
        for n in listS:
            if n.name == "EQW":
                self.energy = n.value
                #store the parameter class in case we want to use that still
                self.energyC = n
            elif n.name == "Lambda":
                self.lambdaA = n.value
                self.lambdaAC=n
            elif n.name == "Sigma":
                self.sigma = n.value
                self.sigmaC = n
            elif n.name == "Redshift":
                continue
            else:
                print("skipped a parameter? review the emissionLine class")
                continue

        self.index = inx
        
        self.elementsPlus = []
        self.elementsADB = []


def convertRoman(number = int):
    roman = {1000:"M", 900:"CM", 500:"D", 400:"CD", 100:"C", 90:"XC", 50:"L", 40:"XL", 10:"X", 9:"IX", 5:"V", 4:"IV",1:"I"}
    ogNum= number
    output=""
    if number <0:
        print("negative number input into convertRoman() method")
        return("0")
    for i,j in roman.items():
        while number >= i:
            output += j
            number -=i
    
    if number == 0:
        return(output)
    else:
        print(f"Something went wrong with converting {ogNum} into {output}")

def eVtoA(eV):
    return 12398/float(eV)

def AtokeV(A):
    return eVtoA(A)/1000

def mAtokeV(mA):
    A=mA*1e-3
    return 12.398/(A)

def eqwSigmatokeV(mA,lamb):
    A=mA*1e-3
    return (12.398*A)/(lamb**2)


def dataEntryDict(outputDict = {}, outputFile = None, convertFunc=None, addMore=True):
    if addMore:
        key = input("key name: ")
        item = input ("item name: ")
        while key != "done":
            if convertFunc ==None:
                outputDict[key] = float(item)
            else:
                outputDict[key] = convertFunc(item)
            key = input("key name (or type\"done\" to end): ")
            item = input ("item name: ")
    
    if outputFile != None:
        with open(outputFile, "w") as file:
            json.dump(outputDict, file)
        print(f"written {outputDict} to {outputFile}")


def siLines():
    path = os.path.join(os.path.dirname(__file__),"dictionaries","siLines.json")
    with open(path, "r") as file:
        return json.load(file)

def sLines():
    path = os.path.join(os.path.dirname(__file__),"dictionaries","sLines.json")
    with open(path, "r") as file:
        return json.load(file)

def list_lines(wavelength, tolerance = 0.3, minEm= 1e-18):
    apecFitsFile = os.path.join(os.environ["ATOMDB"], "apec_line.fits")

    with fits.open(apecFitsFile) as aFF:
        data = aFF[2].data
        mask = (data["Lambda"] > wavelength/(tolerance+1)) & (data["Lambda"] < wavelength/(1-tolerance))
        tableT = data[mask]

        for n in range(3,203):
            data = aFF[n].data
            mask = (data["Lambda"] > wavelength/(tolerance+1)) & (data["Lambda"] < wavelength/(1-tolerance))
            tableT = np.concatenate([tableT,data[mask]])
        
        mask = tableT["Epsilon"] > minEm
        tableT = tableT[mask]
        tableT.sort(order="Epsilon")
        tableT = tableT[::-1]

        _, idx = np.unique(tableT[['Element', 'Ion', 'UpperLev', 'LowerLev']], return_index=True)
        uniqueTable = tableT[idx]

        uniqueTable.sort(order="Epsilon")
        uniqueTable = uniqueTable[::-1]


    return uniqueTable

