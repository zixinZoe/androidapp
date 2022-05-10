import serial
import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.animation as animation
from tag_solver import tag_solver
from correction import antenna_correct_ddoa
import generic_solver
from PIL import Image, ImageDraw
import pathlib

def NSDI_read_TDoA_new():

    anchor_locations = np.array([[0,0],
                            [3600,0],
                            [3600,3100],
                            [0, 3100]])

    antenna_delays = [-514.800046735725,
                    -515.807752377787,
                    -515.311106592656, 
                    -514.793541561308]

    ser = serial.Serial('/dev/cu.usbmodem14201',115200)  

    curpath = pathlib.Path(__file__).parent.resolve() 
    print('curpath: ',curpath)
    path = curpath / 'map.png'
    map = Image.open(path) 
    map.show()

    draw = ImageDraw.Draw(map) # w:1194; h:976
    # w,h = map.size 
    # print('w: ',w) 
    # print('h: ',h)
    draw.point((500,500), fill="white")
    # while True:
    # #     plt.scatter(anchor_locations[:,0],anchor_locations[:,1]) #plot anchor locations
    #     tag_candidates = np.empty((2,0))

    #     read_serial=ser.readline()
    #     #######  change from bytes to string #######
    #     line = str(read_serial,'UTF-8')
    #     print('line: ',line)
    #     line = line[:-3]
    #     print('line: ',line)

    #     tag_loc = generic_solver.NSDI_read_TDoA_new(line)
    #     print('tagLoc: ',tag_loc)
        
    #     if(len(tag_loc) == 2):
    #         plt.scatter(tag_loc[0],tag_loc[1]) #plot original tag locations
    #         # plt.cla()
    #         plt.xlim([-10000,50000])
    #         plt.ylim([-10000,50000])
    #         plt.draw()
    #         plt.pause(0.000001)
    #         plt.cla()
    #                 #time.sleep(1)

NSDI_read_TDoA_new()
