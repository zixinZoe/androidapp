from mimetypes import init
import pickle
from unittest import skip
from sympy import inv_quick
import all_3d
import all_2d
import best_3d
import best_2d
from numpy import random
import numpy as np
import math
import plotly.express as px
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.collections as collections
import pylab as pl
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

mu = 0
count = 100
floorWid = 20
floorLen = 40
anchorNum = 4
floorHeight = 10
sample_distance = 1
loc_indexes = list(range(anchorNum))
locations = np.zeros((anchorNum,3))
seed = [0,0,0]
sigma = 0.1
sampleNum = 5
anchor_z = 20

locations[:,0] = [0,0,40,40]
locations[:,1] = [0,20,0,20]
# locations[:,0] = [0,20,40,20,0]
# locations[:,1] = [10,0,5,15,20]
locations[:,2] = [anchor_z,anchor_z,anchor_z,anchor_z] #floor height of anchors

#take 5 samples
sample_xlocs = random.randint(floorLen,size=5)
sample_ylocs = random.randint(floorWid,size=5)
sample_zloc = 0

#calculate tdoas
count_tdoas = []#all tdoas; shape:count*sampleNum*anchorNum
for i in range(count):
    tdoas_list = []#for each interation
    for j in range(len(sample_ylocs)):
        x = sample_xlocs[j]
        y = sample_ylocs[j]
        z = 0 #sample on the first floor
        sample_tdoas = []#for each sample point
        init_index = 0 #only one initiator
        for respIdx in list(range(anchorNum)): #for each responder
            s1 = np.sqrt((locations[respIdx][0]-x)**2+(locations[respIdx][1]-y)**2+(locations[respIdx][2]-z)**2)
            s2 = np.sqrt((locations[init_index][0]-x)**2+(locations[init_index][1]-y)**2+(locations[init_index][2]-z)**2)
            tdoa = s1-s2
            print("tdoa: ",tdoa)
            noise = np.random.normal(mu, sigma)
            sample_tdoas.append(tdoa+noise)
        tdoas_list.append(sample_tdoas)
    count_tdoas.append(tdoas_list)
count_tdoas = np.array(count_tdoas)
print("count_tdoa0: ",count_tdoas[0])

#calculate locations 3d solver
count_results = []#all results; shape:count*sampleNum*3
for tdoas_lst in count_tdoas:
    result = all_3d.read(locations,tdoas_lst,seed,sampleNum,anchorNum)
    count_results.append(result)
    # print("count_resultsshape: ",np.array(count_results).shape)
with open('3dresults.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(count_results, f)

#calculate locations 2d solver
count_results_2d = []#all results; shape:count*sampleNum*2
locations_2d = locations[:,:-1]
seed_2d = seed[:-1]
for tdoas_lst in count_tdoas:
    result = all_2d.read(locations_2d,tdoas_lst,seed_2d,sampleNum,anchorNum)
    count_results_2d.append(result)
with open('2dresults.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(count_results_2d, f)

#calculate errors 3d
count_all_error = []# for each iteration
xy_count_all_error = []
count_sample_median = []
xy_count_sample_median = []
count_all_xs = []
count_all_ys = []
count_all_zs = []
for rst in count_results:
    all_sample_errors = []#for each sample point
    xy_all_sample_errors = []
    sample_rst_xs = []
    sample_rst_ys = []
    sample_rst_zs = []
    for i in range(len(rst)):#for each sample point
        tag = rst[i]
        # print("sample: ",[sample_xlocs[i],sample_ylocs[i]])
        # print("tag: ", tag)
        xy_error = math.sqrt((tag[0]-sample_xlocs[i])**2+(tag[1]-sample_ylocs[i])**2)
        error = math.sqrt((tag[0]-sample_xlocs[i])**2+(tag[1]-sample_ylocs[i])**2 +(tag[2]-sample_zloc)**2)
        xy_all_sample_errors.append(xy_error)
        all_sample_errors.append(error)
        sample_rst_xs.append(rst[i][0])
        sample_rst_ys.append(rst[i][1])
        sample_rst_zs.append(rst[i][2])
    count_all_xs.append(sample_rst_xs)
    count_all_ys.append(sample_rst_ys)
    count_all_zs.append(sample_rst_zs)
    count_all_error.append(all_sample_errors)
    xy_count_all_error.append(xy_all_sample_errors)
    # count_sample_median.append(error)
    # xy_count_sample_median.append(xy_error)
count_all_error = np.array(count_all_error)
xy_count_all_error = np.array(xy_count_all_error)
count_all_xs = np.array(count_all_xs)
count_all_ys = np.array(count_all_ys)
count_all_zs = np.array(count_all_zs)
z_all_median = [] #median w.r.t all xyz errors
xy_z_all_median = [] #median w.r.t all xy errors

cnt_all_err = np.transpose(count_all_error)
xy_cnt_all_err = np.transpose(xy_count_all_error)
count_all_xs = np.transpose(count_all_xs)#all calculated x coors; shape:sampleNum*count
count_all_ys = np.transpose(count_all_ys)#all calculated y coors; shape:sampleNum*count
count_all_zs = np.transpose(count_all_zs)#all calculated z coors; shape:sampleNum*count

#calculate median errors
median_xs = []
median_ys = []
for i in range(sampleNum):
    cur_median = np.median(cnt_all_err[i])#median for each sample point
    z_all_median.append(cur_median)#median for the entire floor
    xy_cur_median = np.median(xy_cnt_all_err[i])
    xy_z_all_median.append(xy_cur_median)      
    median_xs.append(count_all_xs[i][np.argsort(xy_cnt_all_err[i])[len(xy_cnt_all_err[i])//2]]) #x coors of median error result
    median_ys.append(count_all_ys[i][np.argsort(xy_cnt_all_err[i])[len(xy_cnt_all_err[i])//2]]) #y coors of median error result

#calculate mean, median, variance of errors across the floor
mean_err = np.mean(np.array(all_sample_errors))
median_err = np.median(np.array(all_sample_errors))
var_err = np.var(np.array(all_sample_errors))

xy_mean_err = np.mean(np.array(xy_all_sample_errors))
xy_median_err = np.median(np.array(xy_all_sample_errors))
xy_var_err = np.var(np.array(xy_all_sample_errors))
print('mean3d: ',mean_err)
print("median3d: ",median_err)
print("var_err3d: ",var_err)

print('xy_mean3d: ',xy_mean_err)
print("xy_median3d: ",xy_median_err)
print("xy_var_err3d: ",xy_var_err)
print("anchors3d: ",locations)


#calculate errors 2d
count_all_error_2d = []# for each iteration
count_sample_median_2d = []
count_all_xs_2d = []
count_all_ys_2d = []
for rst in count_results_2d:
    all_sample_errors_2d = []#for each sample point
    sample_rst_xs_2d = []
    sample_rst_ys_2d = []
    for i in range(len(rst)):#for each sample point
        tag = rst[i]
        error_2d = math.sqrt((tag[0]-sample_xlocs[i])**2+(tag[1]-sample_ylocs[i])**2)
        all_sample_errors_2d.append(error_2d)
        sample_rst_xs_2d.append(rst[i][0])
        sample_rst_ys_2d.append(rst[i][1])
    count_all_xs_2d.append(sample_rst_xs_2d)
    count_all_ys_2d.append(sample_rst_ys_2d)
    count_all_error_2d.append(all_sample_errors_2d)
count_all_error_2d = np.array(count_all_error_2d)
count_all_xs_2d = np.array(count_all_xs_2d)
count_all_ys_2d = np.array(count_all_ys_2d)
z_all_median_2d = [] #median w.r.t all xy errors

cnt_all_err_2d = np.transpose(count_all_error_2d)
count_all_xs_2d = np.transpose(count_all_xs_2d)#all calculated x coors; shape:sampleNum*count
count_all_ys_2d = np.transpose(count_all_ys_2d)#all calculated y coors; shape:sampleNum*count

#calculate median errors
median_xs_2d = []
median_ys_2d = []
for i in range(sampleNum):
    cur_median_2d = np.median(cnt_all_err_2d[i])#median for each sample point
    z_all_median_2d.append(cur_median_2d)#median for the entire floor   
    median_xs_2d.append(count_all_xs_2d[i][np.argsort(cnt_all_err_2d[i])[len(cnt_all_err_2d[i])//2]]) #x coors of median error result
    median_ys_2d.append(count_all_ys_2d[i][np.argsort(cnt_all_err_2d[i])[len(cnt_all_err_2d[i])//2]]) #y coors of median error result

#calculate mean, median, variance of errors across the floor
mean_err_2d = np.mean(np.array(all_sample_errors_2d))
median_err_2d = np.median(np.array(all_sample_errors_2d))
var_err_2d = np.var(np.array(all_sample_errors_2d))

print('xy_mean2d: ',mean_err_2d)
print("xy_median2d: ",median_err_2d)
print("xy_var_err2d: ",var_err_2d)
print("anchors2d: ",locations_2d)
# #crop outliers of median errors across the floor
# z = xy_z_all_median
# for i in range(len(z)): # round down outliers
#     if z[i]>50:
#         z[i] = 50
# z3 = z_all_median
# for i in range(len(z3)): # round down outliers
#     if z3[i]>50:
#         z3[i] = 50

# #crop calculated median x y coors
# for i in range(len(median_xs)):
#     cur_x = median_xs[i]
#     if cur_x >60:
#         median_xs[i]=60
#     if cur_x <0:
#         median_xs[i]=0
# for i in range(len(median_ys)):
#     cur_y = median_ys[i]
#     if cur_y >30:
#         median_ys[i]=30
#     if cur_y < 0:
#         median_ys[i]=0

# x_ticks = list(range(0,61,sample_distance))
# y_ticks = list(range(0,31,sample_distance))

# testxy = []
# testxy.append(median_xs)
# testxy.append(median_ys)
# testxy = np.reshape(np.array(testxy),((861,2)))
# print("testxy: ",testxy)

#plot real 3D
for i in range(len(sample_xlocs)):
    sp_x = sample_xlocs[i]
    sp_y = sample_ylocs[i]
    fig = plt.figure()

    calculated = np.array(list(zip(count_all_xs[i],count_all_ys[i],count_all_zs[i])))
    gt = np.tile(np.array([sample_xlocs[i],sample_ylocs[i],sample_zloc]),(count,1))
    lines = list(zip(gt,calculated))
    # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
    ax  = fig.add_subplot(111, projection = '3d')
    #line segments(DONT DELETE)
    # for j in range(count):
    #     ax.plot([gt[j,0],calculated[j,0]],[gt[j,1],calculated[j,1]],[gt[j,2],calculated[j,2]],color="grey")
   
    # lc = collections.LineCollection(lines,linewidths=0.5,color='grey')
    # fig, ax = pl.subplots()
    # ax.add_collection(lc)

    # ax = plt.axes(projection ="3d")

    ax.scatter(count_all_xs[i],count_all_ys[i],count_all_zs[i],s=30,color='orange',label="result "+str(i))
    ax.scatter(locations[:,0],locations[:,1],locations[:,2],s=30,color='red',label="anchors")
    ax.scatter(gt[:,0],gt[:,1],gt[:,2],s=30,color='green',label="ground truth position")
    plt.legend(loc="upper left")
    # plt.title("Anchor Floor: "+str(1)+" Sample: "+str(i+1))
    plt.title("Calculated 3D Positions ("+"Anchor Floor: "+str(3)+" Sample: "+str(i+1)+")", fontsize=10)
    plt.xlabel("Length")
    plt.ylabel("Width")
    plt.xlim([0,60])
    plt.ylim([0,30])
    ax.set_zlim(0,30)
    # plt.xticks(x_ticks)
    # plt.yticks(y_ticks)
    plt.savefig("Calculated 3D Positions ("+"Anchor Floor: "+str(3)+" Sample: "+str(i+1)+")")
    plt.show()
    plt.close('all')

#plot 3D projection
for i in range(len(sample_xlocs)):
    sp_x = sample_xlocs[i]
    sp_y = sample_ylocs[i]
    fig = plt.figure()

    calculated_z = [anchor_z for i in range(count)]
    calculated = np.array(list(zip(count_all_xs[i],count_all_ys[i],calculated_z)))
    gt = np.tile(np.array([sample_xlocs[i],sample_ylocs[i],anchor_z]),(count,1))
    lines = list(zip(gt,calculated))
    # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
    ax  = fig.add_subplot(111, projection = '3d')
    #line segments(DONT DELETE)
    # for j in range(count):
    #     ax.plot([gt[j,0],calculated[j,0]],[gt[j,1],calculated[j,1]],[gt[j,2],calculated[j,2]],color="grey")
    
    # lc = collections.LineCollection(lines,linewidths=0.5,color='grey')
    # fig, ax = pl.subplots()
    # ax.add_collection(lc)

    # ax = plt.axes(projection ="3d")

    ax.scatter(count_all_xs[i],count_all_ys[i],calculated_z,s=30,color='orange',label="result "+str(i))
    ax.scatter(locations[:,0],locations[:,1],locations[:,2],s=30,color='red',label="anchors")
    ax.scatter(gt[:,0],gt[:,1],gt[:,2],s=30,color='green',label="projected ground truth position")
    plt.legend(loc="upper left")
    plt.title("Projected 3D Positions ("+"Anchor Floor: "+str(3)+" Sample: "+str(i+1)+")", fontsize=10)
    plt.xlabel("Length")
    plt.ylabel("Width")
    plt.xlim([0,60])
    plt.ylim([0,30])
    ax.set_zlim(0,30)
    # plt.xticks(x_ticks)
    # plt.yticks(y_ticks)
    plt.savefig("Projected 3D Positions ("+"Anchor Floor: "+str(3)+" Sample: "+str(i+1)+")")
    plt.show()
    plt.close('all')

#plot projected 2D
for i in range(len(sample_xlocs)):
    sp_x = sample_xlocs[i]
    sp_y = sample_ylocs[i]
    fig = plt.figure()

    cal_z = [locations[0,2] for i in range(count)]
    calculated = np.array(list(zip(count_all_xs_2d[i],count_all_ys_2d[i],cal_z)))
    gt = np.tile(np.array([sample_xlocs[i],sample_ylocs[i],locations[0,2]]),(count,1))
    lines = list(zip(gt,calculated))
    ax  = fig.add_subplot(111, projection = '3d')
    #line segments(DONT DELETE)
    # for j in range(count):
    #     ax.plot([gt[j,0],calculated[j,0]],[gt[j,1],calculated[j,1]],[gt[j,2],calculated[j,2]],color="grey")
    
    # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
    # lc = collections.LineCollection(lines,linewidths=0.5,color='grey')
    # fig, ax = pl.subplots()
    # ax.add_collection(lc)

    # ax = plt.axes(projection ="3d")

    ax.scatter(count_all_xs[i],count_all_ys[i],calculated[0,2],s=30,color='orange',label="result "+str(i))
    ax.scatter(locations[:,0],locations[:,1],locations[:,2],s=30,color='red',label="anchors")
    ax.scatter(gt[:,0],gt[:,1],gt[:,2],s=30,color='green',label="projected ground truth position")
    plt.legend(loc="upper left")
    plt.title("Projected 2D Positions ("+"Anchor Floor: "+str(3)+" Sample: "+str(i+1)+")", fontsize=10)
    plt.xlabel("Length")
    plt.ylabel("Width")
    plt.xlim([0,60])
    plt.ylim([0,30])
    ax.set_zlim(0,30)
    plt.savefig("Projected 2D Positions ("+"Anchor Floor: "+str(3)+" Sample: "+str(i+1)+")")
    plt.show()
    plt.close('all')

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