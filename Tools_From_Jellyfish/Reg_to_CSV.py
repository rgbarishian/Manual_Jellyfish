from tkinter import Tk
from tkinter.filedialog import askopenfilename
import csv

filename = askopenfilename() 

with open('filename') as infile, open('filenamev', 'w') as outfile:
    for line in infile:
        outfile.write(" ".join(line.split()).replace(' ', ','))
        outfile.write(",") # trailing comma shouldn't matter

# Unneeded columns are deleted from the csv

input = open('filenamev', 'rb')
output = open('filenamecsvout', 'wb')
writer = csv.writer(output)
for row in csv.reader(input):
    if row:
        writer.writerow(row)
input.close()
output.close()

with open("filenamecsvout","rb") as source:
    rdr= csv.reader( source )
    with open("filenamebarray","wb") as result:
        wtr= csv.writer(result)
        for r in rdr:
            wtr.writerow( (r[5], r[6], r[7]) )