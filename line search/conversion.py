# program to convert Angstrom to KeV
# Author: Anand Basu

# Instructions for use:

# Make sure .par files are in same directory as this program
# Run python3 conversion.py and place .par files as arguments
# Ex: python3 conversion.py filename1.par filename2.par
# Will output filename1_kev.par and filename2_kev.par


#plancks constant in ev
h = 4.135667662e-15
c = 299792458


import sys

# ensure filenames are passed as arguments
if len(sys.argv) == 1:
    raise Exception("Please add filename(s) to arguments")

# loop through files
for i in range(1, len(sys.argv)):
    # read in file
    f_read = open(sys.argv[i])
    # generate name of file to write to
    write_file_name = sys.argv[i].removesuffix(".par")
    write_file_name += "_kev.par"

    f_write = open(write_file_name, "w")

    # loop through file
    for line in f_read:
        #useful flag
        useful = False

        # mA or A
        multiplier = 0

        # value is in milliangstroms
        if line[-3:-1] == "mA":
            # set useful flag and multiplier for milliangstrom
            useful = True
            multiplier = 1e-13

        # value is in angstroms
        elif line[-3:-1].strip() == "A":
            # set useful flag and multiplier for angstrom
            useful = True
            multiplier = 1e-10

        if useful:
            # unit label
            label = "eV"

            # get values from file
            value = float(line[44:52].strip())
            minimum = float(line[56:64].strip())
            maximum = float(line[68:76].strip())

            meter = value * 1e-10
            meter_min = minimum * 1e-10
            meter_max = maximum * 1e-10

            energy = (h * c) / meter
            energy_min = (h * c) / meter_min
            energy_max = (h * c) / meter_max

            energy = round(energy, 6)
            energy_min = round(energy_min, 6)
            energy_max = round(energy_max, 6)

            if energy > 1000:
                energy = energy / 1000
                energy_min = energy_min / 1000
                energy_max = energy_max / 1000
                label = "keV"

            f_write.write(line[0:44])
            f_write.write(str(energy)[0:8])
            f_write.write("    ")
            f_write.write(str(energy_min)[0:8])
            f_write.write("    ")
            f_write.write(str(energy_max)[0:8])
            f_write.write(f"  {label}\n")


        # value does not need to be converted
        else:
            f_write.write(line)



