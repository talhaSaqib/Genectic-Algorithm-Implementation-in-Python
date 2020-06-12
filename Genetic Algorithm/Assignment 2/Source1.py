import copy
import random

import math
import matplotlib.pyplot as plt
import time

start_time = time.time()
#------------------------------------------------
def readNameOfCities( nameOfFile ):
    with open(nameOfFile) as file:
        # Skip 15 Lines from start.
        for i in range(0, 15):
            next(file)


        names = [ [ name.strip() for name in line.split(',') ] for line in file ]
        return names

#-------------------------------------------------
def readCoordinatesFile( nameOfFile ):
    with open(nameOfFile) as file:
        # Skip 7 Lines from start.
        for i in range(0, 7):
            next(file)

        xyCoordinates = [ [ float( digit ) for digit in line.split() ] for line in file ]
        return xyCoordinates

#-------------------------------------------------
def readDistanceFile( nameOfFile ):
    with open(nameOfFile) as file:
        # Skip 7 Lines from start.
        for i in range(0, 7):
            next(file)

        distanceArray = []

        for line in file:
            row = []

            for digit in line.split():
                row.append(int(digit))

            lineCount = 0
            for lineInner in file:
                for digit in lineInner.split():
                    row.append(int(digit))

                lineCount += 1
                if lineCount == 31:
                    break
            distanceArray.append(row)

        return distanceArray

#--------Classes----------------------------------------
class city:
    def __init__(self, x, y, name, no, distances):
        self.x = x
        self.y = y
        self.name = name
        self.no = no
        self.distances = distances

#---Functions----------------

def calcDist(state):
    distance = 0
    for i in range(0, 311):
        distance += state[i].distances[state[i + 1].no]
    return distance

def calFitness(state):
    return (1 / calcDist(state))

def acceptanceProb(stateE, newE, temp):
    if(newE < stateE):
        return 1.0

    return math.exp(-abs(stateE - newE)/temp)

#--------Loading-------------------------------------
names = readNameOfCities('dataset/usca312_name.txt')
xy = readCoordinatesFile('dataset/usca312_xy.txt')
distances = readDistanceFile('dataset/usca312_dist.txt')

state = []
# make cities and add it in a state
for i in range(0, 312):
    city1 = city(xy[i][0], xy[i][1], names[i], i, distances[i])  # distance 2d array having rows of distances?
    state.append(city1)

#assume current one is the best
best = copy.copy(state)

coolingRate = 0.99
temperature = 10000
temp = temperature

#SIMLATED ANNEALING
step = 0
while( temperature > 0.0):
    step += 1
    print(step)

    new_state = copy.copy(state)
    #random.shuffle(new_state)


    #swapping
    index1 = random.randint(0, 311)
    index2 = random.randint(0, 311)
    while(index2 == index1):
        index2 = random.randint(0, 311)

    new_state[index1], new_state[index2] = new_state[index2], new_state[index1]


    #CALCULATING ENERGIES
    stateEnergy = calcDist(state)
    newEnergy = calcDist(new_state)


    #SELECTING NEIGHBOUR
    rand = random.uniform(0.0, 1.0)
    if(acceptanceProb(stateEnergy, newEnergy, temperature) >= rand):
        state = copy.copy(new_state)

    #UPDATING BEST
    if(calcDist(state) < calcDist(best)):
        best = copy.copy(state)

    #COOLING
    temperature = temp * (coolingRate**step)                                #Exponential multiplicative cooling, proposed by Kirkpatrick, Gelatt and Vecchi (1983)

    print("temp = ", temperature)

#OUTPUT
print( "BestFitness = " , calFitness(best))
print( "BestDistance = " , calcDist(best))

print("TIME(s): " , (time.time() - start_time))

#PLOTTING
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 12
fig_size[1] = 12
plt.rcParams["figure.figsize"] = fig_size

x = []
y = []
for i in range(0,312):
    x.append(best[i].x)
    y.append(best[i].y)
plt.scatter(x,y, color="blue")
plt.plot(x,y, color="orange")
plt.show()





























