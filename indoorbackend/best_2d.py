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

def create_combos(resp_coor,combos):
    num_of_resp = len(resp_coor[:,0])
    for num in range(3,num_of_resp+1):#stay consistent with 3D model
        combo_num = np.empty(shape=[0,num],dtype = np.int8)
        for item in itertools.combinations(list(range(1,num_of_resp+1)),num):
            combo_num = np.append(combo_num,np.array([item]),axis=0)
        combos.append(combo_num)
    # print("combos: ",combos)
    return combos

def calc_combo(combos,locs,D_complete,seed,cnt,anchor_combo,tag_candidates,dop_current,init_index):
    for cur in range(0,len(combos)): #for each combo
        mask = np.zeros((len(locs[:,0]),len(locs[:,0]))) 
        zero_coor = [[-1,-1]]
        if combos[cur].any():
            for i in range(len(combos[cur])): #for each responder
                resp = combos[cur][i]       
                mask[0,resp] = 1 
        DDoA = np.multiply(mask,D_complete)
        for idx in range(len(DDoA[init_index])):
            if DDoA[init_index][i] == 0 and i != init_index:
                zero_coor.append([init_index,i]) 
        # print("zerocoor2d: ",zero_coor)
        tag_candidates = np.append(tag_candidates,tag_solver(seed,[DDoA,locs,zero_coor]),axis =1)
        RESP_LIST = [0]
        RESP_LIST = np.append(RESP_LIST,resp)
        dop_current = np.append(dop_current,GDOP(locs[RESP_LIST,:],tag_candidates.T[cnt,:]))
        anchor_combo.append(RESP_LIST)
    return [dop_current,tag_candidates]

def read(locs,noisy_tdoa_list,seed,sampleNum,initNum):
    tag_candidates = []
    for sample in noisy_tdoa_list:
        init_index = 0
        D_complete = np.zeros((len(locs[:,0]),len(locs[:,0])))
        D_complete[init_index] = sample
        tag_cand = np.empty((2,0))
        cnt =0
        anchor_combo = []
        dop_current = []
        combos = [] #list of combos of different sizes
        combos = create_combos(locs[1:],combos)
        result = calc_combo(combos,locs,D_complete,seed,cnt,anchor_combo,tag_cand,dop_current,init_index)
        dop_current = result[0]
        tag_cand = result[1]
        min_dop_idx = np.where(dop_current == np.amin(dop_current))[0][0]
        tagLoc = tag_cand[:,min_dop_idx]
        tagLoc = np.reshape(np.array(tagLoc),((1,2)))
        tag_candidates.append(tagLoc[0].tolist())
    tag_candidates = np.array(tag_candidates)
    tag_candidates = np.reshape(tag_candidates,((sampleNum,2)))
    return tag_candidates

