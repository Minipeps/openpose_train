import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

experiments = [
    # 'pig5_21',
    # 'pig5_v1',
    # 'pig5_v2.1',
    # 'pig5_v2.2',
    # 'pig5_v2.3',
    # 'pig5_v2.4',
    # 'pig5_v2.5',
    # 'pig5_v3',
    'pig5_v4',
]

filesToPlot = [
    '../training_results/{}/pig/pig_5/training_log.txt'.format(xp) for xp in experiments
    # '../training_results/{}/pig/pig_5/resumed_training_log.txt'.format(xp) for xp in experiments
]

figures = []
axes = []

waitingTime = 1 # in minutes

###################### Plot parameters & definitions ######################

sampling_rate = 20
textsToSearch = [
    ', loss = ',
    'loss_stage0_L1 = ',
    'loss_stage0_L2 = ',
    'loss_stage1_L2 = ',
    'loss_stage2_L2 = ',
    'loss_stage3_L2 = ',
    'loss_stage4_L2 = ',
]
everyXIterationsText = '(every {} iterations)'.format(sampling_rate)
labels = [
    'loss',
    'loss_stage0_L1 {}'.format(everyXIterationsText),
    'loss_stage0_L2 {}'.format(everyXIterationsText),
    'loss_stage1_L2 {}'.format(everyXIterationsText),
    'loss_stage2_L2 {}'.format(everyXIterationsText),
    'loss_stage3_L2 {}'.format(everyXIterationsText),
    'loss_stage4_L2 {}'.format(everyXIterationsText),
]
numbersPerIter = 7
numbersPerRow = 4

def pltFunc(ax, k):
    if k == 0:
        return ax.loglog
    return ax.plot

def isRelevantLine(line):
    relevant = False
    i = 0
    while i < len(textsToSearch) and not relevant:
        relevant = textsToSearch[i] in line
        i += 1
    return relevant

def getPlotData(xpIndex):
    # Read log file
    with open(filesToPlot[xpIndex]) as logFile:
        log = logFile.readlines()
        logFile.close()

    # Keep only relevant lines
    log = [line for line in log if isRelevantLine(line)]

    # Extract loss value
    losses = [ [], [], [], [], [], [], [] ]
    for i in range(len(log)):
        if (i%numbersPerIter == 0):
            losses[i%numbersPerIter].append(float(log[i].split(' ')[-1]))
        else:
            losses[i%numbersPerIter].append(float(log[i].split(' ')[-2]))

    x_axis = [i*sampling_rate*1e-3 for i in range(len(losses[0]))]

    return x_axis, losses

def setup():
    for index in range(len(experiments)):
        print("Plotting experiment " + experiments[index] + "...")
        X, Y = getPlotData(index)
        # Setup layout and axes
        figures.append(plt.figure())
        for k in range(2):
            ax = figures[index].add_subplot(1, 2, k+1)
            axes.append(ax)
            for i in range(len(labels)):
                pltFunc(axes[index+k], k)(X,Y[i])
                figures[index].set_label(textsToSearch[i])

            ax.set_title('Training Loss - OpenPose ({})'.format(experiments[index]))
            ax.set_xlabel("10^3 iterations")
            ax.set_ylabel("loss")
            ax.legend(labels)
            ax.grid(which='minor', axis='both')
            ax.grid(which='major', axis='both')

def animate(iter):
    for index in range(len(experiments)):
        X, Y = getPlotData(index)
        # Plot losses in both LogLog and Decimal scale
        for k in range(2):
            axes[index+k].clear()
            for i in range(len(labels)):
                pltFunc(axes[index+k], k)(X,Y[i])
                figures[index].set_label(textsToSearch[i])

            axes[index+k].set_title('Training Loss - OpenPose ({})'.format(experiments[index]))
            axes[index+k].set_xlabel("10^3 iterations")
            axes[index+k].set_ylabel("loss")
            axes[index+k].legend(labels)
            axes[index+k].grid(which='minor', axis='both')
            axes[index+k].grid(which='major', axis='both')
    
        print(experiments[index] + " experiment: " + str(len(Y[0]) * sampling_rate) + " iterations.")
    # Sleep
    print("Sleeping for {}mins...".format(waitingTime))
    print('')

################################### END ###################################

if __name__ == "__main__":
    print("Setup...")
    setup()
    print("Setting up animations...")
    for fig in figures:
        ani = animation.FuncAnimation(fig, animate, interval = waitingTime * 60 * 1000)
    print("Setup done!")
    plt.show()