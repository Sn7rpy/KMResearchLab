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