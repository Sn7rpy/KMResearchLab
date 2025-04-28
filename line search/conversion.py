# program to convert Angstrom to KeV
# Author: Anand Basu

# Instructions for use:

# Make sure .par files are in same directory as this program
# Run python3 conversion.py and place .par files as arguments
# Ex: python3 conversion.py filename1.par filename2.par
# Will output filename1_kev.par and filename2_kev.par
# will also generate temp.par, this file can be ignored


hc = 12400 # plancks constant * c in eV * angstrom


import sys

class Line:
    def __init__(self, name, tie_to, freeze, value, min, max, unit):
        self.name = name
        self.tie_to = tie_to
        self.freeze = freeze
        self.value = value
        if max < min:
            self.min = max
            self.max = min
        else:
            self.min = min
            self.max = max
        self.unit = unit

    def __str__(self):
        toRet = f"  {self.name}"
        toRet += f"{self.tie_to}     {self.freeze}"
        while len(toRet) < 41:
            toRet += " "
        if len(str(self.value)) == 7:
            toRet += " "
        toRet += f"{self.value}"
        for i in range(12 - len(str(self.min))):
            toRet += " "
        toRet += f"{self.min}"
        for i in range(12 - len(str(self.max))):
            toRet += " "
        toRet += f"{self.max}"
        toRet += f"  {self.unit}\n"

        return toRet
        

class Gaussian:
    def __init__(self, eqw, lambdaE, sigma, redshift):
        self.eqw = eqw
        self.lambdaE = lambdaE
        self.sigma = sigma
        self.redshift = redshift



# ensure filenames are passed as arguments
if len(sys.argv) == 1:
    raise Exception("Please add filename(s) to arguments")

# loop through files
for i in range(1, len(sys.argv)):
    # read in file
    f_read = open(sys.argv[i])

    # create temp file with lambda value before eqw and sigma
    temp_file = open("temp.par", "w")
    temp = ''
    for line in f_read:
        if "Lambda" in line:
            temp_file.write(line)
            temp_file.write(temp)
        elif "EQW" in line:
            temp = line
        else:
            temp_file.write(line)
        
    temp_file.close()

    to_read = open("temp.par", "r")

    # generate name of file to write to
    write_file_name = sys.argv[i].removesuffix(".par")
    write_file_name += "_kev.par"

    f_write = open(write_file_name, "w")

    # loop through file
    lambdaval = 0

    # initialize list of gaussians and lines to write as they are
    gausses = []
    other = []

    # each param for a whole gaussian
    cur_lambda = 0
    cur_eqw = 0
    cur_sigma = 0
    cur_redshift = 0
    counter = 0
    for line in to_read:
        #useful flag
        useful = False

        make_new = False

        #lambda flag
        lambdaf = False

        #redshift flag
        redshift = False

        # mA or A
        multiplier = 0

        # value is in milliangstroms
        if line[-3:-1] == "mA":
            # set useful flag and multiplier for milliangstrom
            useful = True
            multiplier = 1e-3

        # value is in angstroms
        elif line[-3:-1].strip() == "A":
            # set useful flag and multiplier for angstrom
            useful = True
            lambdaf = True
            multiplier = 1

        if counter == 3:
            useful = True
            redshift = True

        if useful:

            # dont modify redshift line
            if redshift:
                pass
            else:
                # unit label
                label = "keV"

                # get values from file
                value = float(line[44:52].strip())
                minimum = float(line[56:64].strip())
                maximum = float(line[68:76].strip())

                angstrom = value * multiplier
                angstrom_min = minimum * multiplier
                angstrom_max = maximum * multiplier

                # is line itself
                if lambdaf:
                    energy = hc / angstrom
                    energy_min = hc / angstrom_min
                    energy_max = hc / angstrom_max
                    lambdaval = angstrom

                # is eqw or sigma value
                else:
                    energy = (hc * angstrom) / (lambdaval ** 2)
                    energy_min = (hc * angstrom_min) / (lambdaval ** 2)
                    energy_max = (hc * angstrom_max) / (lambdaval ** 2)

                energy = energy / 1000
                energy_min = energy_min / 1000
                energy_max = energy_max / 1000

                energy = round(energy, 6)
                energy_min = round(energy_min, 6)
                energy_max = round(energy_max, 6)


                cur_line = Line(line[5:28], line[28:29], line[34:35], energy, energy_min, energy_max, label)

            # set line variables
            if counter == 0:
                cur_lambda = cur_line
                counter += 1
            elif counter == 1:
                cur_eqw = cur_line
                counter += 1
            elif counter == 2:
                cur_sigma = cur_line
                counter += 1
            elif counter == 3:
                cur_redshift = line
                counter = 0
                gauss = Gaussian(cur_eqw, cur_lambda, cur_sigma, cur_redshift)
                gausses.append(gauss)

        # value does not need to be converted
        else:
            other.append(line)
            # f_write.write(line)

    # sort gaussian lines
    gausses.sort(key=lambda x: x.eqw.value)
    
    # write the two header lines
    for i in range(2):
        f_write.write(other[i])

    idx = 1
    while True:
        try:
            gauss = gausses.pop()
            # format idx properly
            if idx >= 100:
                f_write.write(str(idx))
            elif idx >= 10:
                f_write.write(f" {idx}")
            else:
                f_write.write(f"  {idx}")
            idx += 1
            # write eqw
            f_write.write(str(gauss.eqw))

            #write lambda
            
            if idx >= 100:
                f_write.write(str(idx))
            elif idx >= 10:
                f_write.write(f" {idx}")
            else:
                f_write.write(f"  {idx}")
            idx += 1
            f_write.write(str(gauss.lambdaE))

            # write sigma
            if idx >= 100:
                f_write.write(str(idx))
            elif idx >= 10:
                f_write.write(f" {idx}")
            else:
                f_write.write(f"  {idx}")
            idx += 1
            f_write.write(str(gauss.sigma))

            #write redshift
            if idx >= 100:
                f_write.write(str(idx))
            elif idx >= 10:
                f_write.write(f" {idx}")
            else:
                f_write.write(f"  {idx}")

            idx += 1
            f_write.write(gauss.redshift[3:])

        except IndexError as e:
            break

    # write the remainder of the lines that did not need to be converted
    for i in range(2, len(other)):
        f_write.write(other[i])



