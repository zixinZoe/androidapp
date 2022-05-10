import random
import numpy as np

threshold = 3
anchors_xs = random.sample(range(0,50),30)
anchors_ys = random.sample(range(0,50),30)
anchors = np.array(list(zip(anchors_xs,anchors_ys)))

cur_index = 0
delete_index = []
for anchor in anchors:
    print("anchors: ",anchors)
    print("anchors[(cur_index+1):,0]: ",anchors[(cur_index+1):,0])
    min_dis = np.amin(np.sqrt((anchor[0]-anchors[(cur_index+1):,0])**2+(anchor[1]-anchors[(cur_index+1):,1])**2))
    print("min_dis: ",min_dis)
    if min_dis < threshold:
        delete_index.append(cur_index)
        # anchors = np.delete(anchors,cur_index,axis=0)
    cur_index+=1
anchors = np.delete(anchors,delete_index,axis=0)
print("lenanchors: ",len(anchors))
print("anchors: ",anchors)
with open('sample_anchors1', 'wb') as saveFile:
    sample_anchors = anchors.tobytes()
    saveFile.write(sample_anchors)