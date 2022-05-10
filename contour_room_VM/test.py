
# l = [34,55,6,4,6,3]

# a = range(0,len(l))
# print('a: ',a)

# r = [i for (i,j) in zip(a,l) if j>30]
# print(r)

# zipped = [("a", 1), ("b", 2)]
# unzipped_object = zip(*zipped)
# print(unzipped_object)

# import itertools

# combo2 = []
# list = [4,3,6,2]
# for item in itertools.combinations(list,2):
#     combo2.append(item)
# print(combo2)
#print(itertools.combinations(list,3))

import numpy as np

# arr = [1,2]
# test = [[1],[2]]
# try_arr = np.empty((0,2))
# try_arr = np.vstack((try_arr,arr))
# #arr1 = np.array(arr)
# print(np.transpose(try_arr))
# print(np.transpose(test))

# anchor_locations = np.array([[2.34,2.45],[5.34,45.3],[65.4,45.2],[45.3,3.54]])

# def GDOP(anchor_locations, tag_location):
#     anchor_locations = np.transpose(anchor_locations)
#     tag_location = [[1][2]]
    
#     for anchor in anchor_locations:
#         relative_distances = anchor - tag_location
#         distance_vec = np.sqrt(np.sum(np.power(relative_distances,2), axis=0))
#         H = relative_distances / distance_vec
#         Q = inv(np.multiply(np.transpose(H),H))
#         dop = np.sqrt(trace(Q))
#         print('........',dop)

# GDOP(anchor_locations,)

# a = np.array([1,2,3,4])
# print((a).T)

# print(len([1]))
# print(range(len([1,2,3])))
# print(range(3))

# from operator import itemgetter 
# a = [-2, 1, 5, 3, 8, 5, 6]
# b = [1, 2, 5]
# itemgetter(*b)(a) = 0
# print(a)
# Result:
# (1, 5, 5)

# def GDOP(anchor_locations, tag_location):

#         #anchor_locations = np.transpose(anchor_locations)
#         #print('aaaaaa',anchor_locations)
#         relative_distances = anchor_locations - tag_location
#         #print('rrrrrrrrr',relative_distances)
#         distance_vec = np.array([np.sqrt(np.sum(np.power(relative_distances,2), axis=1))]).T
#         #print('ddddddd',distance_vec)
#         H = relative_distances / distance_vec
#         #print('hhhhhhhhhhh',H)
#         Q = inv(np.dot(np.transpose(H),H))
#         #print('qqqqqqqqq',Q)
#         #print('tttttttt',np.trace(Q))
#         dop = np.sqrt(np.trace(Q))
#         #print('........',dop)
#         return dop

#  a1 = [1,2]
#  a2 = [1,2,3]
#  A = []
#  A.append(a1)
#  A.append(a2)
#  print(A)

# list = [0,-1,-4,2,4]
# mappedList = map(abs,list)
# print(mappedList)

#list = [1,1,0,2,4,0,5,5,6,3]
# d = [np.diff(list) != 0]
# print(d)

#print(np.nonzero(list))
#print(sum(list[0:4]))
# i1 = []
# [i1[:,0],i2,i3] = [[1,2,3],2,3]
# print(i1)

import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.show()
