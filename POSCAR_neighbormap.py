## program to create neighbourmap of each atom
###
# Assumptions
# Line 3 in input file has vector 'a'
# Line 4 in input file has vector 'b'
# Line 5 in input file has vector 'c'
# From line 9 in input file direct co-ordinates of atoms start
###

import math
import sys

inputFilename = sys.argv[1]        #Input file name
outputFilename = sys.argv[2]      #Output file name
atomPos = {}   #ion position pair
writeln = []  #variable that stores data to be written on  output file
limitDistance = 10.0       #threshold distance to determine nearest atom
f1 = open(inputFilename,"r")    #Open file for reading
lines=f1.readlines()            #Read all lines from the file
f1.close()

####
##Function to convert direct coordinates to cartesian
def d2c(va,vb,vc,direct):
    cartesian = []
    for k1 in range (0,3):
        cartesian.append(str(float(va[k1])*float(direct[0])+float(vb[k1])*float(direct[1])+float(vc[k1])*float(direct[2])))
    return(cartesian)
####

####
## Function to calculate distance between 2 atoms with direct co-ordinates
def distanceCalc(va,vb,vc,d1,d2):
    c1 = d2c(va,vb,vc,d1)
    c2 = d2c(va,vb,vc,d2)
    return(math.sqrt((float(c1[0]) - float(c2[0])) ** 2 + (float(c1[1]) - float(c2[1])) ** 2 + (float(c1[2]) - float(c2[2])) ** 2))
####

vecApos = 3  # Line 3 in file has vector 'a'
vecBpos = 4  # Line 4 in file has vector 'b'
vecCpos = 5  # Line 5 in file has vector 'c'
fileStartPosition = 8   #atom's co-ordinate data starts from line 9 of file
for k1 in range (0,fileStartPosition-1):    #reading vectors 'a', 'b', 'c'
    writeln.append(lines[k1])
    if (k1==vecApos-1):
        a = lines[k1].split()
    if (k1 == vecBpos-1):
        b = lines[k1].split()
    if (k1 == vecCpos-1):
        c = lines[k1].split()

##dictionary of all atoms and their direct co-ordinates
atom = 1
for k in range (fileStartPosition,len(lines)):    #loop through each line of file
    line=lines[k].strip()          #remove spaces from each line
    line1=line.split("#")
    line2=line1[0].strip()
    if(len(line2.split())==3):
        atomPos[atom] = line2
        atom = atom + 1

#repliate unit cube in  3-d space
rValue = [0,1,-1] #list of values to change along a, b, and c unit vectors
unitCubes = []   #list of replicated unit cubes
for a1 in rValue:
    for b1 in rValue:
        for c1 in rValue:
            repAtom={}
            for i in range(1,len(atomPos.keys())+1):
                p1 = atomPos[i].split()
                repAtom[i] = str(float(p1[0])+a1)+"  "+str(float(p1[1])+b1)+"  "+str(float(p1[2])+c1)
            unitCubes.append(repAtom)

heading =  "atom   position                              nearest neighbor table\n"
writeln.append(heading)

#for k3 in range (0,len(unitCubes)):
for k1 in range(1,len(atomPos.keys())+1):
    p1=atomPos[k1].split()
    l1 = str("%2d" %k1)+"   "+str("%10.6f" %float(p1[0]))+"   "+str("%10.6f" %float(p1[1]))+"   "+str("%10.6f" %float(p1[2]))+"    "
    count=0
    for k3 in range (0,len(unitCubes)):
        for k2 in range(1,len(unitCubes[k3].keys())+1):
            if(k3==0 and k1 == k2):
                continue
            p2=unitCubes[k3][k2].split()
            l2 = str("%2d" %k2)+"   "+str("%10.6f" % float(p2[0])) + "   " + str("%10.6f" % float(p2[1])) + "   " + str("%10.6f" % float(p2[2]))
            distance = distanceCalc(a,b,c,p1,p2)
            if(distance < limitDistance):
                if (count == 0):
                    writeln.append(l1 + l2 + "   " + str("%5.3f" %distance)+"\n")
                else:
                        writeln.append(45*" "+ l2 + "   " + str("%5.3f" %distance)+"\n")
                count = count + 1
    if(count == 0):
        writeln.append(l1+"\n")

fo = open(outputFilename, "w")
fo.writelines(writeln)
fo.close()
