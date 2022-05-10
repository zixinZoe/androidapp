from mimetypes import init
from unittest import skip
from sympy import inv_quick
import all_3d
from numpy import random
import numpy as np
import math
import plotly.express as px
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.collections as collections
import pylab as pl

sigma = 1
mu = 0
count = 10
floorWid = 20
floorLen = 40
anchorNum = 4
floorHeight = 10
sample_distance = 1
loc_indexes = list(range(anchorNum))
locations = np.zeros((anchorNum,3))

locations[:,0] = [0,0,40,40]
locations[:,1] = [0,20,0,20]
locations[:,2] = [0,0,0,0] #floor height of anchors

#take 5 samples
# sample_xlocs = random.randint(floorLen,size=5)
# sample_ylocs = random.randint(floorWid,size=5)

# resp_indexes = []
# for i in range(anchorNum):
#     if loc_indexes[:i] == []:
#         resp_indexes = loc_indexes[i+1:]
#     elif loc_indexes[i+1:] == []:
#         resp_indexes = loc_indexes[:i]
#         # print("come here")
#     else:
#         resp_indexes = loc_indexes[:i].append(loc_indexes[i+1:])

#create responders list here!!!!!
# resp_index = []
# loc_indexes = list(range(anchorNum))
# for i in range(anchorNum-1):
#     init_index = i
#     if loc_indexes[:i] == []:
#         resp_index.append(loc_indexes[i+1:])
#     elif loc_indexes[i+1:] == []:
#         resp_index.append(loc_indexes[:i])
#         # print("come here")
#     else:
#         resp_index.append(loc_indexes[:i].append(loc_indexes[i+1:]))

xs = range(0,floorLen+1,sample_distance) #sample locations
ys = range(0,floorWid+1,sample_distance)
count_tdoas = []
for i in range(count):
    tdoas_list = []
    # loc_xs = random.randint(floorLen,size=(anchorNum))
    # loc_ys = random.randint(floorWid,size=(anchorNum))
    # locations[:,0] = loc_xs
    # locations[:,1] = loc_ys #anchor locations
    for x in range(0,floorLen+1,sample_distance):
        for y in range(0,floorWid+1,sample_distance):
            z = 0 #sample on the first floor
            sample_tdoas = []#for each sample point
            init_index = 0
            for init_index in list(range(anchorNum)): # for each initiator
                ini_tdoa = []
                for respIdx in list(range(anchorNum)): #for each anchor
                    s1 = np.sqrt((locations[respIdx][0]-x)**2+(locations[respIdx][1]-y)**2+(locations[respIdx][2]-z)**2)
                    s2 = np.sqrt((locations[init_index][0]-x)**2+(locations[init_index][1]-y)**2+(locations[init_index][2]-z)**2)
                    tdoa = s1-s2
                    noise = np.random.normal(mu, sigma)
                    ini_tdoa.append(tdoa)
                sample_tdoas.append(ini_tdoa)
            tdoas_list.append(sample_tdoas)
    count_tdoas.append(tdoas_list)
count_tdoas = np.array(count_tdoas)

seed = [10,10,10]
sigma = 0.1
count = 10
sampleNum = len(list(xs))*len(list(ys))
count_results = []
for tdoas_list in count_tdoas:
    result = all_3d.read(locations,tdoas_list,seed,sigma,count,sampleNum,anchorNum)
    count_results.append(result)

count_all_error = []# for each count
xy_count_all_error = []
count_sample_median = []
xy_count_sample_median = []
count_all_xs = []
count_all_ys = []
for rst in count_results:
    all_sample_errors = []#for each sample point
    xy_all_sample_errors = []
    xy_sample_median = []#for each sample point
    sample_median = []
    sample_rst_xs = []
    sample_rst_ys = []
    for i in range(len(rst)):#for each sample point
        sample_errors = []
        xy_sample_errors = []
        for tag in rst[i]:#for each initiator
            xy_error = math.sqrt((tag[0]-xs[i//len(list(ys))])**2+(tag[1]-ys[i % len(list(ys))])**2)
            error = math.sqrt((tag[0]-xs[i//len(list(ys))])**2+(tag[1]-ys[i % len(list(ys))])**2 +(tag[2]-0)**2)
            xy_sample_errors.append(xy_error)
            sample_errors.append(error)
            # result
        sample_rst_xs.append(rst[i][:,0])
        sample_rst_ys.append(rst[i][:,1])
        xy_all_sample_errors.append(xy_sample_errors)
        all_sample_errors.append(sample_errors)
        xy_sample_median.append(np.median(np.array(xy_sample_errors)))
        sample_median.append(np.median(np.array(sample_errors)))
    count_all_xs.append(sample_rst_xs)
    count_all_ys.append(sample_rst_ys)
    count_all_error.append(all_sample_errors)
    xy_count_all_error.append(xy_all_sample_errors)
    count_sample_median.append(sample_median)
    xy_count_sample_median.append(xy_sample_median)
count_all_error = np.array(count_all_error)
xy_count_all_error = np.array(xy_count_all_error)
count_all_xs = np.array(count_all_xs)
count_all_ys = np.array(count_all_ys)
z_all_median = [] #median w.r.t all xyz errors
xy_z_all_median = [] #median w.r.t all xy errors

cnt_all_err = np.reshape(count_all_error,((sampleNum,(count*anchorNum))))
xy_cnt_all_err = np.reshape(xy_count_all_error,((sampleNum,(count*anchorNum))))
count_all_xs = np.reshape(count_all_xs,((sampleNum,(count*anchorNum))))
count_all_ys = np.reshape(count_all_ys,((sampleNum,(count*anchorNum))))
# cur_median = np.median(count_all_error[j][i]) #median w.r.t all xyz errors for each sample point
median_xs = []
median_ys = []
for i in range(sampleNum):
    cur_median = np.median(cnt_all_err[i])
    z_all_median.append(cur_median)
    # xy_cur_median = np.median(xy_count_all_error[j][i])#median w.r.t all xy errors for each sample point
    xy_cur_median = np.median(xy_cnt_all_err[i])
    xy_z_all_median.append(xy_cur_median)      

    median_xs.append(count_all_xs[i][np.argsort(xy_cnt_all_err[i])[len(xy_cnt_all_err[i])//2]]) #x coors of median error result
    median_ys.append(count_all_ys[i][np.argsort(xy_cnt_all_err[i])[len(xy_cnt_all_err[i])//2]]) #y coors of median error result

mean_err = np.mean(np.array(all_sample_errors))
median_err = np.median(np.array(all_sample_errors))
var_err = np.var(np.array(all_sample_errors))

xy_mean_err = np.mean(np.array(xy_all_sample_errors))
xy_median_err = np.median(np.array(xy_all_sample_errors))
xy_var_err = np.var(np.array(xy_all_sample_errors))
print('mean: ',mean_err)
print("median: ",median_err)
print("var_err: ",var_err)

print('xy_mean: ',xy_mean_err)
print("xy_median: ",xy_median_err)
print("xy_var_err: ",xy_var_err)
print("anchors: ",locations)


np_xs = np.array(list(xs))
np_ys = np.array(list(ys))
x = np.repeat(np_xs,len(list(ys)))
y = np.tile(ys,len(list(xs)))
z = xy_z_all_median
for i in range(len(z)): # round down outliers
    if z[i]>50:
        z[i] = 50
z3 = z_all_median
for i in range(len(z3)): # round down outliers
    if z3[i]>50:
        z3[i] = 50
# for idx in range(len(x)):
#     for loc_id in range(locations.shape[0]):
#         if x[idx] == locations[loc_id,0] and y[idx] == locations[loc_id,1]:
#             print('x: ',x[idx])
#             print("y: ",y[idx])
#             np.delete(x,idx)
#             np.delete(y,idx)
#             np.delete(z,idx)

for i in range(len(median_xs)):
    cur_x = median_xs[i]
    if cur_x >60:
        median_xs[i]=60
    if cur_x <0:
        median_xs[i]=0
for i in range(len(median_ys)):
    cur_y = median_ys[i]
    if cur_y >30:
        median_ys[i]=30
    if cur_y < 0:
        median_ys[i]=0

x_coors = [x,median_xs]
y_coors = [y,median_ys]
x_ticks = list(range(0,61,sample_distance))
y_ticks = list(range(0,31,sample_distance))

# testxy = []
# testxy.append(median_xs)
# testxy.append(median_ys)
# testxy = np.reshape(np.array(testxy),((861,2)))
# print("testxy: ",testxy)

plt.figure()

first_points = tuple(zip(x,y))
second_points = tuple(zip(median_xs,median_ys))
lines = list(zip(first_points,second_points))
# lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]

lc = collections.LineCollection(lines,linewidths=0.5,color='grey')
fig, ax = pl.subplots()
ax.add_collection(lc)
plt.scatter(x,y, s=30,color='green')
plt.scatter(median_xs,median_ys,s=30,color='orange')


# for i in range(len(count_all_xs.flatten())):
#     cur_x = count_all_xs.flatten()[i]
#     if cur_x >60:
#         count_all_xs.flatten()[i]=60
#     if cur_x <0:
#         count_all_xs.flatten()[i]=0
# for i in range(len(count_all_ys.flatten())):
#     cur_y =count_all_ys.flatten()[i]
#     if cur_y >30:
#         count_all_ys.flatten()[i]=30
#     if cur_y < 0:
#         count_all_ys.flatten()[i]=0
# plt.scatter(count_all_xs.flatten(),count_all_ys.flatten(),s=50,color='orange')


plt.xticks(x_ticks)
plt.yticks(y_ticks)
plt.show()

# plt.xlabel("width", size=24)
# plt.ylabel("lifeExp", size=24)
# plt.savefig("Connecting_paired_points_scatterplot_matplotlib_Python.png",
#             format='png',dpi=150)

#3D plot here(DON'T DELETE)
# #xy
# fig = plt.figure()
# ax = plt.axes(projection ="3d")
 
# # Creating plot
# ax.scatter3D(x, y, z, color = "green")
# ax.scatter3D(locations[:,0],locations[:,1],locations[:,2],color = "red")
# plt.title("first floor xy")
 
# # show plot
# plt.show()

# #xyz
# fig3 = plt.figure()
# ax3 = plt.axes(projection ="3d")
 
# # Creating plot
# ax3.scatter3D(x, y, z3, color = "orange")
# ax3.scatter3D(locations[:,0],locations[:,1],locations[:,2],color = "blue")
# plt.title("first floor xyz")
 
# # show plot
# plt.show()