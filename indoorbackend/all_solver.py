#run 100 times with different Gaussian noise added to tdoas & return 100 tagLocs
import numpy as np
from tag_solver import tag_solver
import statistics

def calc_combo(locs,D_complete,estX,estY,init_index,beacon_pos,r):           
    DDoA = D_complete
    estimation = [estX,estY]
    # estimation = [0,0]
    # estimation = [width//2,height//2]
    # zero_coor = [-1,-1]
    zero_coor = [[-1,-1]]
    for id in range(len(DDoA[init_index])):
        if DDoA[init_index][id] == 0 and id != init_index:
            zero_coor.append([init_index,id])
    # print('estimation: ',estimation)
    # print("before tag_solver")
    tag_candidate  = tag_solver(estimation,[DDoA,locs,zero_coor,beacon_pos,r])
    # print('tag_can2: ',tag_candidate)
    return tag_candidate

def NSDI_read_TDoA_new(line):
#“x0,y0;x1,y1;x2,y2;x4,y4@TDoA01,TDoA02,TDoA04@roomwidth*roomheight@seed_choice@dop@sigma@beacon_pos@r” 
    print("allsolverline: ",line)
    parts = line.split("@")
    # print('parts: ',parts)
    read_locs = parts[0].split(";")
    locs = np.zeros((len(read_locs),2))
    # width = 0
    # height = 0
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
    room = parts[2].split("*")
    width = int(room[0])
    height = int(room[1])
    # print("width: ",width)
    estX = 0
    estY = 0
    seed_choice = parts[3]
    if seed_choice == "rmctr":
        estX = width//2
        # print('estX: ',estX)
        estY = height//2
        # print('estY: ',estY)
    else:
        est_coors = seed_choice.split(",")
        estX = int(est_coors[0])
        estY = int(est_coors[1])
    # print("estX: ",estX)
    tdoas = []
    mu = 0
    sigma = float(parts[5])
    count = int(parts[6])
    # print("count: ",count)
    # print("parts[7]: ",parts[7])
    # print("parts[7].split: ",parts[7].split(",")) 
    if len(parts) == 9:
        beacon_pos = parts[7].split(",")
        # beacon_pos = float(beacon_pos)
        # print("beacon_pos: ",beacon_pos)
        r = float(parts[8])
    else:
        beacon_pos = ["",""]
        r=0
    # print('sigma: ',sigma)
    for read_tdoa in read_tdoas:
        noise_tdoa = []
        for i in range(count):
            # noise = np.random.normal(mu, sigma,count)
            noise = np.random.normal(mu,sigma)
            tdoa = int(float(read_tdoa))
            # noise_tdoa.append(tdoa+noise[i])
            noise_tdoa.append(tdoa+noise)
            # noise_tdoa.append(tdoa)
        tdoas.append(noise_tdoa)
    tdoas = np.transpose(np.array(tdoas) )#100*respnum
    # print('tdoas: ',tdoas)
    tag_candidates = []
    for row in tdoas:
        if all(tdoa<100000 and tdoa>-100000 for tdoa in row):
        #     try:
            D_complete = np.zeros((len(locs[:,0]),len(locs[:,0])))
            for resp_index in list(range(1,len(resp_coor[:,0])+1)): #resp_index with respect to input string of coors
                D_complete[0,resp_index] = row[resp_index-1]
            # print("D_complete: ",D_complete)
            init_index = 0
            tag_candidate = np.transpose(calc_combo(locs,D_complete,estX,estY,init_index,beacon_pos,r))[0]
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
                # saveFile.write(tag_cand_data)
            # with open('resp_list1', 'wb') as saveFile:
            #     resp_data = anchor_combo.tobytes()
            #     saveFile.write(resp_data)
            # print("tag: ",tag_candidate)
        tag_candidates.append(tag_candidate)
    tag_candidates = np.array(tag_candidates)
    return tag_candidates
        #     except:
        #         return[]
        # else:
        #     print("tdoa too large")
        #     return []


# NSDI_read_TDoA_new("0,0;3600,0;3600,3100;0,3100@115;484;238")
# NSDI_read_TDoA_new("0,0;3600,0;3600,3100;0,3100;1500,1500;1000,1500@115;484;238;345;34")

