import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from tag_solver import tag_solver
from correction import antenna_correct_ddoa
import itertools

def GDOP(anchor_locations, tag_location):

    relative_distances = anchor_locations - np.transpose(tag_location)
    distance_vec = np.array([np.sqrt(np.sum(np.power(relative_distances,2), axis=1))]).T
    H = relative_distances / distance_vec
    Q = np.linalg.inv(np.dot(np.transpose(H),H))
    dop = np.sqrt(np.trace(Q))
    return dop

def NSDI_read_TDoA_new(line):

    anchor_combo = []
    dop_current = []
    count = 0

    anchor_locations = np.array([[0,0],
                            [3600,0],
                            [3600,3100],
                            [0, 3100]])

    antenna_delays = [-514.800046735725,
                    -515.807752377787,
                    -515.311106592656, 
                    -514.793541561308]


    tag_candidates = np.empty((2,0))

    parts = line.split("@")
    read_ids = parts[0].split(";")
    ids = []
    for read_id in read_ids: 
        id = int(read_id)
        ids.append(id)
    init_id = ids[0]
    resp_ids = ids[1:]
    read_tdoas = parts[1].split(";")
    tdoas = []
    for read_tdoa in read_tdoas:
        tdoa = int(read_tdoa)
        tdoas.append(tdoa)

    #if tdoas[0] < 100000 and tdoas[0] > -100000 and tdoas[1] < 100000 and tdoas[1] > -100000 and tdoas[0] < 100000 and tdoas[0] > -100000: #filter lines by DDoA
    if all(tdoa<100000 and tdoa>-100000 for tdoa in tdoas):

        D_complete = np.zeros((len(anchor_locations),len(anchor_locations)))
        index = 0
        for resp in resp_ids:
            D_complete[init_id,resp] = tdoas[index]
            index = index+1
        # print("d_complete: ",D_complete)
        combo2 = np.empty(shape=[0,2],dtype = np.int8)
        combo3 = np.empty(shape=[0,3],dtype = np.int8)

        for item in itertools.combinations(resp_ids,2):
            combo2 = np.append(combo2,np.array([item]),axis=0)
        for item in itertools.combinations(resp_ids,3):
            combo3 = np.append(combo3,np.array([item]),axis=0)

        # print("combo2: ",combo2)
        # print('combo3: ',combo3)
        tag_candidates = np.empty((2,0))
        cnt =0
        if combo2.any():

            for i in range(len(combo2)):
                idx = combo2[i][:]

                mask = np.zeros((len(anchor_locations),len(anchor_locations)))
                
                for resp in idx:
                    mask[init_id,resp] = 1
                DDoA = np.multiply(mask,D_complete)
                estimation = anchor_locations[0][:]
                tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)
                # print('tag_can2: ',tag_candidates)
                RESP_LIST = [init_id]
                for index in idx:
                    RESP_LIST = np.append(RESP_LIST,index)
                dop_current = np.append(dop_current,GDOP(anchor_locations[RESP_LIST,:],tag_candidates.T[cnt,:]))
                anchor_combo.append(RESP_LIST)
                count = count+1

        if combo3.any():
            for i in range(len(combo3)):
                idx = combo3[i][:]
                mask = np.zeros((len(anchor_locations),len(anchor_locations)))
                for resp in idx:
                    mask[init_id,resp] = 1
                DDoA = np.multiply(mask,D_complete)
                estimation = anchor_locations[0][:]+[1,1]
                tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)

                RESP_LIST = [init_id]
                for index in idx:
                    RESP_LIST = np.append(RESP_LIST,index)
                dop_current = np.append(dop_current,GDOP(anchor_locations[RESP_LIST,:],tag_candidates.T[cnt,:]))
                anchor_combo.append(RESP_LIST)
                count = count+1

        min_dop_idx = np.where(dop_current == np.amin(dop_current))[0][0]
        tagLoc = tag_candidates[:,min_dop_idx]
        print("tagLocsolver: ",tagLoc)
        return tagLoc
    else:
        print("tdoa too large")
        return []

