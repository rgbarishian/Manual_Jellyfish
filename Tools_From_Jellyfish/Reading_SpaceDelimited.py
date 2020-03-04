from tkinter import Tk
from tkinter.filedialog import askopenfilename

#filename = askopenfilename()
file = open('Possible_Jellies.reg', 'r')

x=[]
y=[]
flux=[]
for line in file:
    fields = line.split()
    x.append(float(fields[0]))
    y.append(float(fields[1]))
    flux.append(float(fields[2]))
file.close()
print(x)
print(y)
print(flux)
print(sum(x))
