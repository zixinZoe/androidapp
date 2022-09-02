import re
import statistics
import sys
import numpy as np
import matplotlib.pyplot as plt
# from tag_solver import tag_solver
from threed_tag_solver import tag_solver#changed
from correction import antenna_correct_ddoa
import itertools
import serial
import math
import time
import json

class generic_solver:
    def __init__(self):
        self.tags=np.empty([0,3],dtype=float)#changed
        self.tags2=np.empty([0,3],dtype=float)#changed
        self.tags3=np.empty([0,3],dtype=float)#changed
        self.all_tdoas=np.empty([0,1],dtype=float)#for tdoa checking
        # self.used_tdoas=np.empty([0,1],dtype=float)#for tdoa checking

    def GDOP(self,anchor_locations, tag_location):
        relative_distances = anchor_locations - np.transpose(tag_location)
        distance_vec = np.array([np.sqrt(np.sum(np.power(relative_distances,2), axis=1))]).T
        H = relative_distances / distance_vec
        Q = np.linalg.inv(np.dot(np.transpose(H),H))
        dop = np.sqrt(np.trace(Q))
        return dop

    def create_combos(self,resp_coor,combos):
        num_of_resp = len(resp_coor[:,0])
        # print("num_of_resp: ",num_of_resp)
        for num in range(3,num_of_resp+1):#changed
            # combo_num = np.empty(shape=[0,num],dtype = np.int8)
            combo_num=[]
            for item in itertools.combinations(list(range(1,num_of_resp+1)),num):
                # combo_num = np.append(combo_num,np.array([item]),axis=0)
                # print("type: ",type(item))
                # print("item: ",item)
                combos.append(list(item))
            # combos.append(combo_num)
        # print('combos: ',combos)
        return combos

    def calc_combo(self,combos,locs,D_complete,init_coor,cnt,anchor_combo,tag_candidates,dop_current):
        for cur in range(len(combos)):
            if combos[cur]:
                # for i in range(len(combos[cur])):
                idx = combos[cur][:]
                # print("idx: ",idx)
                zero_coor = [[-1,-1]]
                mask = np.zeros((len(locs[:,0]),len(locs[:,0])))
                            
                for resp in idx:
                    # print("resp: ",resp)
                    mask[0,resp] = 1
                    if D_complete[0,resp] == 0:
                        zero_coor = [0,resp]
                # print("mask: ",mask) 
                DDoA = np.multiply(mask,D_complete)
                # print("ddoa: ",DDoA)
                estimation = init_coor
                # estimation = [1000,1000]
                # print('init_coor: ',init_coor)
                tag_candidates = np.append(tag_candidates, tag_solver(estimation,[DDoA,locs,zero_coor,["",""]]),axis =1)
                # print('tag_can2: ',tag_candidates)
                RESP_LIST = [0]
                for index in idx:
                    RESP_LIST = np.append(RESP_LIST,index)
                dop_current = np.append(dop_current,self.GDOP(locs[RESP_LIST,:],tag_candidates.T[cnt,:]))
                anchor_combo.append(RESP_LIST)
        return [dop_current,tag_candidates]

    #input format: “x0,y0;x1,y1;x2,y2;x4,y4@TDoA01,TDoA02,TDoA04”
    def NSDI_read_TDoA_new(self,line):
        print("line: ",line)
        if '@' in line:
            anchor_combo = []
            dop_current = []

            # tag_candidates = np.empty((2,0))

            parts = line.split("@")
            # print('parts0: ',parts[0])
            read_locs = parts[0].split(";")
            locs = np.zeros((len(read_locs),3))#changed
            num = 0
            for read_loc in read_locs: 
                coors = read_loc.split(",")
                x = int(coors[0])
                y = int(coors[1])
                z = int(coors[2])
                locs[num][0] = x
                locs[num][1] = y
                locs[num][2] = z #changed
                num = num+1

            init_coor = locs[0,:]
            resp_coor = locs[1:,:]
            read_tdoas = parts[1].split(";")
            # print("read_tdoas: ",read_tdoas)
            tdoas = []

            i=1
            for read_tdoa in read_tdoas:
                anchor_diff=math.sqrt((locs[i][0]-locs[0][0])**2+(locs[i][1]-locs[0][1])**2+(locs[i][2]-locs[0][2])**2)
                tdoa = int(float(read_tdoa))
                if tdoa<=anchor_diff:
                    tdoas.append(tdoa)
                else:
                    tdoa=math.inf
                    tdoas.append(math.inf)
                self.all_tdoas=np.append(self.all_tdoas,[[tdoa]],axis=0)#collect every tdoa for testing
                i+=1
        # print("resp_coor",resp_coor)

            # if len(parts)>2:
            #     flr=parts[2]

            if all(tdoa<100000000000 and tdoa>-100000000000 for tdoa in tdoas):#tdoa threshold set to be length of the largest diagonal of this building

                try:
                    D_complete = np.zeros((len(locs[:,0]),len(locs[:,0])))
                    for resp_index in list(range(1,len(resp_coor[:,0])+1)): #resp_index with respect to input string of coors
                        D_complete[0,resp_index] = tdoas[resp_index-1]

                    # print("d_complete: ",D_complete)
                    # self.used_tdoas.append(tdoas)

                    tag_candidates = np.empty((3,0))#changed
                    cnt =0
                    combos = [] #list of combos of different sizes
                    combos = self.create_combos(resp_coor,combos)
                    result = self.calc_combo(combos,locs,D_complete,init_coor,cnt,anchor_combo,tag_candidates,dop_current)
                    dop_current = result[0]
                    tag_candidates = result[1]
                    # print('result: ',tag_candidates)
                    min_dop_idx = np.where(dop_current == np.amin(dop_current))[0][0]
                    tagLoc = tag_candidates[:,min_dop_idx]
                    # print("tagLocsolver: ",tagLoc)
                    # print("typetagLoc: ",type(tagLoc))
                    # tags.append(tagLoc)
                    # print('locs[0][2]: ',locs[0][2])
                    tagLoc=np.array([tagLoc.tolist()])
                    self.tags = np.append(self.tags, tagLoc, axis=0)
                    if locs[0][2]==4500:
                        self.tags3 = np.append(self.tags3, tagLoc, axis=0)
                    else:
                        self.tags2 = np.append(self.tags2, tagLoc, axis=0)
                    # print('locs[0][2]: ',locs[0][2])
                    # print("new_tags2: ",self.tags2)
                    # print("tagLoc: ",tagLoc)

                    # with open('tag2d_1', 'rb') as inFile:
                    #     f_inis = inFile.read()
                    #     f_initiators = np.frombuffer(f_inis,dtype=int)
                    # f_initiators = np.reshape(f_initiators,(len(f_initiators)//2,2))
                    # print("f_initiators: ",f_initiators)
                    return tagLoc
                except:
                    return[]
            else:
                print("tdoa too large")
                return []
        else:
            print('not enough signal captured')
            return[]

    def plot_tdoas(self):
        #read from text file
        with open('scattercenter.txt', 'r') as f:
            a = json.loads(f.read())
        for line in a:
            print(line)
        with open('all_tdoa1minfiltertdoacenter', 'rb') as inFile:
            tdoas = inFile.read()
            all_t = np.frombuffer(tdoas,dtype=float)
        # print("tdoas: ",all_t)
        sorted_tdoas=sorted(all_t)
        cumu_tdoas=np.arange(1,len(all_t)+1)/len(all_t)
        print("amount: ",len(all_t))
        print('sorted_tdoas: ',sorted_tdoas)
        count=0
        for t in sorted_tdoas:
            if -10000<=t<=10000:
                count+=1
        print('10mtdoapercentage: ',count/len(sorted_tdoas))
        # interp_y=np.interp(2.4,sorted_errors,percents)
        # interp_y0=np.interp(0.9,sorted_errors,percents)
        plt.plot(sorted_tdoas,cumu_tdoas,marker='.',color='green',label='tdoas')
        plt.xlabel("tdoas(mm)")
        plt.ylabel('cdf')
        plt.title("tdoa cdf with filtering")
        # plt.vlines(x=10,color='blue',ymin=0,ymax=1)
        plt.legend()
        plt.show()


    #plots track
    def scatterplot(self):
        # anchor_xs=[0,3360,3360,0]
        # anchor_ys=[0,0,3800,3800]
        anchor_xs=[0,3200,3200,0]
        anchor_ys=[0,0,3500,3500]
        gt_x,gt_y=1600,1750#center
        # gt_x,gt_y=0,1750

        # with open('scattersame30center.txt', 'r') as f:
        #     a = json.loads(f.read())
        # for line in a:
        #     print(line)
        with open('tagsame30mincenter', 'rb') as inFile:
            coors = inFile.read()
            tag_coors = np.frombuffer(coors,dtype=float)
        tag_coors = np.reshape(tag_coors,(len(tag_coors)//3,3))#changed
        print("tag_coors: ",tag_coors)
        with open('tag2diff1mincenter', 'rb') as inFile:
            coors = inFile.read()
            tag_coors2 = np.frombuffer(coors,dtype=float)
        tag_coors2 = np.reshape(tag_coors2,(len(tag_coors2)//3,3))#changed
        print("tag_coors: ",tag_coors)
        with open('tag3diff1mincenter', 'rb') as inFile:
            coors = inFile.read()
            tag_coors3 = np.frombuffer(coors,dtype=float)
        tag_coors3 = np.reshape(tag_coors3,(len(tag_coors3)//3,3))#changed
        # print("tag_coors: ",tag_coors)

        errors=[]
        for x,y,z in tag_coors:
            err=math.sqrt((x-gt_x)**2+(y-gt_y)**2)
            # if err<=5000:
            errors.append(err)

        good_tags=np.empty([0,3])#changed
        good_cnt=0
        for tc in tag_coors2:
            if tc[0]>=0 and tc[0]<=3200 and tc[1]>=0 and tc[1]<=3500:
            # if tc[0]>=-84000 and tc[0]<=116000 and tc[1]>=-82500 and tc[1]<=117500:
                good_tags=np.append(good_tags,np.array([tc]),axis=0)
                good_cnt+=1

#alldots
        # xs=tag_coors2[:,0]
        # ys=tag_coors2[:,1]

        xs=good_tags[:,0]
        ys=good_tags[:,1]
        print('good_cnt: ',good_cnt)
        print("all_cnt: ",len(tag_coors2))
        print("std second floor x: ",statistics.stdev(tag_coors2[:,0]))
        print("std second floor y: ",statistics.stdev(tag_coors2[:,1]))
        print("std third floor x: ",statistics.stdev(tag_coors3[:,0]))
        print("std third floor y: ",statistics.stdev(tag_coors3[:,1]))

#show calculated positions
        plt.scatter(anchor_xs,anchor_ys,color="purple",label="anchors")
        plt.scatter(gt_x,gt_y,color='red',label='ground truth')
        plt.scatter(xs,ys,c='blue')
        plt.title("2nd floor result center 10min scatter 3D solver(mm)")
        plt.legend()
        # plt.savefig("3D solver diff floor 10min",format='png',dpi=150)
        plt.show()

    #plots track
    def plots(self):
        # anchor_xs=[0,3360,3360,0]
        # anchor_ys=[0,0,3800,3800]
        anchor_xs=[0,3200,3200,0]
        anchor_ys=[0,0,3500,3500]
        gt_x,gt_y=1600,1750
#error plot for different floor
        with open('scattercenter.txt', 'r') as f:
            a = json.loads(f.read())
        for line in a:
            print(line)
        # with open('tagdiff1mincenter', 'rb') as inFile:
        #     coors = inFile.read()
        #     tag_coors = np.frombuffer(coors,dtype=float)
        # tag_coors = np.reshape(tag_coors,(len(tag_coors)//3,3))#changed
        # print("tag_coors: ",tag_coors)
        with open('tag2diff1mincenter', 'rb') as inFile:
            coors = inFile.read()
            tag_coors2 = np.frombuffer(coors,dtype=float)
        tag_coors2 = np.reshape(tag_coors2,(len(tag_coors2)//3,3))#changed
        print("tag_coors2: ",tag_coors2)
        # with open('tag3diff1mincenter', 'rb') as inFile:
        #     coors = inFile.read()
        #     tag_coors3 = np.frombuffer(coors,dtype=float)
        # tag_coors3 = np.reshape(tag_coors3,(len(tag_coors3)//3,3))#changed
        # print("tag_coors3: ",tag_coors3)


        # print('size: ',np.size(tag_coors2[:,0]))
        # print("std second floor x: ",statistics.stdev(tag_coors2[:,0]))
        # print("std second floor y: ",statistics.stdev(tag_coors2[:,1]))
        # print("std third floor x: ",statistics.stdev(tag_coors3[:,0]))
        # print("std third floor y: ",statistics.stdev(tag_coors3[:,1]))       
        
        # errors=[]
        # for x,y,z in tag_coors3:
        #     err=math.sqrt((x-gt_x)**2+(y-gt_y)**2)
        #     # if err2<=100000:
        #     errors.append(abs(err))
        # print('errors: ',errors)
        errors2=[]
        for x,y,z in tag_coors2:
            err2=math.sqrt((x-gt_x)**2+(y-gt_y)**2)
            # if err2<=100000:
            errors2.append(abs(err2))

        # errors3=[]
        # for x,y,z in tag_coors3:
        #     err3=math.sqrt((x-gt_x)**2+(y-gt_y)**2)
        #     # if err3<=100000:
        #     errors3.append(abs(err3))

        good_tags=np.empty([0,3])#changed
        good_cnt=0
        for tc in tag_coors2:
            if tc[0]>=0 and tc[0]<=3200 and tc[1]>=0 and tc[1]<=3500:
                good_tags=np.append(good_tags,np.array([tc]),axis=0)
                good_cnt+=1

        xs=good_tags[:,0]
        ys=good_tags[:,1]

        sorted_x_err=np.sort([x3/1000 for x3 in errors2])
        percents=np.arange(1,len(sorted_x_err)+1)/len(sorted_x_err)
        # interp_y=np.interp(10,sorted_x_err,percents)
        # interp_y0=np.interp(20,sorted_x_err,percents)
        plt.plot(sorted_x_err,percents,marker='.',color='red',label="different floor")
        plt.xlabel("absolute localization result error same floor(m)")
        plt.ylabel('cumulative error percentile')
        # plt.vlines(x=16,color='green',ymin=0,ymax=1)
        plt.xlim(0,1)
        plt.ylim(0,1)
        # plt.vlines(x=100,color='blue',ymin=0,ymax=1)
        # plt.vlines(x=0.9,color='blue',ymin=0,ymax=1)
        # plt.title("Error Percentile Graph for 10s 2&3floor Data Collection(5m Error)")
        # plt.text(70, 0.65, "60% within 100m error", bbox=dict(facecolor='red', alpha=0.5))
        # plt.text(20, 0.37, "37% within 20m", bbox=dict(facecolor='red', alpha=0.5))
        # plt.text(10, 0, "0.5% within 10m", bbox=dict(facecolor='red', alpha=0.5))
        plt.title("absolute localization error percentile graph")
        # print("interp_ydiff: ",interp_y)
        # print('interp_y0.9diff: ',interp_y0)
        # # label=str(int(interp_y*100))+'percent of results lie in 0.5m Euclidean distance.'
        # print('good_cnt: ',good_cnt)
        # print("all_cnt: ",len(tag_coors))

#error plot for same floor
        # with open('tag3d_3&2atr10s', 'rb') as inFile:
        #     coors = inFile.read()
        #     tag_coors = np.frombuffer(coors,dtype=float)
        # tag_coors = np.reshape(tag_coors,(len(tag_coors)//3,3))#changed
        # # print("tag_coors: ",tag_coors)
        # errors=[]
        # for x,y,z in tag_coors:
        #     err=math.sqrt((x-gt_x)**2+(y-gt_y)**2)
        #     if err<=5000:
        #         errors.append(err)

        # good_tags=np.empty([0,3])#changed
        # good_cnt=0
        # for tc in tag_coors:
        #     if tc[0]>=0 and tc[0]<=3200 and tc[1]>=0 and tc[1]<=3500:
        #         good_tags=np.append(good_tags,np.array([tc]),axis=0)
        #         good_cnt+=1
        # sorted_errors=np.sort([err/1000 for err in errors])
        # percents=np.arange(1,len(sorted_errors)+1)/len(sorted_errors)
        # interp_y=np.interp(2.4,sorted_errors,percents)
        # interp_y0=np.interp(0.9,sorted_errors,percents)
        # plt.plot(sorted_errors,percents,marker='.',color='green',label='same floor')
        # # plt.vlines(x=1000,color='red',ymin=0,ymax=1)
        # # plt.vlines(x=2,color='red',ymin=0,ymax=1)
        # # plt.xlim(0,5)
        # print('interp_y2.4same: ',interp_y)
        # print('interp_y0.9same: ',interp_y0)
        # plt.text(2.4, 0.98, "97.7% within 2.4m", bbox=dict(facecolor='green', alpha=0.5))
        # plt.text(0.9, 0.969, "96.9% within 0.9m", bbox=dict(facecolor='green', alpha=0.5))

        #tennis table
        # path1_xs=[0,3360]
        # path1_ys=[0,0]
        # path2_xs=[3360,0]
        # path2_ys=[0,3800]
        # path3_xs=[0,3360]
        # path3_ys=[3800,3800]

        #atrium
        path1_xs=[0,3200]
        path1_ys=[0,0]
        path2_xs=[3200,0]
        path2_ys=[0,3500]
        path3_xs=[0,3200]
        path3_ys=[3500,3500]

        # plt.plot(path1_xs,path1_ys,color="red",label="ground truth")
        # plt.plot(path2_xs,path2_ys,color="red")
        # plt.plot(path3_xs,path3_ys,color="red")

#show calculated positions
        # plt.scatter(anchor_xs,anchor_ys,color="purple",label="anchors")
        # plt.scatter(gt_x,gt_y,color='red',label='ground truth')
        # plt.scatter(xs,ys,c='blue')
        # plt.title("3D solver same floor 10min scatter")
        plt.legend()
        # plt.savefig("3D solver diff floor 10min",format='png',dpi=150)
        plt.show()

    def read_serial(self,SAVE):
        if SAVE:
            #directly read from serial port
            ser = serial.Serial('/dev/cu.usbmodem14401',115200) 
            # tags=np.empty([0,2],dtype=float)
            start=time.time()
            # while time.time()-start<10:
            #     print('time: ',time.time()-start)

            # for i in range(600):
            info=[]#store all information here
            while time.time()-start<600:
                read_serial=ser.readline()
                #######  change from bytes to string #######
                line = str(read_serial,'UTF-8')
                # print("len(line): ",len(line))
                line = line.replace('\x00','') #remove all the NUL characters
                line = line[:-3]#remove the last ";"
                # print("line: ",line)
                info.append(line+'\n')
                self.NSDI_read_TDoA_new(line)
            # print("tags: ",tags)

            print("self.tags: ",self.tags)
            # print("self.tags2: ",self.tags2)
            # print("self.tags3: ",self.tags3)
            with open('tagdiff1minfiltertdoacenter', 'wb') as saveFile:
                saved_tags = self.tags.tobytes()
                saveFile.write(saved_tags)
            # with open('tag2diff1mincenter', 'wb') as saveFile:
            #     saved_tags2 = self.tags2.tobytes()
            #     saveFile.write(saved_tags2)
            # with open('tag3diff1mincenter', 'wb') as saveFile:
            #     saved_tags3 = self.tags3.tobytes()
            #     saveFile.write(saved_tags3)

            # with open('scatterdiff1center.txt', 'w') as f:
            #     f.write(json.dumps(info))

# #read from text file
# with open('test.txt', 'r') as f:
#     a = json.loads(f.read())

            # print("all_tdoas: ",self.all_tdoas)
            with open('all_tdoa1minfiltertdoacenter', 'wb') as saveFile:
                all_t = self.all_tdoas.tobytes()
                saveFile.write(all_t)
        else:
            # self.plots()
            self.plot_tdoas()
            # self.scatterplot()

gs=generic_solver()
gs.read_serial(False)
# NSDI_read_TDoA_new("0,0;3600,0;3600,3100;0,3100@115;484;238")
# NSDI_read_TDoA_new("0,0;3600,0;3600,3100;0,3100;1500,1500;1000,1500@115;484;238;345;34")

