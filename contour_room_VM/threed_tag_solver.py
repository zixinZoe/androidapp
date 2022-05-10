import scipy.optimize
import numpy as np
import math
import matplotlib.pyplot as plt

#estimation: estimated tag location (x,y)
#DDoA: a matrix of distance difference of arrival
#anchor_locations: a matrix of anchor coordinates

#tag_location is the result tag location (x,y)

def tag_solver(estimation,args):
    def solve_fun(estimation,args):
        
        DDoA = args[0]
        # print("ddoa: ",DDoA)
        anchor_locations = args[1]
        # print("anchors: ",anchor_locations)
        zero_coor = args[2] #where tdoa = 0
        tag_locations = []

        for i in range(len(DDoA)):
            for j in range(len(DDoA)):
                # if DDoA[i][j] != 0:
                for coor in zero_coor:
                    if DDoA[i][j] != 0 or i == coor[0] and j == coor[1]:
                        tag_locations.append( -np.sqrt( (estimation[0]-anchor_locations[i][0])**2 + (estimation[1]-anchor_locations[i][1])**2 + (estimation[2]-anchor_locations[i][2])**2 ) 
                        + np.sqrt( (estimation[0]-anchor_locations[j][0])**2 + (estimation[1]-anchor_locations[j][1])**2 + (estimation[2]-anchor_locations[j][2])**2 )-DDoA[i][j])
        return tag_locations

    temp_result = scipy.optimize.root(solve_fun,estimation,args,method='lm')
    result =np.empty((0,3))
    #plt.scatter(np.vstack((result,temp_result.x))[:,0],np.vstack((result,temp_result.x))[:,1])
    # print('result: ',np.transpose(np.vstack((result,temp_result.x))))
    return np.transpose(np.vstack((result,temp_result.x)))

# anchor_locations = np.array([[0,0,0],[10,0,0],[0,10,0],[0,0,10]])
# DDoA = [[ 0. ,  10, 10 , 10],
#  [ 0.   ,       0.      ,    0.       ,   0.        ],
#  [ 0.    ,      0.       ,   0.      ,    0.        ],
#  [ 0.    ,      0.      ,    0.      ,    0.        ]]
# estimation = [0,0,0]
# anchor_locations = np.array([[0,0,0],[10,0,0],[0,10,0],[10,10,0]])
# DDoA = [[ 0. ,  1.36680054, -1.50811372 , 0.10159303],
#  [ 0.   ,       0.      ,    0.       ,   0.        ],
#  [ 0.    ,      0.       ,   0.      ,    0.        ],
#  [ 0.    ,      0.      ,    0.      ,    0.        ]]
# estimation = [10,10,10]
# zero_coor = [-1,-1]
# tag_solver(estimation,[DDoA,anchor_locations,zero_coor])
