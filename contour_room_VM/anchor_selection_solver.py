from read import NSDI_read_TDoA_new
from tag_filter_power import tag_filter_power
import numpy as np
from operator import itemgetter
from scipy.spatial.distance import pdist
from ismember import ismember
import matplotlib.pyplot as plt

def getTag(line):

    cur_packet_id = 0
    cur_read_ID1 = []
    cur_read_ID2 = []
    cur_read_DDoA = []
    cur_read_FP_PW_tag = []

    cur_init_packet_id = []
    cur_init_FP_PW = []

    # changeID = 0 #keep track if packet id changes
    while true:
        [packet_id,ID1,ID2,TDoA,FP_PW_tag,init_power_packet_id,FP_PW_init] = NSDI_read_TDoA_new(line)
        if cur_packet_id == 0 or packet_id == cur_packet_id:
            cur_read_ID1.append(ID1)
            cur_read_ID2.append(ID2)
            cur_read_DDoA.append(TDoA)
            cur_read_FP_PW_tag.append(FP_PW_tag)
            cur_init_packet_id.append(init_power_packet_id)
            cur_init_FP_PW.append(FP_PW_init)
        else:
            anchorLoc_mm = np.array([[131756.727272727,	89523.4545454545],
                                    [132403.272727273,	67564.0000000000],
                                    # [108111.636363636,	73290.5454545455],
                                    # [124436.909090909,	96935.6363636364],      
                                    # [110259.090909091,	95965.8181818182],
                                    # [102269.636363636,	82319.0909090909],
                                    # [117994.545454545,	61283.2727272727],
                                    # [105871.818181818,	108111.636363636],
                                    # [96681.6363636364,	92178.9090909091],
                                    # [86244.5454545455,	73867.8181818182],
                                    [101692.363636364,	66016.9090909091],
                                    [130763.818181818,	59620.7272727273]])
            antenna_delays = [-514.800046735725,
                            -515.807752377787,
                            -515.311106592656, 
                            -515.115189872074,
                            -514.882780169421,
                            -513.592856014242,
                            -514.918087972098,
                            -515.128385013776,
                            -514.793541561308,
                            -515.321036364222,
                            -515.241712743109,
                            -514.973272610434,
                            -514.989929612259]

            #Filter by initiator power (>-105 dBm)
            a = range(0,len(FP_PW_init_mat))
            valid_index = [i for (i,j) in zip(a,FP_PW_init_mat) if j>-105]
            valid_packet_id = []
            for vindex in valid_index:
                valid_packet_id.append(init_power_packet_id_mat[vindex])

            #Filter TDoA(outliers)
            ab_TDoA_mat = map(abs,TDoA_mat)
            keep_idx = [i for (i,j) in zip(a,ab_TDoA_mat) if j<30000]

            f_packet_id_mat = []
            f_ID1_mat = []
            f_ID2_mat = []
            f_TDoA_mat = []
            f_FP_PW_tag_mat = []
            
            for kidx in keep_idx:
                f_packet_id_mat.append(packet_id_mat[kidx])
                f_ID1_mat.append(ID1_mat[kidx])
                f_ID2_mat.append(ID2_mat[kidx])
                f_TDoA_mat.append(TDoA_mat[kidx])
                f_FP_PW_tag_mat.append(FP_PW_tag_mat[kidx])

            #Solve tag
            d = (np.diff(f_packet_id_mat) != 0)
            d = np.append([True],d)
            d = np.append(d,[True])
            n = np.diff(np.nonzero(d))[0]

            current_idx = 0
            tagLoc = []
            dop = []
            anchor_selected = []
            candidate = []
            candidate_dop = []
            tag_candidates = []
            dop_all = []

            packet_seq = []
            anchor_combo = []

            for i in range(len(n)):
                current_idx = sum(n[0:i])
                if n[i] >= 2:
                    INIT_id = int(f_ID2_mat[current_idx])
                    RESP_id = f_ID1_mat[current_idx:current_idx+n[i]]
                    RESP_id = [int(id) for id in RESP_id]
                    print('RESP_id',RESP_id)
                    TDoA_in = f_TDoA_mat[current_idx:current_idx+n[i]]
                    FP_PW_in = f_FP_PW_tag_mat[current_idx:current_idx+n[i]]

                    [cur_tagLoc,cur_dop,cur_anchor_selected,cur_candidate,cur_candidate_dop,cur_tag_candidates,cur_dop_all] = tag_filter_power(RESP_id,INIT_id,TDoA_in,FP_PW_in,anchorLoc_mm,[],antenna_delays)
                    tagLoc.append(cur_tagLoc)
                    dop.append(cur_dop)
                    anchor_selected.append(cur_anchor_selected)
                    candidate.append(cur_candidate)
                    candidate_dop.append(cur_candidate_dop)
                    tag_candidates.append(cur_tag_candidates)
                    dop_all.append(cur_dop_all)

                    packet_seq.append(f_packet_id_mat[current_idx])
                    anchor_combo.append([INIT_id,RESP_id])

            #Filter by candidate relative location
            good_candidate = []
            tagLoc_candidate = []
            good_packet_id = []
            tagLoc_candidate2 = [];#tag location
            packet_id_candidate2 = []

            for i in range(len(candidate)):
                if len(tag_candidates[i]) == 1 and dop[i] < 1.1:
                    tagLoc_candidate2.append(tag_candidates[i])
                    packet_id_candidate2.append(packet_seq[i])
                #if there are more responders, compare the results
                elif(len(np.transpose(tag_candidates[i]))>1):
                    #find the 2 solutions iwth lowest DoP
                    # [sorted_dop_all,new_a] = sorted(zip(dop_all,a),key = lambda t: t[0])#//////////////
                    sorted_dop_all = sorted(dop_all[i])
                    new_a = np.argwhere(dop_all[i]<=sorted_dop_all[1])
                    temp = tag_candidates[i][:,new_a[0][0]]
                    temp = np.vstack([temp,tag_candidates[i][:,new_a[1][0]]])

                    #find distance between these solutions
                    d_vec = pdist(temp)

                    #check if the distance is smaller than 800mm and DoP is smaller than 1.4
                    if d_vec and d_vec<800 and min(dop_all[i])<1.4:
                        tagLoc_candidate2.append(np.mean(temp,axis = 0))
                        packet_id_candidate2.append(packet_seq[i])
            tagLoc_candidate2_filterPW = []
            for index in np.nonzero(ismember(packet_id_candidate2,valid_packet_id)[0])[0]:
                tagLoc_candidate2_filterPW.append(tagLoc_candidate2[int(index)])
                tagLoc_result = np.array(tagLoc_candidate2_filterPW)

            #plot locations
            #plt.scatter(anchorLoc_mm[:,0]*66/5/304.8,anchorLoc_mm[:,1]*66/5/304.8) #plot anchor locations
            #plt.scatter(tagLoc_result[:,0]*66/5/304.8,tagLoc_result[:,1]*66/5/304.8) #plot filtered tag locations
            #tagLoc2 = np.array(tagLoc_candidate2)
            #print('tagCandidates',np.transpose(tagCandidates))
            # plt.scatter(tagLoc2[:,0],tagLoc2[:,1]) #plot original tag locations

            plt.xlim([3430,6020])
            plt.ylim([2536,4826])
            plt.show()

            cur_packet_id = packet_id
            cur_read_ID1 = [ID1]
            cur_read_ID2 = [ID2]
            cur_read_DDoA = [TDoA]
            cur_read_FP_PW_tag = [FP_PW_init]
            cur_init_packet_id = [init_power_packet_id]
            cur_init_FP_PW = [FP_PW_init]