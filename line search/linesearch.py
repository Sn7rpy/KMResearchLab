#By Violet da Motta
#script to scan a line search .par file and return a list of possible ions for each line 

import pyatomdb
import numpy as np
from parameters import *



#pick the file to be scanned and the name of the output file
file = "line search/searchFiles/zlines_30.par"
output = "line search/latexFiles/zlines30"
if file == "":
    file = input("What file should I do? \n")

#declaring the default values for the atomdb queary
initialTolerance = 0.01
toleranceStep = 0.01
temperature = 1
temperatureStep = 1

#flag for the code to create the LaTeX pdf or not
#WILL THROW OUT ERRORS IF YOU DON'T HAVE PACKAGES TO RENDER LATEX DOCUMENTS (MacTeX for Macs, MikTeX for Windows)
createPDF = True

#flag to do the plot of redshifts
shiftSearch = True

if createPDF:
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
if shiftSearch:
    import matplotlib.pyplot as plt

#check the parameters.py file for the how this method works
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

    #remove the (1) from the name
    nameM[0]=nameM[0][:-3]

    #check if the line index is already in the dictionary
    if nameM[0] in parTGD.keys():
        m.name = nameM[1]
        parTGD[nameM[0]].append(m)
    else:
        m.name = nameM[1]
        parTGD[nameM[0]]=[m]

#setting up atomdb 
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



linesL=[]
#loops through all of the different lines in the dictionary
for keys,items in parTGD.items():
    #resets the tolerance value
    tolerance = initialTolerance
    #sorts the lines into classes for ease of access 
    lineC = emissionLine(keys, items)
    #keep searching for lines until there are at least 3 line candidates
    while len(lineC.elements) <= 2:
        #add the list of possible emission lines to the line's parameters
        lineC.elements = session.return_linelist(temperature, [lineC.lambdaA-tolerance, lineC.lambdaA+tolerance])
        tolerance += toleranceStep

    #Sort the possible lines by emissivity (increasing)
    lineC.elements.sort(order="Epsilon")
    #reverse the order so the strongest line is first
    lineC.elements = lineC.elements[::-1]

    #add the line class to a list of them so that they can be easily parsed
    linesL.append(lineC)

    #print(lineC.elements)
    print(f"index: {lineC.index}, energy: {lineC.energy}, wavelegth: {lineC.lambdaA}, elements: {lineC.elements}")


#setting up the plotting for the redshifts
if shiftSearch:
    plt.figure(figsize=(50, 5))

#this is a horrible nested mess but I don't fully understand how this laTeX library works tbh
#I can probably put this inside the previous loop for the sake of efficiency but sacrificing the readability of the code
if createPDF:
    #Lable the section with the filename
    with doc.create(Section(file)):
        #loop over the list of line classes created in the last section of the code
        for Line in linesL:
            #Create a subsection for the particular line being evaluated
            with doc.create(Subsection(Line.index)):
                #label the subsection with information about the possible line
                doc.append(f"Energy: {Line.energy}, Sigma: {Line.sigma}, Lambda: {Line.lambdaA}")
                #initiate the table that will contain the possible likes 
                with doc.create(Tabular("l l l l")) as tablE:
                    #header and line underneeth for neatness 
                    tablE.add_row(["Element:Ion |Up to Low", "Lambda", "Emissivity", "Redshift"])
                    tablE.add_hline()
                    #resetting the counter so that only 6 possible lines are listed
                    count = 0
                    for pL in Line.elements:
                        redshift = Line.lambdaA-pL[0]
                        if count > 6:
                            break

                        if shiftSearch and count<1:
                            plt.plot(redshift,(np.log10(pL[2])+19), ".")
                            plt.text(redshift, (np.log10(pL[2])+19)+0.1, f"{Line.index}")
                            pass

                        tablE.add_row([f"{elementsD[pL[-4]]}:{convertRoman(pL[-3])} |{pL[-2]} to {pL[-1]}", pL[0], pL[2], redshift])
                        count += 1
                    tablE.add_hline()
    #self explanatory
    doc.generate_pdf(output, clean_tex=False)

#todo:
#figure out how to add the shift search plot to the latex document
#add the option to search by temperature

if shiftSearch:
    plt.show()

print('everything ran fine')
