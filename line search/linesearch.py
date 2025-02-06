#By Violet da Motta
#script to scan a line search .par file and return a list of possible ions for each line 

import pyatomdb
import numpy as np
from parameters import *
from pylatex import (
    Alignat,
    Axis,
    Document,
    Figure,
    Math,
    Matrix,
    Plot,
    Section,
    Subsection,
    Tabular,
    TikZ,
)


#pick the file to be scanned
file = "line search/searchFiles/zlines_30.par"
if file == "":
    file = input("What file should I do? \n")

createPDF = True

#check the parameters file for the method
parL= getParameterList(file)

#Break down the parameters from the file into a class so that the parameters are more easily acessible
parCL =[]
for n in parL:
    parCL.append(parameterFrame(n))

#grouping all of the parameters of one line into the same dictionary entry
parTGD =dict()
for m in parCL:
    
    #ignore any of the parameters that don't refeer to lines
    if m.name.startswith("ga"):
        pass
    else:
        continue

    #split the name of the parameter into the line index and the parameter
    nameM= m.name.split(".")

    #check if the line index is already in the dictionary
    if nameM[0] in parTGD.keys():
        m.name = nameM[1]
        parTGD[nameM[0]].append(m)
    else:
        m.name = nameM[1]
        parTGD[nameM[0]]=[m]


session = pyatomdb.spectrum.CIESession()

elementsD = {
    1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B",
    6: "C", 7: "N", 8: "O", 9: "F", 10: "Ne",
    11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
    16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca",
    21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn",
    26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn",
    31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br",
    36: "Kr", 37: "Rb", 38: "Sr", 39: "Y", 40: "Zr",
    41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh",
    46: "Pd", 47: "Ag", 48: "Cd", 49: "In", 50: "Sn",
    51: "Sb", 52: "Te", 53: "I", 54: "Xe", 55: "Cs",
    56: "Ba", 57: "La", 58: "Ce", 59: "Pr", 60: "Nd",
    61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb",
    66: "Dy", 67: "Ho", 68: "Er", 69: "Tm", 70: "Yb",
    71: "Lu", 72: "Hf", 73: "Ta", 74: "W", 75: "Re",
    76: "Os", 77: "Ir", 78: "Pt", 79: "Au", 80: "Hg",
    81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At",
    86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac", 90: "Th",
    91: "Pa", 92: "U", 93: "Np", 94: "Pu", 95: "Am",
    96: "Cm", 97: "Bk", 98: "Cf", 99: "Es", 100: "Fm",
    101: "Md", 102: "No", 103: "Lr", 104: "Rf", 105: "Db",
    106: "Sg", 107: "Bh", 108: "Hs", 109: "Mt", 110: "Ds",
    111: "Rg", 112: "Cn", 113: "Nh", 114: "Fl", 115: "Mc",
    116: "Lv", 117: "Ts", 118: "Og"
}

#setting up the information for the latex document
if createPDF:
    geometry_opt= {"tmargin": "1cm", "lmargin": "1cm"}
    doc = Document(geometry_options=geometry_opt)


temperature = 1
linesL=[]
#loops through all of the different lines in the dictionary
for keys,items in parTGD.items():
    #resets the tolerance value
    tolerance = 0.01
    #sorts the lines into classes for ease of access 
    lineC = emissionLine(keys, items)
    #keep searching for lines until there are at least 2 line candidates
    while len(lineC.elements) <= 2:
        lineC.elements = session.return_linelist(temperature, [lineC.lambdaA-tolerance, lineC.lambdaA+tolerance])
        tolerance += 0.01
    #Sort the possible lines by emissivity
    lineC.elements.sort(order="Epsilon")
    lineC.elements = lineC.elements[::-1]

    linesL.append(lineC)

    print(lineC.elements)
   # print(f"index: {c.index}, energy: {c.energy}, wavelegth: {c.lambdaA}, elements: {c.elements}")

#so now I need to turn this whole thing into a latex document
# which means:
# printing the header what line is this refeering to and what its measured values were
# Printing out all of the possible lines or some selection of them

#this is a horrible nested mess but I don't fully understand how this laTeX library works tbh

with doc.create(Section(file)):
    for Line in linesL:
        with doc.create(Subsection(Line.index)):
            doc.append(f"Energy: {Line.energy}, Sigma: {Line.sigma}, Lambda: {Line.lambdaA}")
            with doc.create(Tabular("l l l l")) as tablE:
                tablE.add_row(["Element:Ion |Up to Low", "Lambda", "Emissivity", "Redshift"])
                tablE.add_hline()
                count = 0
                for pL in Line.elements:
                    if count > 6:
                        break
                    tablE.add_row([f"{elementsD[pL[-4]]}:{pL[-3]} |{pL[-2]} to {pL[-1]}", pL[0], pL[2], Line.lambdaA-pL[0]])
                    count += 1
                tablE.add_hline()

doc.generate_pdf("line search/latexFiles/zlines30", clean_tex=False)





print('hello')
