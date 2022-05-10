import itertools
import numpy as np
from correction import antenna_correct_ddoa
from tag_solver import tag_solver
from numpy.linalg import inv
from operator import itemgetter 
from array import *
import math
import matplotlib.pyplot as plt

#RESP_ID:a list of respond IDs
#init_id:the initiator ID
#FP_PW: a list of first path power
#anchor_locations: a np matrix
#tag_location:[]
def tag_filter_power(RESP_ID, init_id, TDoA, FP_PW, anchor_locations,tag_location,antenna_delays):
    
    tagLoc = []
    dop=0
    anchor_combo=[]
    candidate=[]
    candidate_dop=[]
    tag_candidates=[]
    dop_current=[]

    #filter weak anchors
    a = range(0,len(FP_PW))#indexes of FP_PW items
    strong_indexes = [i for (i,j) in zip(a,FP_PW) if j>-110]#indexes of strong FP_PW
    num_strong = len(strong_indexes)
    strong_idx = []

    if(num_strong>5):
        [sorted_FP_PW,new_a] = zip(*(sorted(zip(FP_PW,a),key = lambda t: t[0])))
        #print('/////',sorted(zip(FP_PW,a),key = lambda t: t[0]))
        strong_idx = new_a[-5:]#indexes of the top5 FP_PW

    elif(num_strong>=2):
        strong_idx = strong_indexes
    else:
        result = [tagLoc,dop,anchor_combo,candidate,candidate_dop,tag_candidates,dop_current]
        return result

    #create combinations of anchors
    combo2 = np.empty(shape=[0,2],dtype = np.int8)
    combo3 = np.empty(shape=[0,3],dtype = np.int8)
    combo4 = np.empty(shape=[0,4],dtype = np.int8)
    combo5 = np.empty(shape=[0,5],dtype = np.int8)

    if(len(strong_idx) == 2):
        combo2 = np.append(combo2,np.array([strong_idx]),axis=0)

    elif(len(strong_idx) == 3):
        for item in itertools.combinations(strong_idx,2):
            combo2 = np.append(combo2,np.array([item]),axis=0)
        for item in itertools.combinations(strong_idx,3):
            combo3 = np.append(combo3,np.array([item]),axis=0)

    elif(len(strong_idx) == 4):
        for item in itertools.combinations(strong_idx,2):
            combo2 = np.append(combo2,np.array([item]),axis=0)
        for item in itertools.combinations(strong_idx,3):
            combo3 = np.append(combo3,np.array([item]),axis=0)
        for item in itertools.combinations(strong_idx,4):
            combo4 = np.append(combo4,np.array([item]),axis=0)

    elif(len(strong_idx) == 5):
        for item in itertools.combinations(strong_idx,2):
            combo2 = np.append(combo2,np.array([item]),axis=0)
        for item in itertools.combinations(strong_idx,3):
            combo3 = np.append(combo3,np.array([item]),axis=0)
        for item in itertools.combinations(strong_idx,4):
            combo4 = np.append(combo4,np.array([item]),axis=0)
        for item in itertools.combinations(strong_idx,5):
            combo5 = np.append(combo5,np.array([item]),axis=0)

    DDoA_all = np.zeros((len(anchor_locations),len(anchor_locations)))

    DDoA_all[init_id][RESP_ID]=TDoA
    for i in range(len(DDoA_all)):
        for j in range(len(DDoA_all)):
            if DDoA_all[i][j] != 0:
                DDoA_all[i][j] = antenna_correct_ddoa(DDoA_all[i][j],i,j,antenna_delays)

    A = anchor_locations.transpose()

    tag_candidates = np.empty((2,0))
    count =0
    if combo2.any():

        for i in range(len(combo2)):
            idx = combo2[i][:]

            mask = np.zeros((len(anchor_locations),len(anchor_locations)))
            for index in idx:
                mask[init_id,RESP_ID[index]] = 1
            DDoA = np.multiply(mask,DDoA_all)

            estimation = anchor_locations[0][:]
            tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)

            RESP_LIST = [init_id]
            for index in idx:
                RESP_LIST = np.append(RESP_LIST,RESP_ID[index])
            dop_current = np.append(dop_current,GDOP(anchor_locations[RESP_LIST,:],tag_candidates.T[count,:]))
            anchor_combo.append(RESP_LIST)
            count = count+1

    if combo3.any():
        for i in range(len(combo3)):
            idx = combo3[i][:]
            mask = np.zeros((len(anchor_locations),len(anchor_locations)))

            for index in idx:
                mask[init_id,RESP_ID[index]] = 1
            DDoA = np.multiply(mask,DDoA_all)

            estimation = anchor_locations[0][:]+[1,1]
            tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)

            RESP_LIST = [init_id]
            for index in idx:
                RESP_LIST = np.append(RESP_LIST,RESP_ID[index])
            dop_current = np.append(dop_current,GDOP(anchor_locations[RESP_LIST,:],tag_candidates.T[count,:]))
            anchor_combo.append(RESP_LIST)
            count = count+1

    if combo4.any():
        for i in range(len(combo4)):
            idx = combo4[i][:]
            mask = np.zeros((len(anchor_locations),len(anchor_locations)))
            for index in idx:
                mask[init_id,RESP_ID[index]] = 1
            DDoA = np.multiply(mask,DDoA_all)
            estimation = anchor_locations[0][:]

            tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)

            tag = np.transpose(tag_candidates)
            plt.scatter(tag[:,0]*66/5/304.8,tag[:,1]*66/5/304.8)


            RESP_LIST = [init_id]
            for index in idx:
                RESP_LIST = np.append(RESP_LIST,RESP_ID[index])
            dop_current = np.append(dop_current,GDOP(anchor_locations[RESP_LIST,:],tag_candidates.T[count,:]))
            anchor_combo.append(RESP_LIST)
            count = count+1

    if combo5.any():
        for i in range(len(combo5)):
            idx = combo5[i][:]
            mask = np.zeros((len(anchor_locations),len(anchor_locations)))
            for index in idx:
                mask[init_id,RESP_ID[index]] = 1
            DDoA = np.multiply(mask,DDoA_all)
            estimation = anchor_locations[0][:]
            tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)

            tag = np.transpose(tag_candidates)
            plt.scatter(tag[:,0]*66/5/304.8,tag[:,1]*66/5/304.8)


            RESP_LIST = [init_id]
            for index in idx:
                RESP_LIST = np.append(RESP_LIST,RESP_ID[index])

            dop_current = np.append(dop_current,GDOP(anchor_locations[RESP_LIST,:],tag_candidates.T[count,:]))
            anchor_combo.append(RESP_LIST)
            count = count+1

    min_dop_idx = np.where(dop_current == np.amin(dop_current))[0][0]
    tagLoc = tag_candidates[:,min_dop_idx]

    a = range(len(dop_current))
    idx = np.argsort(dop_current)
    idx = idx[0:(np.amin([2,len(idx)-1])+1)]

    if len(idx) == 1:
        candidate = tag_candidates
        candidate_dop = dop_current[0]
    else:
        for index in idx:
            candidate.append(tag_candidates[:,index])
            candidate_dop = np.append(candidate_dop, dop_current[index])

    dop = dop_current[min_dop_idx]
    anchor_combo = anchor_combo[min_dop_idx] 

    result = [tagLoc,dop,anchor_combo,candidate,candidate_dop,tag_candidates,dop_current]
    return result

#anchor_locations: locations of chosen anchors(size:n*2)
#tag_location: one tag location(size:n*2)
def GDOP(anchor_locations, tag_location):

        relative_distances = anchor_locations - np.transpose(tag_location)
        distance_vec = np.array([np.sqrt(np.sum(np.power(relative_distances,2), axis=1))]).T
        H = relative_distances / distance_vec
        Q = inv(np.dot(np.transpose(H),H))
        dop = np.sqrt(np.trace(Q))
        return dop



# RESP_ID = [1,2,3]
# init_id = 0
# TDoA = np.array([1.36680054, -1.50811372,  0.10159303])
#         # [34.3,0,34,5],
#         # [45.3,34,0,556],
#         # [4,5,556,0]])
# #print('\\\\\\\\\\',type(TDoA))
# FP_PW = [-35.64,-4,-3]
# #print('+++++++++',type(FP_PW))
# anchor_locations = np.array([[0,0],[10,0],[0,10],[10,10]])
# tag_locations = []

# antenna_delays = [-514.800046735725,
#                 -515.807752377787,
#                 -515.311106592656, 
#                 -515.115189872074,
#                 -514.882780169421,
#                 -513.592856014242,
#                 -514.918087972098,
#                 -515.128385013776,
#                 -514.793541561308,
#                 -515.321036364222,
#                 -515.241712743109,
#                 -514.973272610434,
#                 -514.989929612259]
# #print('========',len(antenna_delays))

# tag_filter_power(RESP_ID,init_id,TDoA, FP_PW,anchor_locations, tag_locations,antenna_delays)
# #tag_location = [[1,2]]
# #GDOP(anchor_locations, tag_location)
