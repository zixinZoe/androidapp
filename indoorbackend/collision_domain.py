from cmath import inf
import random
from tokenize import group
import numpy as np
from scipy.fft import idst

threshold = 3
# anchors_xs = random.sample(range(0,50),30)
# anchors_ys = random.sample(range(0,50),30)
# anchors = np.array(list(zip(anchors_xs,anchors_ys)))

# cur_index = 0
# delete_index = []
# for anchor in anchors[:-1]:
#     min_dis = np.amin(np.sqrt((anchor[0]-anchors[(cur_index+1):,0])**2+(anchor[1]-anchors[(cur_index+1):,1])**2))
#     if min_dis < threshold:
#         delete_index.append(cur_index)
#     cur_index+=1
# anchors = np.delete(anchors,delete_index,axis=0)
# with open('sample_anchors1', 'wb') as saveFile:
#     sample_anchors = anchors.tobytes()
#     saveFile.write(sample_anchors)

with open('sample_anchors1', 'rb') as inFile:
    anchors = inFile.read()
    anchors = np.frombuffer(anchors,dtype=int)
anchors = np.reshape(anchors,(len(anchors)//2,2))
# print("anchors: ",anchors)

FI_num = len(anchors)//4
# FI_indexes = random.sample(range(0,len(anchors)-1),FI_num)
# FIs = anchors[FI_indexes]
# with open('FIs1', 'wb') as saveFile:
#     f_inis = FIs.tobytes()
#     saveFile.write(f_inis)
# print("FI: ",FIs)

with open('FIs1', 'rb') as inFile:
    f_inis = inFile.read()
    f_initiators = np.frombuffer(f_inis,dtype=int)
f_initiators = np.reshape(f_initiators,(len(f_initiators)//2,2))
# print("f_initiators: ",f_initiators)

#assign signal strength received by anchors from each FIs
Fh = 10.6
Fl = 3.1
Fb = 10.6-3.1
c = 299792458
pw_threshold = -240

# distance = []
# for FI in f_initiators:
#     cur_distances = []
#     for anchor in anchors:
#         if anchor not in f_initiators:
#             #print("cur_dis: ",np.sqrt((FI[0]-anchor[0])**2+(FI[1]-anchor[1])**2))
#             cur_distances.append(np.sqrt((FI[0]-anchor[0])**2+(FI[1]-anchor[1])**2))
#     distance.append(cur_distances)
# distance = np.array(distance)

# with open('distances1', 'wb') as saveFile:
#     dis = distance.tobytes()
#     saveFile.write(dis)

with open('distances1', 'rb') as inFile:
    dis = inFile.read()
    distance = np.frombuffer(dis)
distance = np.reshape(distance,(len(f_initiators),len(distance)//len(f_initiators)))

# fppw = []
# for fi_row in distance:
#     cur_pw = []
#     for d in fi_row:
#         pl = 20*np.log(4*np.pi*d*Fb/(c*np.log(Fh/Fl)))
#         if pl >= pw_threshold:
#             cur_pw.append(pl)
#         else:
#             cur_pw.append(-inf)
#     fppw.append(cur_pw)
# print("fppw: ",fppw)
# fppw = np.array(fppw)

# with open('fppw1', 'wb') as saveFile:
#     fppw1 = fppw.tobytes()
#     saveFile.write(fppw1)

with open('fppw1', 'rb') as inFile:
    fppw = inFile.read()
    fppw = np.frombuffer(fppw)
fppw = np.reshape(fppw,(len(f_initiators),len(fppw)//len(f_initiators)))
print("openedfppw: ",fppw)

# fppw = np.array([[-1,-2,-3,-inf],[-3,-4,-1,-4],[-inf,-inf,-inf,-inf]])

group_id = np.argmax(fppw,axis=0)#for each anchor(except for FIs)
groups = {}
for fi in range(FI_num):
    groups.update({fi:[]})
# groups=dict.fromkeys(tuple(range(FI_num)),[])
print("groupsinit: ",groups)
anchor_id = 0
print("groupid: ",group_id)
for id in group_id:
    print("id: ",id)
    # if id in groups.keys():
    print("groups[id]: ",groups[id])
    groups[id].append(anchor_id)
    print("groups: ",groups)
    # else:
    #     groups.update({id:np.array([anchor_id])})
    anchor_id+=1
# print("groups: ",groups)

group_fppw = np.where(fppw>pw_threshold,fppw,-inf)
# print("group_fppw: ",group_fppw)
gates = np.full((group_fppw.shape[0],group_fppw.shape[0]),-1)
# print('emptygates: ',gates)
for id in groups:
    for other_id in groups:
        if other_id != id:
            if len(groups[id]) != 0:
                # print("type: ",type(groups[id]))
                # print("type0: ",type(groups[0]))
                if np.max([group_fppw[other_id][gid] for gid in groups[id]])!=-inf:
                    gate_id = groups[id][np.argmax(group_fppw[other_id][groups[id]])]
                    gates[id][other_id] = gate_id
# print("gates: ",gates)

poll_time = 1
resp_time = 1
final_time = 1

neighbor_count = {}
print("gates: ",gates)
for fi in range(gates.shape[0]):
    print("fi: ",fi)
    print("gates[fi]: ",gates[fi])
    nei0 = np.where(gates[fi]>-1)[0]
    print("nei0: ",nei0)
    print("gates[:][fi]: ",gates[:,fi])
    nei1 = np.where(gates[:,fi]>-1)[0]
    print("nei1: ",nei1)
    neighbors = np.array(list(set(np.append(nei0,nei1))))
    neighbor_count.update({fi:neighbors})
print("neighbor_count: ",neighbor_count)

group_time = {}
for group_id in groups:
    time = poll_time+resp_time*len(groups[group_id])+final_time
    group_time.update({group_id:time})
print("group_time: ",group_time)

neighbor_num = {}
for fi in neighbor_count:
    neighbor_num.update({fi:len(neighbor_count[fi])})
print("neighbor_num: ",neighbor_num)
sorted_neighbor_num = {}
sorted_keys = sorted(neighbor_num, key=neighbor_num.get, reverse=True)  # [1, 3, 2]

for w in sorted_keys:
    sorted_neighbor_num[w] = neighbor_num[w]
print("sorted: ",sorted_neighbor_num)

group_record = []
time_count = 0
index = 0
cdr=0#count device round
while len(group_record)<len(groups):
    if list(sorted_neighbor_num.keys())[index] not in group_record:
        cur_lead = list(sorted_neighbor_num.keys())[index]
        # group_record.append(cur_lead)
        cur_groups = []
        for group in groups.keys():
            if group not in neighbor_count[cur_lead]:
                cur_groups.append(group)
                group_record.append(group)
        time_count+=max([group_time[group] for group in cur_groups])
        cdr+=sum([len(groups[group]) for group in cur_groups])
        index += 1
        print("cur_groups: ",cur_groups)
        print("group_record: ",group_record)
        print("groups: ",groups)
    else:
        index += 1
print("time: ",time_count)
print("cdr: ",cdr)
#calculate time cost for per device per round of communication
# pdpr=time_count/

