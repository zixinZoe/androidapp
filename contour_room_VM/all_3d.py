#run 100 times with different Gaussian noise added to tdoas & return 100 tagLocs
from operator import index
import numpy as np
from threed_tag_solver import tag_solver
import statistics

def calc_combo(locs,DDoA,estimation,init_index):           
    # zero_coor = [-1,-1]
    zero_coor = [[-1,-1]]
    for idx in range(len(DDoA[init_index])):
        if DDoA[init_index][idx] == 0 and idx != init_index:
            zero_coor.append([init_index,idx])
    tag_candidate  = tag_solver(estimation,[DDoA,locs,zero_coor])
    return tag_candidate

def read(locs,noisy_tdoa_list,seed,sampleNum,initNum):

    tag_candidates = []
    for sample in noisy_tdoa_list:#every sample point
        print('sample: ',sample)
        # for init_index in range(len(sample)):#each initiator
        init_index = 0
        D_complete = np.zeros((len(locs[:,0]),len(locs[:,0])))
        D_complete[init_index] = sample
        # print("D: ",D_complete)
        tag_candidate = np.transpose(calc_combo(locs,D_complete,seed,init_index))[0]
        tag_candidates.append(tag_candidate)
    tag_candidates = np.array(tag_candidates)
    tag_candidates = np.reshape(tag_candidates,((sampleNum,3)))
    return tag_candidates

