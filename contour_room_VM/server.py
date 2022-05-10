# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import tag_solver 
from urllib.parse import urlparse
from urllib.parse import parse_qs
import re
import read
import threading
from socketserver import ThreadingMixIn
import serial
import sys
import numpy as np
import matplotlib.pyplot as plt
from tag_solver import tag_solver
from correction import antenna_correct_ddoa
import itertools

#hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    lineNum = 0
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

    anchor_locations = np.array([[0,0],
                            [3600,0],
                            [3600,3100],
                            [0, 3100]])
    
    def storeValues(arr):
        #print('reach')
        MyServer.read_packet_id.append(float(arr[1]))
        MyServer.read_respID.append(int(arr[3]))
        MyServer.read_initID.append(int(arr[5][0:1]))
        MyServer.read_DDoA.append(float(arr[12]))
        MyServer.read_FP_PW_tag.append(float(arr[6][6:]))

        print("self.read_packet_id: ",MyServer.read_packet_id)
        print("self.read_respID: ",MyServer.read_respID)
        print("self.read_initID: ",MyServer.read_initID)
        print("self.read_DDoA: ",MyServer.read_DDoA)
    
    def GDOP(anchor_locations, tag_location):

        relative_distances = anchor_locations - np.transpose(tag_location)
        distance_vec = np.array([np.sqrt(np.sum(np.power(relative_distances,2), axis=1))]).T
        H = relative_distances / distance_vec
        Q = np.linalg.inv(np.dot(np.transpose(H),H))
        dop = np.sqrt(np.trace(Q))
        return dop

    count = 0
    # tag_candidates = np.empty((2,0))

    def do_GET(self):
        try:
            # parsed_url = urlparse(self.path)

            def NSDI_read_TDoA_new():

                parsed_url = urlparse(self.path)
                if parse_qs(parsed_url.query)['line'] :
                    if parse_qs(parsed_url.query)['line'][0]:
                        if parse_qs(parsed_url.query)['line'][0] != '':
                            
                            line = parse_qs(parsed_url.query)['line'][0]#we got the line!!
                            print("line: ",line)
                            MyServer.lineNum = MyServer.lineNum+1
                            print("lineNum: ",MyServer.lineNum)
                            #now we start to calculate tag location~
                            line = line.replace('\x00','') #remove all the NUL characters
                            arr = line.split("@")

                            if arr[0] == "Pkt" and len(arr) == 14:
                                if int(arr[12]) < 100000 and int(arr[12]) > -100000: #filter lines by DDoA
                                    #print("line: ",line)
                                    if MyServer.count ==0:
                                        #print("reach self.count0")
                                        MyServer.storeValues(arr)
                                        MyServer.count = MyServer.count+1
                                        print("count: ",MyServer.count)
                                    else:
                                        # print("get here")
                                        # print("packetid: ",self.read_packet_id)
                                        # print("respid: ",self.read_respID)
                                        # print("initid: ",self.read_initID)
                                        # print("DDoA: ",self.read_DDoA)
                                        print("count: ",MyServer.count)
                                        if float(arr[1]) == MyServer.read_packet_id[MyServer.count-1]:
                                            print("samepacketid")
                                            MyServer.storeValues(arr)
                                            MyServer.count = MyServer.count+1
                                        else:#starts calculating after getting all the messages from one initiator
                                            D_complete = np.zeros((len(MyServer.anchor_locations),len(MyServer.anchor_locations)))
                                            current_count = 0
                                            for resp in MyServer.read_respID:
                                                D_complete[MyServer.read_initID,resp] = MyServer.read_DDoA[current_count]
                                                current_count = current_count+1
                                            print("D_complete: ",D_complete)
                                            combo2 = np.empty(shape=[0,2],dtype = np.int8)
                                            combo3 = np.empty(shape=[0,3],dtype = np.int8)

                                            for item in itertools.combinations(MyServer.read_respID,2):
                                                combo2 = np.append(combo2,np.array([item]),axis=0)
                                            for item in itertools.combinations(MyServer.read_respID,3):
                                                combo3 = np.append(combo3,np.array([item]),axis=0)
                                            
                                            #print("combo2: ",combo2)
                                            
                                            tag_candidates = np.empty((2,0))
                                            cnt =0
                                            if combo2.any():

                                                for i in range(len(combo2)):
                                                    idx = combo2[i][:]

                                                    mask = np.zeros((len(MyServer.anchor_locations),len(MyServer.anchor_locations)))
                                                    
                                                    for resp in idx:
                                                        mask[MyServer.read_initID,resp] = 1
                                                    DDoA = np.multiply(mask,D_complete)
                                                    print("DDOA: ",DDoA)
                                                    estimation = MyServer.anchor_locations[0][:]
                                                    tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,MyServer.anchor_locations]),axis =1)
                                                    print("tag_candidates: ",tag_candidates)
                                                    RESP_LIST = [MyServer.read_initID]
                                                    for index in idx:
                                                        RESP_LIST = np.append(RESP_LIST,index)
                                                    #print("RESP_LIST: ",RESP_LIST)
                                                    MyServer.dop_current = np.append(MyServer.dop_current,MyServer.GDOP(MyServer.anchor_locations[RESP_LIST,:],tag_candidates.T[cnt,:]))
                                                    MyServer.anchor_combo.append(RESP_LIST)
                                                    MyServer.count = MyServer.count+1
                                                    #print("end of 2")

                                            if combo3.any():
                                                for i in range(len(combo3)):
                                                    idx = combo3[i][:]
                                                    mask = np.zeros((len(MyServer.anchor_locations),len(MyServer.anchor_locations)))
                                                    for resp in idx:
                                                        mask[MyServer.read_initID,resp] = 1
                                                    DDoA = np.multiply(mask,D_complete)
                                                    print("DDoA3: ",DDoA)
                                                    estimation = MyServer.anchor_locations[0][:]+[1,1]
                                                    tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,MyServer.anchor_locations]),axis =1)
                                                    print("tag_candidate3: ",tag_candidates)
                                                    RESP_LIST = [MyServer.read_initID]
                                                    for index in idx:
                                                        RESP_LIST = np.append(RESP_LIST,index)
                                                    MyServer.dop_current = np.append(MyServer.dop_current,MyServer.GDOP(MyServer.anchor_locations[RESP_LIST,:],tag_candidates.T[cnt,:]))
                                                    MyServer.anchor_combo.append(RESP_LIST)
                                                    MyServer.count = MyServer.count+1
                                                    #print("end of 3")
                                                
                                            #print("dop_current: ",MyServer.dop_current)
                                            min_dop_idx = np.where(MyServer.dop_current == np.amin(MyServer.dop_current))[0][0]
                                            #print("min_dop_idx: ",min_dop_idx)
                                            tagLoc = tag_candidates[:,min_dop_idx]
                                            print("tagLoc: ",tagLoc)

                                            self.send_response(200)
                                            self.send_header("Content-type", "text/html")
                                            self.end_headers()
                                            self.wfile.write(bytes("["+str(int(tagLoc[0]))+","+str(int(tagLoc[1]))+"]", "utf-8"))

                                            #print("send over")
                                            MyServer.count = 0

                                            # Add x and y to lists
                                            MyServer.read_packet_id = []
                                            MyServer.read_respID = []
                                            MyServer.read_initID = []
                                            MyServer.read_DDoA = []
                                            MyServer.read_FP_PW_tag = []

                                            MyServer.init_packet_id = []
                                            MyServer.init_FP_PW = [] #first path receive power(indicator of transmission quality)
                                                            #other paths are reflections of signals
                                            MyServer.anchor_combo = []
                                            MyServer.dop_current = []

                                            MyServer.storeValues(arr)#catch the first line of each packet id
                                        #print("value restored")
                            # plt.scatter(tag_candidates[0][0],tag_candidates[1][0]) #plot original tag locations
                            # plt.xlim([-1000,5000])
                            # plt.ylim([-1000,5000])
                            # plt.draw()
                            # plt.pause(0.000001)
                            # plt.cla()
                            else:
                                print("no pkt14")
                else:
                    print('line does not exist')
            NSDI_read_TDoA_new()
        except:
            print('error occured')
            MyServer.count = 0
            # Add x and y to lists
            MyServer.read_packet_id = []
            MyServer.read_respID = []
            MyServer.read_initID = []
            MyServer.read_DDoA = []
            MyServer.read_FP_PW_tag = []

            MyServer.init_packet_id = []
            MyServer.init_FP_PW = [] #first path receive power(indicator of transmission quality)
                            #other paths are reflections of signals
            MyServer.anchor_combo = []
            MyServer.dop_current = []

    # def GDOP(anchor_locations, tag_location):

    #     relative_distances = anchor_locations - np.transpose(tag_location)
    #     distance_vec = np.array([np.sqrt(np.sum(np.power(relative_distances,2), axis=1))]).T
    #     H = relative_distances / distance_vec
    #     Q = np.linalg.inv(np.dot(np.transpose(H),H))
    #     dop = np.sqrt(np.trace(Q))
    #     return dop

            # NSDI_read_TDoA_new()



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == "__main__":        

    webServer = HTTPServer(('', serverPort), MyServer)
    print("Server started http://%s:%s" % ('', serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")