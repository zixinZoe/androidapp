import csv
import numpy as np

with open('../hikernet-export.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    count = 0
    locations = np.matrix([0,0])#locations of standards
    standard_loc = [0,0]
    #only record network connection status when a person moves 1km vertically or horizontally.
    for row in csv_reader: 
        if count >=4 and ((float(row[7])-standard_loc[0])>0.01 or (float(row[8])-standard_loc[1])>0.01): #0.01 in longitude and latitude is about 1km
            locations= np.vstack([locations,[float(row[7]),float(row[8])]]) #remember first actual location starts at index 1
            standard_loc = [float(row[7]),float(row[8])]
        count = count +1
print(locations)
    

