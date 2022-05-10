import string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

roomX = 40
roomY = 20
sample_distance = 1
threshold = 2
count = 100
locations = np.array([[0,0],[10,20],[20,0],[40,20]])

#sample & anchors plot
xs = np.array(list(range(0,roomX+1,sample_distance)))
ys = np.array(list(range(0,roomY+1,sample_distance)))
new_xs = np.repeat(xs,len(ys))
new_ys = np.tile(ys,len(xs))
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(new_xs,new_ys,color="green",label="sample points")
# ax.scatter(locations[:,0],locations[:,1],color="red",label="anchors")
# plt.xlabel("Length")
# plt.ylabel("Width")
# plt.legend(loc="lower right")
# plt.savefig("samples&anchors")
# plt.show()

fig = plt.figure()
ax = fig.subplots()
with open('error_matrix1', 'rb') as inFile:
    data = inFile.read()
    ori_errors = np.frombuffer(data,dtype=float)
cmap = plt.cm.hot
norm = colors.Normalize(vmin=np.amin(ori_errors),vmax=np.amax(ori_errors))
ax.scatter(new_xs,new_ys,color=cmap(norm(ori_errors)),label="sample points")
ax.scatter(locations[:,0],locations[:,1],color="blue",label="anchors")
sm = plt.cm.ScalarMappable(cmap=cmap,norm=norm)
fig.colorbar(sm)
plt.xlabel("Length")
plt.ylabel("Width")
plt.legend(loc="lower right")
plt.title("sample_error_hot_scatter")
plt.savefig("sample_error_hot_scatter")
plt.show()

#sample new error scatter
# new_fig = plt.figure()
# new_ax = new_fig.subplots()
# with open('new_error_matrix', 'rb') as inFile:
#     data = inFile.read()
#     new_errors = np.frombuffer(data,dtype=float)
# cmap = plt.cm.hot
# new_norm = colors.Normalize(vmin=np.amin(new_errors),vmax=np.amax(new_errors))
# new_ax.scatter(new_xs,new_ys,color=cmap(new_norm(new_errors)),label="sample points")
# new_ax.scatter(locations[:,0],locations[:,1],color="blue",label="anchors")
# new_sm = plt.cm.ScalarMappable(cmap=cmap,norm=new_norm)
# new_fig.colorbar(new_sm)
# plt.xlabel("Length")
# plt.ylabel("Width")
# plt.legend(loc="lower right")
# plt.title("sample_new_error_hot_scatter")
# plt.savefig("sample_new_error_hot_scatter")
# plt.show()

# fig = plt.figure()
# ax = fig.subplots()
# with open('sample_pos1', 'rb') as inFile:
#     sample_pos = inFile.read()
#     pos = np.frombuffer(sample_pos,dtype=int)
# pos = np.reshape(pos,((len(pos)//2,2)))
# # print("pos: ",pos)
# with open('error_matrix1', 'rb') as inFile:
#     data = inFile.read()
#     ori_errors = np.frombuffer(data,dtype=float)
# ori_errors = np.reshape(ori_errors,(int((roomX+1)//sample_distance),int((roomY+1)//sample_distance)))
# large_ori_errors = []
# for position in pos:
#     large_ori_errors.append(ori_errors[position[0],position[1]])
# # print("large_ori_errors: ",large_ori_errors)
# cmap = plt.cm.hot
# norm = colors.Normalize(vmin=0,vmax=np.amax(large_ori_errors))
# ax.scatter(pos[:,0],pos[:,1],color=cmap(norm(large_ori_errors)),label="large sample points")
# ax.scatter(locations[:,0],locations[:,1],color="blue",label="anchors")
# sm = plt.cm.ScalarMappable(cmap=cmap,norm=norm)
# fig.colorbar(sm)
# plt.xlabel("Length")
# plt.ylabel("Width")
# plt.legend(loc="lower right")
# plt.title("large_sample_error_hot_scatter")
# plt.savefig("large_sample_error_hot_scatter")
# plt.show()

# fig = plt.figure()
# ax = fig.subplots()
# with open('sample_pos1', 'rb') as inFile:
#     sample_pos = inFile.read()
#     pos = np.frombuffer(sample_pos,dtype=int)
# pos = np.reshape(pos,((len(pos)//2,2)))
# # print("pos: ",pos)
# with open('error_matrix1', 'rb') as inFile:
#     data = inFile.read()
#     ori_errors = np.frombuffer(data,dtype=float)
# ori_errors = np.reshape(ori_errors,(int((roomX+1)//sample_distance),int((roomY+1)//sample_distance)))
# large_ori_errors = []
# for position in pos:
#     large_ori_errors.append(ori_errors[position[0],position[1]])
# with open('new_error_matrix', 'rb') as inFile:
#     data = inFile.read()
#     new_errors = np.frombuffer(data,dtype=float)
# new_errors = np.reshape(new_errors,(int((roomX+1)//sample_distance),int((roomY+1)//sample_distance)))
# large_new_errors = []
# for position in pos:
#     large_new_errors.append(new_errors[position[0],position[1]])
# cmap = plt.cm.hot
# norm = colors.Normalize(vmin=0,vmax=np.amax(large_ori_errors))
# ax.scatter(pos[:,0],pos[:,1],color=cmap(norm(large_new_errors)),label="new large sample points")
# ax.scatter(locations[:,0],locations[:,1],color="blue",label="anchors")
# sm = plt.cm.ScalarMappable(cmap=cmap,norm=norm)
# fig.colorbar(sm)
# plt.xlabel("Length")
# plt.ylabel("Width")
# plt.legend(loc="lower right")
# plt.title("large_sample_new_error_hot_scatter")
# plt.savefig("large_sample_new_error_hot_scatter")
# plt.show()

# #read error matrix from file
# with open('error_matrix1', 'rb') as inFile:
#     data = inFile.read()
#     data = np.frombuffer(data,dtype=float)
# ori_data = np.reshape(data,(int((roomX+1)//sample_distance),int((roomY+1)//sample_distance)))
# position = np.argwhere(data>threshold) #samples that require beacon
# print("positions: ",position)
# print("positionlen: ",len(position))

# #read all errors from file
# with open('all_errors1', 'rb') as inFile:
#     data = inFile.read()
#     all_data = np.frombuffer(data,dtype=float)
# # all_data = np.reshape(data,(int((roomX+1)//sample_distance),int((roomY+1)//sample_distance),count))

# with open('new_error_matrix', 'rb') as inFile:
#     data = inFile.read()
#     data = np.frombuffer(data,dtype=float)
# data1 = np.reshape(data,(int((roomX+1)//sample_distance),int((roomY+1)//sample_distance)))
# position1 = np.argwhere(data1>threshold) #samples that require beacon
# print("position1:",position1)
# print("position1len: ",len(position1))

# #read new all errors from file
# with open('new_all_errors', 'rb') as inFile:
#     data = inFile.read()
#     new_all_data = np.frombuffer(data,dtype=float)
# # new_all_data = np.reshape(data,(int((roomX+1)//sample_distance),int((roomY+1)//sample_distance),count))

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.scatter(all_data,new_all_data,label="all errors for each sample")
# ax1.scatter(ori_data,data1,color = "red",label="median errors for each sample")
# x1,y1 = [-1e100,1e100],[2,2]
# x2,y2 = [2,2],[-1e100,1e100]
# ax1.plot(x1,y1,color="orange",label="threshold")
# ax1.plot(x2,y2,color="orange")
# plt.xlim(np.amin(all_data)-1,np.amax(all_data)+1)
# plt.ylim(np.amin(new_all_data)-1,np.amax(new_all_data)+1)
# plt.xlabel("Original Errors")
# plt.ylabel("New Errors")
# plt.legend(loc="upper right")
# plt.savefig("Before&After Beacon Error")
# plt.show()
# #read error matrix from file
# # with open('combos1', 'rb') as inFile:
# #     combos = inFile.read()
# #     combos = np.frombuffer(combos)
# # print("combos: ",combos)

# #read error matrix from file
# # with open('dop_current1', 'rb') as inFile:
# #     dop = inFile.read()
# #     dop = np.frombuffer(dop,dtype=float)
# # print("dop: ",dop)

# # #read error matrix from file
# # with open('tag_cand1', 'rb') as inFile:
# #     tag = inFile.read()
# #     tag = np.frombuffer(tag,dtype=string)
# # print("tag: ",tag)

# # #read error matrix from file
# # combo_list = []
# # with open('anchor_combo1', 'r') as inFile:
# #     anchor_combo = inFile.read()
# # print("combo: ",anchor_combo)

# # with open("best_combos1","r") as inFile:
# #     best_combo = inFile.read()
# #     print("best_combo: ",best_combo)