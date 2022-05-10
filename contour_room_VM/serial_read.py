import serial
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.animation as animation
from tag_solver import tag_solver
from correction import antenna_correct_ddoa
import time
import itertools

# ser = serial.Serial('/dev/cu.usbmodem14401',115200,timeout = 5)   
# for i in range(20):
# #ser.read_util()
#     read_serial=ser.readline()
#     #######  change from bytes to string #######
#     serial_string = str(read_serial,'UTF-8')
#     print('serial_string',serial_string)

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
                            # [124436.909090909,	96935.6363636364],      
                            # [110259.090909091,	95965.8181818182],
                            # [102269.636363636,	82319.0909090909],
                            # [117994.545454545,	61283.2727272727],
                            # [105871.818181818,	108111.636363636],
                            # [96681.6363636364,	92178.9090909091],
                            # [86244.5454545455,	73867.8181818182],
                            # [101692.363636364,	66016.9090909091],
                            

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
    antenna_delays = [-514.800046735725,
                    -515.807752377787,
                    -515.311106592656, 
                    -514.793541561308]
        #if len(arr) == 14:
            #print('something be stored', float(arr[1]))
        # elif len(arr) == 4:
        #     init_packet_id.append(float(arr[1][:-1]))
        #     init_FP_PW.append(float(arr[2][6:]))

#store values read
    def storeValues(arr):
        read_packet_id.append(float(arr[1]))
        #print('stored',read_packet_id)
        read_respID.append(int(arr[3]))
        read_initID.append(int(arr[5][0:1]))
        read_DDoA.append(float(arr[12]))
        read_FP_PW_tag.append(float(arr[6][6:]))

    ser = serial.Serial('/dev/cu.usbmodem14201',115200)   
    ser.timeout = 5.0
    count = 0 #line index
    tic = time.time()
    #for i in range(20):
    while (time.time() - tic) < ser.timeout:
        plt.scatter(anchor_locations[:,0],anchor_locations[:,1]) #plot anchor locations
        tag_candidates = np.empty((2,0))
        #read_serial = ser.read_until()

        read_serial=ser.readline()
        #######  change from bytes to string #######
        line = str(read_serial,'UTF-8')
        print('line: ',line)
        arr = line.split()
        #print('i',i)
        #print("arr[0]: ",arr[0])
        #print("length: ", len(arr))
        if arr[0] == "Pkt" and len(arr) == 14:
            if count ==0:
                storeValues(arr)
                #print('count',count)
                count = count+1
                #print('read_packet_id',read_packet_id)
            else:
                #print('count',count)
                if float(arr[1]) == read_packet_id[count-1]:
                    #print('initID',read_initID[0])
                    storeValues(arr)
                    #print('read_packet_id',read_packet_id)
                    count = count+1
                else:#starts calculating after getting all the messages from one initiator
                    D_complete = np.zeros((len(anchor_locations),len(anchor_locations)))
                    current_count = 0
                    for resp in read_respID:
                        D_complete[read_initID,resp] = read_DDoA[current_count]
                        current_count = current_count+1
                        
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
                                #print("mask: ", mask)
                            DDoA = np.multiply(mask,D_complete)

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
                                #mask[read_initID,read_respID[resp]] = 1
                                mask[read_initID,resp] = 1
                            DDoA = np.multiply(mask,D_complete)

                            estimation = anchor_locations[0][:]+[1,1]
                            tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)

                            RESP_LIST = [read_initID]
                            for index in idx:
                                #RESP_LIST = np.append(RESP_LIST,read_respID[index])
                                RESP_LIST = np.append(RESP_LIST,index)
                            dop_current = np.append(dop_current,GDOP(anchor_locations[RESP_LIST,:],tag_candidates.T[cnt,:]))
                            anchor_combo.append(RESP_LIST)
                            count = count+1

                    min_dop_idx = np.where(dop_current == np.amin(dop_current))[0][0]
                    tagLoc = tag_candidates[:,min_dop_idx]





                    # DDoA_all = np.zeros((len(anchor_locations),len(anchor_locations)))
                    # respID_int = [int(id) for id in read_respID]
                    # #print('respID_int',respID_int)
                    # #for index in range(len(read_respID)):
                    
                    # #print('read_DDoA',read_DDoA)
                    # print('initID',read_initID[0])
                    # print('respID',read_respID)
                    # DDoA_all[read_initID[0]][respID_int]=read_DDoA
                    # print('DDoA_all1',DDoA_all)

                    # for k in range(len(DDoA_all)):
                    #     for j in range(len(DDoA_all)):
                    #         if DDoA_all[k][j] != 0:
                    #             DDoA_all[k][j] = antenna_correct_ddoa(DDoA_all[k][j],k,j,antenna_delays)
                    # print('DDoA_all2',DDoA_all)

                    # mask = np.zeros((len(anchor_locations),len(anchor_locations)))
                    # for index in range(len(read_respID)):
                    #     mask[read_initID[0],read_respID[index]] = 1
                    # DDoA = np.multiply(mask,DDoA_all)

                    # estimation = anchor_locations[0][:]
                    # tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,anchor_locations]),axis =1)
                    # tag_candidates = np.transpose(tag_candidates)

                    count = 0
                    # print('tag_candidates: ',tag_candidates)

                    # Set up plot to call animate() function periodically
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
                    #plt.scatter(tag_candidates[:,0],tag_candidates[:,1]) #plot original tag locations
                    #NSDI_read_TDoA_new()
                    storeValues(arr)#catch the first line of each packet id

                    #print("tag_candiates: ",tag_candidates)
                    plt.scatter(tag_candidates[0][0],tag_candidates[1][0]) #plot original tag locations
                    # plt.cla()
                    plt.xlim([-1000,5000])
                    plt.ylim([-1000,5000])
                    plt.draw()
                    plt.pause(0.000001)
                    plt.cla()
                    #time.sleep(1)

def GDOP(anchor_locations, tag_location):

        relative_distances = anchor_locations - np.transpose(tag_location)
        distance_vec = np.array([np.sqrt(np.sum(np.power(relative_distances,2), axis=1))]).T
        H = relative_distances / distance_vec
        Q = np.linalg.inv(np.dot(np.transpose(H),H))
        dop = np.sqrt(np.trace(Q))
        return dop
#                     def animate(i,xs,ys):
#                         xs.append(tag_candidates[0][0])
#                         ys.append(tag_candidates[0][1])

#                         print('xs',xs)

#                         # Draw x and y lists
#                         plt.cla()
#                         plt.plot(xs,ys)

#                         # Format plot
#                         plt.title('Real-Time Location Tracker')
#                         plt.xlim([100000,150000])
#                         plt.ylim([70000,80000])
#         ani = animation.FuncAnimation(plt.gcf(), animate)
# # Set up plot to call animate() function periodically
# ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys))
# plt.show()

#print('result', read_packet_id)
#return [read_packet_id,read_ID1,read_ID2,read_DDoA,read_FP_PW_tag, init_packet_id,init_FP_PW]

NSDI_read_TDoA_new()
