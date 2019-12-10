import matplotlib.pyplot as plt


def onclick(event):
    print(event)
    datax.append(event.xdata)
    datay.append(event.ydata)
    plt.scatter(datax, datay, color="blue")
    fig.canvas.draw()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
datax = []
datay = []
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()