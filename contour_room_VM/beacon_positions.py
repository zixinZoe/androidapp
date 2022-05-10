import math
import numpy as np
roomX = 40
roomY = 20
sample_distance = 1
threshold = 2
anchorNum = 4
r = 1
locations = np.array([[0,0],[10,20],[20,0],[40,20]])
#read error matrix from file
with open('error_matrix1', 'rb') as inFile:
    data = inFile.read()
    data = np.frombuffer(data,dtype=float)
data = np.reshape(data,(int((roomX+1)//sample_distance),int((roomY+1)//sample_distance)))
position = np.argwhere(data>threshold) #samples that require beacon
with open('sample_pos1', 'wb') as saveFile:
    position_data = position.tobytes()
    saveFile.write(position_data)
print("positions: ",position)
print("len: ",len(position))

#read tdoas from file
with open('tdoas1', 'rb') as inFile:
    data = inFile.read()
    data = np.frombuffer(data,dtype=float)
# tdoas = np.reshape(data,(int((roomX+1)//sample_distance),int((roomY+1)//sample_distance)))
tdoa_list = np.reshape(data,((roomX//sample_distance+1),(roomY//sample_distance+1),(anchorNum-1)))
# position = np.argwhere(data>threshold) #samples that require beacon
# print(position)
# print("tdoas0: ",tdoas[0])

#we use anchor 0,n
n = 1
tan_t2 = (locations[0,1]-locations[1,1])/(locations[0,0]-locations[1,0])
c = np.sqrt((locations[0,1]-locations[1,1])**2+(locations[0,0]-locations[1,0])**2)/2
a_list = []
for pos in position:
    a = tdoa_list[pos[0],pos[1]][n]/2
    a_list.append(a)
a_list = np.array(a_list)
b_list = np.sqrt(c**2-a_list**2)
# print("b_list: ",b_list)
# print("a_list[0]",a_list[0])
# print("b_list[0]",b_list[0])
# print("c: ",c)
tan_t1_list = []
for i in range(len(position)):
    tan_t1_list.append(position[i][0]*b_list[i]**2/position[i][1]*a_list[i]**2)
tan_t1_list = np.array(tan_t1_list)
# print("klist: ",tan_t1_list)

# print("tan_t1_list+tan_t2: ",tan_t1_list+tan_t2)
# print("1-tan_t1_list*tan_t2: ",1-tan_t1_list*tan_t2)
k_list = []
for tan_t1 in tan_t1_list:
    if np.abs(tan_t1) == math.inf:
        k_list.append(-tan_t2**(-1))
    elif np.abs(tan_t2) == math.inf:
        k_list.append(-tan_t1**(-1))
    else:
        k_list.append((tan_t1+tan_t2)/(1-tan_t1*tan_t2))
# print("k_list: ",k_list)

x_coor_list = []
y_coor_list = []
i = 0
for pos in position:
    x = np.abs(r/np.sqrt(1+k_list[i]**2))
    x_coor_list.append(pos[0]+x)
    y_coor_list.append(pos[1]+x*k_list[i])
    i+=1
beacon_pos = np.array(list(zip(x_coor_list,y_coor_list)))
print("beacon_pos: ",beacon_pos)
with open('beacons1', 'wb') as saveFile:
    beacon_data = np.array(beacon_pos).tobytes()
    saveFile.write(beacon_data)
# distance = [] #distance between beacons and target samples
# for i in range(len(position)):
#     distance.append(np.sqrt((beacon_pos[i][0]-position[i][0])**2+(beacon_pos[i][1]-position[i][1])**2))
# print("distance: ",distance)
