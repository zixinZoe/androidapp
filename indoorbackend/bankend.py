import serial
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from tag_solver import tag_solver
from correction import antenna_correct_ddoa
import time
import itertools

def NSDI_read_TDoA_new():
    read_packet_id = []
    read_respID = []
    read_initID = []
    read_DDoA = []
    read_FP_PW_tag = []

    init_packet_id = []
    init_FP_PW = [] #first path receive power(indicator of transmission quality)
                    #other paths are reflections of signals

    anchor_combo = []
    dop_current = []

    xs = []
    ys = []

    anchor_locations = np.array([[0,0],
                            [3600,0],
                            [3600,3100],
                            [0, 3100]])

    antenna_delays = [-514.800046735725,
                    -515.807752377787,
                    -515.311106592656, 
                    -514.793541561308]

#store values read
    def storeValues(arr):
        read_packet_id.append(float(arr[1]))
        read_respID.append(int(arr[3]))
        read_initID.append(int(arr[5][0:1]))
        read_DDoA.append(float(arr[12]))
        read_FP_PW_tag.append(float(arr[6][6:]))

        print("packetid: ",read_packet_id)
        print("respid: ",read_respID)
        print("initid: ",read_initID)
        print("ddoa: ",read_DDoA)

    ser = serial.Serial('/dev/cu.usbmodem14301',115200)   
    ser.timeout = 5.0
    count = 0 #line index
    tic = time.time()
    while (time.time() - tic) < ser.timeout:
        plt.scatter(anchor_locations[:,0],anchor_locations[:,1]) #plot anchor locations
        tag_candidates = np.empty((2,0))

        read_serial=ser.readline()
        #######  change from bytes to string #######
        line = str(read_serial,'UTF-8')
        arr = line.split()

        if arr[0] == "Pkt" and len(arr) == 14:
            print('line: ',line)
            if count ==0:
                storeValues(arr)
                count = count+1
            else:
                if float(arr[1]) == read_packet_id[count-1]:
                    storeValues(arr)
                    count = count+1
                else:#starts calculating after getting all the messages from one initiator
                    D_complete = np.zeros((len(anchor_locations),len(anchor_locations)))
                    current_count = 0
                    for resp in read_respID:
                        D_complete[read_initID,resp] = read_DDoA[current_count]
                        current_count = current_count+1
                    print("dcomplete: ",D_complete)
                    combo2 = np.empty(shape=[0,2],dtype = np.int8)
                    combo3 = np.empty(shape=[0,3],dtype = np.int8)

                    for item in itertools.combinations(read_respID,2):
                        combo2 = np.append(combo2,np.array([item]),axis=0)
                    for item in itertools.combinations(read_respID,3):
                        combo3 = np.append(combo3,np.array([item]),axis=0)

                    tag_candidates = np.empty((2,0))
                    cnt =0
                    if combo2.any():

                        for i in range(len(combo2)):
                            idx = combo2[i][:]

                            mask = np.zeros((len(anchor_locations),len(anchor_locations)))
                            
                            for resp in idx:
                                mask[read_initID,resp] = 1
                            DDoA = np.multiply(mask,D_complete)
                            print("DDoA: ",DDoA)
                            estimation = anchor_locations[0][:]
                            tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)

                            RESP_LIST = [read_initID]
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
                                mask[read_initID,resp] = 1
                            DDoA = np.multiply(mask,D_complete)
                            print("DDoA3: ",DDoA)
                            estimation = anchor_locations[0][:]+[1,1]
                            tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)

                            RESP_LIST = [read_initID]
                            for index in idx:
                                RESP_LIST = np.append(RESP_LIST,index)
                            dop_current = np.append(dop_current,GDOP(anchor_locations[RESP_LIST,:],tag_candidates.T[cnt,:]))
                            anchor_combo.append(RESP_LIST)
                            count = count+1

                    min_dop_idx = np.where(dop_current == np.amin(dop_current))[0][0]
                    tagLoc = tag_candidates[:,min_dop_idx]

                    count = 0

                    # Add x and y to lists
                    tic = time.time()
                    read_packet_id = []
                    read_respID = []
                    read_initID = []
                    read_DDoA = []
                    read_FP_PW_tag = []

                    init_packet_id = []
                    init_FP_PW = [] #first path receive power(indicator of transmission quality)
                                    #other paths are reflections of signals
                    anchor_combo = []
                    dop_current = []

                    storeValues(arr)#catch the first line of each packet id
                    print(tagLoc)
                    #plt.scatter(tag_candidates[0][0],tag_candidates[1][0]) #plot original tag locations
                    #plt.scatter(tagLoc[0],tagLoc[1])
                    plt.xlim([-1000,5000])
                    plt.ylim([-1000,5000])
                    plt.draw()
                    plt.pause(0.000001)
                    plt.cla()

def GDOP(anchor_locations, tag_location):

        relative_distances = anchor_locations - np.transpose(tag_location)
        distance_vec = np.array([np.sqrt(np.sum(np.power(relative_distances,2), axis=1))]).T
        H = relative_distances / distance_vec
        Q = np.linalg.inv(np.dot(np.transpose(H),H))
        dop = np.sqrt(np.trace(Q))
        return dop

NSDI_read_TDoA_new()
