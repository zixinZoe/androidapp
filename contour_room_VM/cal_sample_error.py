from http.server import CGIHTTPRequestHandler, HTTPServer
import math
from socketserver import ThreadingMixIn
import statistics
from urllib.parse import urlparse
from urllib.parse import parse_qs
import urllib.request
import json
from numpy import random

from matplotlib.cbook import report_memory

from server import MyServer
import numpy as np
import requests

# class MyServer(CGIHTTPRequestHandler):
mu = 0
count = 100
floorWid = 20
floorLen = 40
anchorNum = 4
sample_distance = 1
loc_indexes = list(range(anchorNum))
locations = np.zeros((anchorNum,3))
seed = "0,0"
sigma = 0.1
r = 1
sample_distance = 1

SAVE_TDOA = 0
SAVE_ORIGINAL_ERROR_MATRIX = 0
SAVE_ORIGINAL_All_ERROR = 0
SAVE_NEW_ERROR_MATRIX = 1
READ_LARGE_SAMPLE_POS = 1
READ_BEACON_POS = 1
SAVE_NEW_All_ERROR = 1

locations = "0,0;10,20;20,0;40,20" # location1
with open('locations1', 'wb') as saveFile:
    loc_data = np.array(locations).tobytes()
    saveFile.write(loc_data)
# locations[:,0] = [0,0,40,40]
# locations[:,1] = [0,20,0,20]
# locations[:,0] = [0,20,40,20,0]
# locations[:,1] = [10,0,5,15,20]
locs = np.zeros((anchorNum,2))
read_locs = locations.split(";")
num = 0
respNum = len(read_locs)
for read_loc in read_locs: 
    coors = read_loc.split(",")
    x = int(coors[0])
    y = int(coors[1])
    locs[num][0] = x
    locs[num][1] = y
    num = num+1

roomX = floorLen
roomY = floorWid
tdoalist = []#for all samples
all_tdoa = []#for storage
xs = range(0,roomX+1,sample_distance)
xs = [ele for ele in xs for i in range(0,roomY+1,sample_distance)]
ys = range(0,roomY+1,sample_distance)
for x in range(0,roomX+1,sample_distance):
    for y in range(0,roomY+1,sample_distance):
        tdoas = ""#for each sample
        init_index = 0 #only one initiator
        resp_tdoa = []
        for respIdx in list(range(anchorNum))[1:]:#for each responder
            s1 = np.sqrt((locs[respIdx][0]-x)**2+(locs[respIdx][1]-y)**2)
            s2 = np.sqrt((locs[init_index][0]-x)**2+(locs[init_index][1]-y)**2)
            tdoa = s1-s2
            
            # cur_tdoa = []
            # noise = np.random.normal(mu, sigma,100)
            # for i in range(100):
            #     cur_tdoa.append(tdoa + noise[i])
            tdoas= tdoas+str(tdoa)+";"
            resp_tdoa.append(tdoa)
        tdoas = tdoas[:-1]
        # print("tdoas: ",tdoas)
        tdoalist.append(tdoas)
        all_tdoa.append(resp_tdoa)
        # print("tdoalist: ",tdoalist)

if SAVE_TDOA == 1:
    with open('tdoas1', 'wb') as saveFile:#save tdoas data here!(DONT DELETE)
        tdoa_data = np.array(all_tdoa).tobytes()
        saveFile.write(tdoa_data)

# anchors = ""
# for location in locations:
#     anchors = anchors+str(int(location[0]))+","+str(int(location[1]))+";"
# anchors = anchors[:-1]
anchors = locations
# print("anchors: ",anchors)
room = str(floorLen)+"*"+str(floorWid)
seed_choice = seed
dop = "all"

if READ_LARGE_SAMPLE_POS == 1:
    with open('sample_pos1', 'rb') as inFile:
        sample_pos = inFile.read()
        pos = np.frombuffer(sample_pos,dtype=int)
    pos = np.reshape(pos,(len(pos)//2,2))
if READ_BEACON_POS == 1:
    with open('beacons1', 'rb') as inFile:
        beacons = inFile.read()
        beacons = np.frombuffer(beacons,dtype=float)
    beacons = np.reshape(beacons,(len(beacons)//2,2))

index = 0
pos_count = 0
error_matrix = []
all_errors = []
for tdoa in tdoalist: #for each sample point
    # print("tdoa: ",tdoa)
    beacon_pos = ","
    if READ_LARGE_SAMPLE_POS == 1:
        if pos_count < pos.shape[0]:
            if index == pos[pos_count][0]*(roomY//sample_distance+1)+pos[pos_count][1]:
                beacon_pos = str(beacons[pos_count][0])+","+str(beacons[pos_count][1])
                pos_count+=1
    # line = anchors+"@"+tdoa+"@"+room+"@"+seed_choice+"@"+dop+"@"+str(sigma)+"@"+str(count)+";"
    line = anchors+"@"+tdoa+"@"+room+"@"+seed_choice+"@"+dop+"@"+str(sigma)+"@"+str(count)+"@"+beacon_pos+"@"+str(r)+";" 
    #“x0,y0;x1,y1;x2,y2;x4,y4@TDoA01,TDoA02,TDoA04@roomwidth*roomheight@seed_choice@dop@sigma@count” 
    curUrl = "http://localhost:8080/path"
    PARAMS = {"line":line}
    # print("params: ",line)
    tag_candidates = json.loads(requests.get(url = curUrl,params=PARAMS).text)
    # print("tag_candidates: ",tag_candidates)
    errors = []
    error = None
    for tag in tag_candidates:
        if tag != "":
            x = tag[0]
            y = tag[1]
            error = math.sqrt((x-xs[index])**2+(y-ys[(index+1) % len(ys)-1])**2)
            errors.append(error)
        else:
            errors.append(-1) #if no result, set error as -1
    median_error = statistics.median(errors)
    # print("median error: ",median_error)
    # print('errlimit: ',errlimit)
    # if median_error <=errlimit:
    error_matrix.append(median_error)
    all_errors.append(errors)
    index += 1
    # else:
    #     error_matrix.append(errlimit/1000)
    #     index = index +1
error_matrix = np.array(error_matrix).reshape((int((roomX+1)//sample_distance),int((roomY+1)//sample_distance)))
all_errors = np.array(all_errors).reshape((int((roomX+1)//sample_distance),int((roomY+1)//sample_distance),count))
# print("error_matrix: ",error_matrix)
#save error matrix to file
if SAVE_NEW_ERROR_MATRIX == 1:
    with open('new_error_matrix', 'wb') as saveFile:
        data = error_matrix.tobytes()
        saveFile.write(data)
#write error matrix from file
if SAVE_ORIGINAL_ERROR_MATRIX == 1:
    with open('error_matrix1', 'wb') as saveFile:
        data = error_matrix.tobytes()
        saveFile.write(data)
#write error matrix from file
if SAVE_ORIGINAL_All_ERROR == 1:
    with open('all_errors1', 'wb') as saveFile:
        data = all_errors.tobytes()
        saveFile.write(data)
#write error matrix from file
if SAVE_NEW_All_ERROR == 1:
    with open('new_all_errors', 'wb') as saveFile:
        data = all_errors.tobytes()
        saveFile.write(data)