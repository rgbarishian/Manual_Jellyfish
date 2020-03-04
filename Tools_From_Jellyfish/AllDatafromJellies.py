#Ryan Barishian, University of Alabama in Huntsville, 2018-2019
#With the help of Elliot Codd, William Waldron, and Dr. Ming Sun
#This script is a conversion of Elliot Codd's MatLab script to find Jellyfish Galaxies

#Import libraries
import numpy as np
import math
from astropy.io import ascii
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time

#User inputs
print("Select sextractor.dat")
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
scale = float(input("Scale (kpc/\"): "))
start_time = time.time()
#data = ascii.read('/home/ryan/Documents/Manual_Jelly/Fall_19/HST_Relics/A2495/sextractor.dat') #directory of dat file
data = ascii.read(filename) #new
#Import Data
#Define arrays of data from columns in data
Flux_all = data['FLUX_BEST']
Kron_all = data['KRON_RADIUS']
X_all = data['X_WORLD']
Y_all = data['Y_WORLD']
A_all = data['A_WORLD']
B_all = data['B_WORLD']
#Constants
#Common Scales: #A520: 3.325;A68: 3.903; A370: 5.162; AA1758a: 4.244 ;A2744: 4.536; to to calculate use ned wrights calculator H0 = .7, Omega-m = .3, flat
outerRad = 40/scale/3600
sigma = 2.5

#Specify threasholds for a galaxy
min_gal_flux = 15
max_gal_flux = float('inf')
min_gal_kronA = 2e-4 #"minkron * A" IDK
max_gal_kronA = float('inf')
GalIndex = np.logical_and(np.logical_and(Flux_all > min_gal_flux, Flux_all < max_gal_flux), np.logical_and(Kron_all*A_all > min_gal_kronA, Kron_all < max_gal_kronA))

#Create array by extracting only those that tested as galaxies
Flux_Gal = Flux_all[GalIndex]
Kron_Gal = Kron_all[GalIndex]
X_Gal = X_all[GalIndex]
Y_Gal = Y_all[GalIndex]
A_Gal = A_all[GalIndex]
B_Gal = B_all[GalIndex]
#Create array of galaxies fitting certain conditions
Good_GalIndex = (Kron_Gal*B_Gal>0.000400) #Value choosen by guess and check
Flux_Gal = Flux_Gal[Good_GalIndex]
Kron_Gal = Kron_Gal[Good_GalIndex]
X_Gal = X_Gal[Good_GalIndex]
Y_Gal = Y_Gal[Good_GalIndex]
A_Gal = A_Gal[Good_GalIndex]
B_Gal = B_Gal[Good_GalIndex]

#Region file of galaxies
fid = open('galaxy.reg', 'w')
fid.close()
for i in range(len(Flux_Gal)):
    fid = open('galaxy.reg','a')
    fid.write("j2000; annulus %fd %fd %fd %fd\n" % (X_Gal[i], Y_Gal[i], B_Gal[i] * Kron_Gal[i], outerRad))
fid.close()
fid = open('galaxy.txt', 'w')
fid.close()
for i in range(len(Flux_Gal)):
    fid = open('galaxy.txt','a')
    fid.write("%f %f %fd\n" % (X_Gal[i], Y_Gal[i], Flux_Gal[i]))
fid.close()

#Remove Galaxies from main array, leaving array of independent stars/sources
Gal_X_Not = X_all[np.logical_not(GalIndex)]
Gal_Y_Not = Y_all[np.logical_not(GalIndex)]
Gal_A_Not = A_all[np.logical_not(GalIndex)]
Gal_B_Not = B_all[np.logical_not(GalIndex)]
Gal_Flux_Not = Flux_all[np.logical_not(GalIndex)]
Kron_Not = Kron_all[np.logical_not(GalIndex)]

#region file of non galaxies
for i in range(len(Gal_Flux_Not)):
    fid = open('nongalaxy.reg','a')
    fid.write("j2000; point %fd %fd\n" % (Gal_X_Not[i], Gal_Y_Not[i]))
fid.close()
for i in range(len(Gal_Flux_Not)):
    fid = open('nongalaxy.txt','a')
    fid.write("%f %f %f\n" % (Gal_X_Not[i], Gal_Y_Not[i], Gal_Flux_Not[i]))
fid.close()

#Create file that all sources in annulus will be exported to (can be removed in final verision)
fid = open('Sources_inany_Annulus.reg', 'w')
fid.close()

#Create regions file of possible Jellyfish Galaxies
fid = open('Possible_Jellies.reg', 'w')
fid.close()
fid = open('Possible_Jellies.txt', 'w')
fid.close()

#Loop through each galaxy
for i in range(len(X_Gal)):
    Index_Sources_in_Annulus=[]  
    #Loop through each source and see if it is in bounds of said galaxy
    for j in range(len(Gal_X_Not)):
        Index_Sources_in_Annulus.append(((((X_Gal[i] - Gal_X_Not[j])**2) + ((Y_Gal[i]- Gal_Y_Not[j])**2) <= (outerRad)**2)) and (((X_Gal[i] - Gal_X_Not[j])**2) + (Y_Gal[i] - Gal_Y_Not[j])**2 >= (B_Gal[i]*(Kron_Gal[i]))**2))
    X_Source_in_Annulus = Gal_X_Not[Index_Sources_in_Annulus]
    Y_Source_in_Annulus = Gal_Y_Not[Index_Sources_in_Annulus]
    A_Source_in_Annulus = Gal_A_Not[Index_Sources_in_Annulus]
    B_Source_in_Annulus = Gal_B_Not[Index_Sources_in_Annulus]
    Flux_Source_in_Annulus = Gal_Flux_Not[Index_Sources_in_Annulus]
    Kron_Source_in_Annulus = Kron_Not[Index_Sources_in_Annulus]
    
    #Export all sources that are in an annulus to document (Can be removed in final version)
    fid = open('Sources_inany_Annulus.reg','a')
    for j in range(len(X_Source_in_Annulus)):
        fid.write("j2000; point %fd %fd\n" % (X_Source_in_Annulus[j], Y_Source_in_Annulus[j]))
    fid.close
    fid = open('Sources_inany_Annulus.txt','a')
    for j in range(len(X_Source_in_Annulus)):
        fid.write("%f %f %f\n" % (X_Source_in_Annulus[j], Y_Source_in_Annulus[j], Flux_Source_in_Annulus[j]))
    fid.close
    #Get angle between x,y position of source with origin being galaxy
    X_Shifted = []
    Y_Shifted = []
    for j in range(len(X_Source_in_Annulus)):
        X_Shifted.append(X_Source_in_Annulus[j] - X_Gal[i])
        Y_Shifted.append(Y_Source_in_Annulus[j] - Y_Gal[i])
    Angles = np.arctan2(Y_Shifted, X_Shifted)

    Bins = np.arange(0,361,30)
    histdata = np.histogram(Angles,Bins)
    Counts_in_Bins = histdata[0] #Array listing number of items in each bin
    bins = np.arange(0,361,30)
    Total_in_Annulus = sum(Counts_in_Bins)
    
    Counts_in_Segments=[]
    Max_Count_in_3Bin_Segment = 0
    for j in range(len(Counts_in_Bins)):
    #Conditions for if any set of 3 is >= sigm
        if j+1 >= len(Counts_in_Bins):
            target1 = Counts_in_Bins[10]
            target2 = Counts_in_Bins[11]
            target3 = Counts_in_Bins[0]
            target = [target1, target2, target3]
        elif j == 0:
            target1 = Counts_in_Bins[11]
            target2 = Counts_in_Bins[0]
            target3 = Counts_in_Bins[1]
            target = [target1, target2, target3]
        else:
            target = Counts_in_Bins[j-1:j+2]
        
        Count_in_3Bin_Segment = sum(target)
        Counts_in_Segments.append(Count_in_3Bin_Segment)
        if Count_in_3Bin_Segment > Max_Count_in_3Bin_Segment:
            Max_Count_in_3Bin_Segment = Count_in_3Bin_Segment
    Non_Max_Counts = Total_in_Annulus - Max_Count_in_3Bin_Segment
    Non_Max_Average = Non_Max_Counts/11
    #Calculating if sources in annulus are unevenly distributed
    if np.logical_and((Max_Count_in_3Bin_Segment - Non_Max_Average)/math.sqrt(Non_Max_Average) >= sigma, Max_Count_in_3Bin_Segment>6):
        #if Flux_Gal[i] < 10000:
        fid = open('Possible_Jellies.reg','a')
        fid.write("j2000; annulus %fd %fd %fd %fd\n" % (X_Gal[i], Y_Gal[i], B_Gal[i] * Kron_Gal[i], outerRad))
        Radius_Annulus=[]
        for k in range(len(X_Source_in_Annulus)):
            Radius_Not = B_Source_in_Annulus[k] * Kron_Source_in_Annulus[k]
            Radius_Annulus.append(Radius_Not)
            fid.write("j2000; circle %fd %fd %fd\n" % (X_Source_in_Annulus[k], Y_Source_in_Annulus[k], Radius_Annulus[k]))
        fid.close()
        fid = open('Possible_Jellies.txt','a')
        fid.write("%f %f %f\n" % (X_Gal[i], Y_Gal[i], Flux_Gal[i]))
        Radius_Annulus=[]
        for k in range(len(X_Source_in_Annulus)):
            Radius_Not = B_Source_in_Annulus[k] * Kron_Source_in_Annulus[k]
            Radius_Annulus.append(Radius_Not)
            fid.write("%f %f %f\n" % (X_Source_in_Annulus[k], Y_Source_in_Annulus[k], Flux_Source_in_Annulus[k]))
        fid.close()


print(filename)
#Diagnostics Output
print("\n\nDiagnostics\nGalaxy: %s\nScale: %f\n# of Galaxies: %d" %(filename, scale, len(X_Gal)))
print("# of Sources: %d" %(len(Gal_X_Not)))
print("Time Elapsed:", time.time()-start_time)

#