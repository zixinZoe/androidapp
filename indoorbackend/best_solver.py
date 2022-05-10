#select the best anchor combination and return only one tagLoc with best anchor combo
#select the best anchor combination and run 100 times with different Gaussian noise
#return 100 tagLocs with best anchor combos
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
        # combo_num = []
        for item in itertools.combinations(list(range(1,num_of_resp+1)),num):
            combo_num = np.append(combo_num,np.array([item]),axis=0)
            # combo_num.append(item)
        combos.append(combo_num)
    # print("combos: ",combos)
    # print("combosshape: ",np.array(combos).shape)
    return combos

def calc_combo(combos,locs,D_complete,estX,estY,cnt,anchor_combo,tag_candidates,dop_current,init_index,beacon_pos,r):
    for cur in range(0,len(combos)):
        if combos[cur].any():
            # print('combos[index]',combos[cur])
            for i in range(len(combos[cur])):
                # print('cur: ',cur)
                # print("i: ",i)
                # print('combos[cur][i]: ',combos[cur][i])
                idx = combos[cur][i][:]
                mask = np.zeros((len(locs[:,0]),len(locs[:,0])))
                for resp in idx:
                    mask[0,resp] = 1 
                DDoA = np.multiply(mask,D_complete)
                zero_coor = [[-1,-1]]
                for id in range(len(DDoA[init_index])):
                    if DDoA[init_index][id] == 0 and id != init_index:
                        zero_coor.append([init_index,id])
                estimation = [estX,estY]
                # estimation = [1000,1000]
                # print('init_coor: ',init_coor)
                print("DDoA: ",DDoA)
                
                tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,locs,zero_coor,beacon_pos,r]),axis =1)
                # print('tag_can2: ',tag_candidates)
                # print("before resplist")
                RESP_LIST = [0]
                for index in idx:
                   RESP_LIST = np.append(RESP_LIST,index)
                    # RESP_LIST.append(index)
                dop_current = np.append(dop_current,GDOP(locs[RESP_LIST,:],tag_candidates.T[cnt,:]))
                anchor_combo.append(RESP_LIST)
                # print("after resplist")
    return [dop_current,tag_candidates,np.array(anchor_combo)]

#input format: “x0,y0;x1,y1;x2,y2;x4,y4@TDoA01,TDoA02,TDoA04”
#“x0,y0;x1,y1;x2,y2;x4,y4@TDoA01,TDoA02,TDoA04@roomwidth*roomheight@seed_choice@dop@sigma@count” 
def NSDI_read_TDoA_new(line):
    if '@' in line:
        # anchor_combo = []
        # dop_current = []

        # tag_candidates = np.empty((2,0))

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
        # print("locs: ",locs)
        init_coor = locs[0,:]
        resp_coor = locs[1:,:]
        read_tdoas = parts[1].split(";")
        # print("read_tdoas: ",read_tdoas)
        # print("read_tdoas: ",read_tdoas)
        # tdoas = []

        # mu = 0
        # sigma = int(parts[5])
        # print('sigma: ',sigma)
        # for read_tdoa in read_tdoas:
        #     noise = np.random.normal(mu, sigma)
        #     tdoa = int(float(read_tdoa))+noise
        #     tdoas.append(tdoa)
        tdoas = []
        mu = 0
        sigma = float(parts[5])
        count = int(parts[6])
        print('sigma: ',sigma)
        if len(parts) == 9:
            beacon_pos = parts[7].split(",")
            # beacon_pos = float(beacon_pos)
            # print("beacon_pos: ",beacon_pos)
            r = float(parts[8])
        else:
            beacon_pos = ["",""]
            r=0
        # print("count: ",count)
        for read_tdoa in read_tdoas:
            # print("gethere")
            noise_tdoa = []
            for i in range(count):
                noise = np.random.normal(mu, sigma)
                tdoa = int(float(read_tdoa))
                # print("tdoa: ",tdoa)
                noise_tdoa.append(tdoa+noise)
                # print("noise_tdoa: ",noise_tdoa)
            tdoas.append(noise_tdoa)
            # print('tdoasshape: ',tdoas.shape)
        tdoas = np.transpose(np.array(tdoas) )#100*respnum
        # print("tdoasshape: ",tdoas.shape)
        # print("resp_coor",resp_coor)
        room = parts[2].split("*")
        width = int(room[0])
        height = int(room[1])

        estX = 0
        estY = 0
        seed_choice = parts[3]
        if seed_choice == "rmctr":
            estX = width//2
            estY = height//2
        else:
            est_coors = seed_choice.split(",")
            estX = int(est_coors[0])
            estY = int(est_coors[1])

        tag_candidates = []
        # print('typecandidat: ',type(tag_candidates))
        for row in tdoas:
            if all(tdoa<100000 and tdoa>-100000 for tdoa in row):#tdoa threshold set to be length of the largest diagonal of this building

                try:
                    # print("in try")
                    # print("row: ",row)
                    D_complete = np.zeros((len(locs[:,0]),len(locs[:,0])))
                    for resp_index in list(range(1,len(resp_coor[:,0])+1)): #resp_index with respect to input string of coors
                        D_complete[0,resp_index] = row[resp_index-1]

                    # print("d_complete: ",D_complete)

                    tag_cand = np.empty((2,0))
                    cnt =0
                    anchor_combo = []
                    dop_current = []
                    init_index = 0
                    combos = [] #list of combos of different sizes
                    print("before creating combos")
                    combos = create_combos(resp_coor,combos)
                    print("before calculating combos")
                    result = calc_combo(combos,locs,D_complete,estX,estY,cnt,anchor_combo,tag_cand,dop_current,init_index,beacon_pos,r)
                    # print("result: ",result)
                    dop_current = result[0]
                    tag_cand = result[1]
                    anchor_combo = result[2]
                    # print("combos: ",combos)
                    # print("dop_current: ",dop_current)
                    # print("tag_cand: ",tag_cand)
                    # print("anchor_combo: ",anchor_combo)
                    # with open('combos1', 'wb') as saveFile:
                    #     for i in range(len(combos)):
                    #         combos[i] = combos[i].tolist()
                    #     combos_data = np.array(combos).tobytes()
                    #     saveFile.write(combos_data)
                    # with open('dop_current1', 'wb') as saveFile:
                    #     dop_data = dop_current.tobytes()
                    #     saveFile.write(dop_data)
                    # with open('tag_cand1', 'wb') as saveFile:
                    #     tag_cand_data = tag_cand.tobytes()
                    #     saveFile.write(tag_cand_data)
                    # with open('anchor_combo1', 'w') as saveFile:
                    #     combos_list = []
                    #     for an_combo in anchor_combo:
                    #         # print("str(an_combo): ",str(an_combo))
                    #         combo_string = "".join(str(an_combo))
                    #         combos_list.append(combo_string)
                    #     stored_combo = ";".join(combos_list)
                    #     saveFile.write(stored_combo)
                    # print("tagcand: ", tag_cand)
                    min_dop_idx = np.where(dop_current == np.amin(dop_current))[0][0]
                    tagLoc = tag_cand[:,min_dop_idx]
                    best_combo = anchor_combo[min_dop_idx]
                    # with open("best_combos1","w") as saveFile:
                    #     best_combo = "".join(str(best_combo))
                    #     saveFile.write(best_combo)
                    # print("tagLocsolver: ",tagLoc)
                    tagLoc = np.reshape(np.array(tagLoc),((1,2)))
                    # serialized = json.dump(tagLoc)
                    # return tagLoc
                    # print('typecandidates: ',type(tag_candidates))
                    # print("tagloc: ",tagLoc[0].tolist())
                    tag_candidates.append(tagLoc[0].tolist())
                    # print("tag_candidates: ",tag_candidates)
                    # return tag_candidates
                except:
                    # return np.empty([1,1])
                    # print('typecan: ',type(tag_candidates))
                    tag_candidates.append([1])
            else:
                print("tdoa too large")
                # return np.empty([1,1])
                tag_candidates.append([1])
        # print('tag_candidates: ',tag_candidates)
        tag_candidates = np.array(tag_candidates)
        # print('shape: ',tag_candidates.shape)
        return tag_candidates
    else:
        print('not enough signal captured')
        return np.empty([1,1])

# NSDI_read_TDoA_new("0,0;3600,0;3600,3100;0,3100@115;484;238@800*800@0,0@best@100")
# NSDI_read_TDoA_new("0,0;3600,0;3600,3100;0,3100;1500,1500;1000,1500@115;484;238;345;34")

