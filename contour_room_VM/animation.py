import matplotlib.pyplot as plt
from serial_read import tag_candidates
import matplotlib.animation as animation

xs = []
ys = []

# This function is called periodically from FuncAnimation
def animate(i,xs,ys):

    xs.append(tag_candidates[0][0])
    ys.append(tag_candidates[0][1])

    print('xs',xs)

    # Draw x and y lists
    plt.cla()
    plt.plot(xs,ys)

    # Format plot
    plt.title('Real-Time Location Tracker')
    plt.xlim([100000,150000])
    plt.ylim([70000,80000])
    plt.show()

ani = animation.FuncAnimation(plt.gcf(), animate)
