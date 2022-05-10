# from urllib.parse import urlparse
# from urllib.parse import parse_qs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.collections as collections
import pylab as pl

with open('sample_pos1', 'rb') as inFile:
    sample_pos = inFile.read()
    pos = np.frombuffer(sample_pos,dtype=int)
pos = np.reshape(pos,(len(pos)//2,2))
print("pos: ",pos)
with open('beacons1', 'rb') as inFile:
    beacons = inFile.read()
    beacons = np.frombuffer(beacons,dtype=float)
beacons = np.reshape(beacons,(len(beacons)//2,2))
print("beacons: ",beacons)
# anchor_combo = np.array([[0,1,2],[0,1,3],[0,2,3],[0,1,2,3]],dtype=list)
# with open('anchor_combo1', 'w') as saveFile:
#     combos_list = []
#     for an_combo in anchor_combo:
#         # print("str(an_combo): ",str(an_combo))
#         combo_string = "".join(str(an_combo))
#         combos_list.append(combo_string)
#     stored_combo = ";".join(combos_list)
#     saveFile.write(stored_combo)

# #read error matrix from file
# combo_list = []
# with open('anchor_combo1', 'r') as inFile:
#     anchor_combo = inFile.read()
# print("combo: ",anchor_combo)

# lines = [[(1, 2), (1, 3)]]

# print("shape: ",np.array([(0, 1), (1, 1)]).shape)
# lc = collections.LineCollection(lines,linewidths=2)
# fig, ax = pl.subplots()
# ax.add_collection(lc)
# plt.scatter(1,2, s=30,color='green')
# plt.scatter(1,3,s=30,color='orange')
# plt.show()
# error_matrix = np.array([1.2,1,1])
# with open('error_matrix', 'wb') as saveFile:
#     #.write() does not automatically add a newline, like print does
#     data = error_matrix.tobytes()
#     saveFile.write(data)

# with open('error_matrix', 'rb') as inFile:
#     content = inFile.read()
#     content = np.frombuffer(content,dtype=float)
#     print("content: ",content)
    # for line in inFile:
    #     #get rid of EOL
    #     line = inFile.rstrip()
    #     print("line: ",line)

        #Or another approach if we want to simply print each token on a newline
        # for word in line:
        #     print word 
# import matplotlib.pyplot
# from mpl_toolkits.mplot3d import Axes3D

# dates       = [20020514, 20020515, 20020516, 20020517, 20020520]
# highs       = [1135, 1158, 1152, 1158, 1163]
# lows        = [1257, 1253, 1259, 1264, 1252]
# upperLimits = [1125.0, 1125.0, 1093.75, 1125.0, 1125.0]
# lowerLimits = [1250.0, 1250.0, 1156.25, 1250.0, 1250.0]

# zaxisvalues0= [0, 0, 0, 0, 0]
# zaxisvalues1= [1, 1, 1, 1, 1]
# zaxisvalues2= [2, 2, 2, 2, 2]

# fig = matplotlib.pyplot.figure()
# ax  = fig.add_subplot(111, projection = '3d')

# ax.plot(dates, zaxisvalues1, lowerLimits, color = 'b')
# ax.plot(dates, zaxisvalues2, upperLimits, color = 'r')

# for i,j,k,h in zip(dates,zaxisvalues0,lows,highs):
#     ax.plot([i,i],[j,j],[k,h],color = 'g')

# ax.scatter(dates, zaxisvalues0, highs, color = 'g', marker = "o")
# ax.scatter(dates, zaxisvalues0, lows, color = 'y', marker = "^")
# matplotlib.pyplot.show()
# url = '/some_path?some_key=some_value'
# parsed_url = urlparse(url)
# captured_value = parse_qs(parsed_url.query)['some_key'][0]

# print(captured_value)
# s = 'ab\ncd\nef'
# print(s.replace('\n', ''))
# print(s.translate({ord('\n'): None}))
# print("\x00\x00\x00")
# print(ord("\x00"))

# for index in range(10):
#     mu, sigma = 0, 50
#     noise = np.random.normal(mu, sigma)
#     print(noise)
#     index = index + 1

