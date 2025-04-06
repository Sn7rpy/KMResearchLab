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
        
        self.elements = []


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
    return json.load(os.path.join(os.path.dirname(__file__)),"dictionaries","siLines.json")

def sLines():
    return json.load(os.path.join(os.path.dirname(__file__)),"dictionaries","sLines.json")

def list_lines():
    apecFitsFile = os.path.join(os.environ["ATOMDB"], "apec_line.fits")

    with fits.open(apecFitsFile) as aFF:
        lines_data = aFF[1].data

    return