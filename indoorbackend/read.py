import sys
import re

def NSDI_read_TDoA_new(line):
    
    # read_packet_id = []
    # read_ID1 = []
    # read_ID2 = []
    # read_DDoA = []
    # read_FP_PW_tag = []

    # init_packet_id = []
    # init_FP_PW = []
    
    
    read_packet_id = 0
    read_ID1 = 0
    read_ID2 = 0
    read_DDoA = 0
    read_FP_PW_tag = 0

    init_packet_id = 0
    init_FP_PW = 0 #first path receive power(indicator of transmission quality)
                    #other paths are reflections of signals
    # with open(file_path) as f:
        
    #     lines = f.readlines()
    #     for line in lines:
        #match = re.fullmatch('Pkt\s[0-9]+\s')
    arr = line.split("_")
    if arr[0] == "Pkt" and len(arr) == 14:
        # read_packet_id.append(float(arr[1]))
        # read_ID1.append(float(arr[3]))
        # read_ID2.append(float(arr[5][0:1]))
        # read_DDoA.append(float(arr[12]))
        # read_FP_PW_tag.append(float(arr[6][6:]))

        read_packet_id = float(arr[1])
        read_ID1 = float(arr[3])
        read_ID2 = float(arr[5][0:1])
        read_DDoA = float(arr[12])
        read_FP_PW_tag = float(arr[6][6:])
    elif arr[0] == "Pkt" and len(arr) == 4:
        # init_packet_id.append(float(arr[1][:-1]))
        # init_FP_PW.append(float(arr[2][6:]))

        init_packet_id = float(arr[1][:-1])
        init_FP_PW = float(arr[2][6:])
    return [read_packet_id,read_ID1,read_ID2,read_DDoA,read_FP_PW_tag, init_packet_id,init_FP_PW]
# file_path = "../../Desktop/Zixin project/nnnsdi_walk_3_17/teraterm.log"
# NSDI_read_TDoA_new(file_path)
