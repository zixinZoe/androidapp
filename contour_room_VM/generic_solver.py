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
    for num in range(2,num_of_resp+1):
        combo_num = np.empty(shape=[0,num],dtype = np.int8)
        for item in itertools.combinations(list(range(1,num_of_resp+1)),num):
            combo_num = np.append(combo_num,np.array([item]),axis=0)
        combos.append(combo_num)
    # print(combos)
    return combos

def calc_combo(combos,locs,D_complete,init_coor,cnt,anchor_combo,tag_candidates,dop_current):
    for cur in range(0,len(combos)):
        if combos[cur].any():
            for i in range(len(combos[cur])):
                idx = combos[cur][i][:]
                zero_coor = [-1,-1]
                mask = np.zeros((len(locs[:,0]),len(locs[:,0])))                
                for resp in idx:
                    mask[0,resp] = 1
                    if D_complete[0,resp] == 0:
                        zero_coor = [0,resp]
                DDoA = np.multiply(mask,D_complete)
                estimation = init_coor
                # estimation = [1000,1000]
                # print('init_coor: ',init_coor)
                tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,locs,zero_coor]),axis =1)
                # print('tag_can2: ',tag_candidates)
                RESP_LIST = [0]
                for index in idx:
                    RESP_LIST = np.append(RESP_LIST,index)
                dop_current = np.append(dop_current,GDOP(locs[RESP_LIST,:],tag_candidates.T[cnt,:]))
                anchor_combo.append(RESP_LIST)
    return [dop_current,tag_candidates]

#input format: “x0,y0;x1,y1;x2,y2;x4,y4@TDoA01,TDoA02,TDoA04”
def NSDI_read_TDoA_new(line):
    if '@' in line:
        anchor_combo = []
        dop_current = []

        tag_candidates = np.empty((2,0))

        parts = line.split("@")
        # print('parts0: ',parts[0])
        read_locs = parts[0].split(";")
        locs = np.zeros((len(read_locs),2))
        num = 0
        for read_loc in read_locs: 
            coors = read_loc.split(",")
            x = int(coors[0])
            y = int(coors[1])
            locs[num][0] = x
            locs[num][1] = y
            num = num+1

        init_coor = locs[0,:]
        resp_coor = locs[1:,:]
        read_tdoas = parts[1].split(";")
        print("read_tdoas: ",read_tdoas)
        tdoas = []

        for read_tdoa in read_tdoas:
            tdoa = int(float(read_tdoa))
            tdoas.append(tdoa)
    # print("tdoas: ",tdoas)
    # print("resp_coor",resp_coor)

        if all(tdoa<100000 and tdoa>-100000 for tdoa in tdoas):#tdoa threshold set to be length of the largest diagonal of this building

            try:
                D_complete = np.zeros((len(locs[:,0]),len(locs[:,0])))
                for resp_index in list(range(1,len(resp_coor[:,0])+1)): #resp_index with respect to input string of coors
                    D_complete[0,resp_index] = tdoas[resp_index-1]

                # print("d_complete: ",D_complete)

                tag_candidates = np.empty((2,0))
                cnt =0
                combos = [] #list of combos of different sizes
                combos = create_combos(resp_coor,combos)
                result = calc_combo(combos,locs,D_complete,init_coor,cnt,anchor_combo,tag_candidates,dop_current)
                dop_current = result[0]
                tag_candidates = result[1]
                print(tag_candidates)
                min_dop_idx = np.where(dop_current == np.amin(dop_current))[0][0]
                tagLoc = tag_candidates[:,min_dop_idx]
                print("tagLocsolver: ",tagLoc)
                return tagLoc
            except:
                return[]
        else:
            print("tdoa too large")
            return []
    else:
        print('not enough signal captured')
        return[]

# NSDI_read_TDoA_new("0,0;3600,0;3600,3100;0,3100@115;484;238")
# NSDI_read_TDoA_new("0,0;3600,0;3600,3100;0,3100;1500,1500;1000,1500@115;484;238;345;34")

