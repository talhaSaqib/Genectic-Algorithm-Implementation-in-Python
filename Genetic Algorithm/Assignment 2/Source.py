import copy
import random
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

def calcDist(path):
    distance = 0
    for i in range(0, 311):
        distance += path[i].distances[path[i + 1].no]
    return distance

def calFitness(path):
    return 1 / calcDist(path)


#--------Loading-------------------------------------
names = readNameOfCities('dataset/usca312_name.txt')
xy = readCoordinatesFile('dataset/usca312_xy.txt')
distances = readDistanceFile('dataset/usca312_dist.txt')


path = []
# make cities and add it in a path
for i in range(0, 312):
    city1 = city(xy[i][0], xy[i][1], names[i], i, distances[i])  # distance 2d array having rows of distances?
    path.append(city1)


k = 10          # population size , make it even  AND not LESS THAN 6
population = []

def selectParent( selectionIntervals, randomInt ):
    global k

    for i in range( 0, k ):
        if randomInt >= selectionIntervals[i][0] and randomInt <= selectionIntervals[ i ][ 1 ] :
            return i
    return -1


#make population
for j in range (0,k):

    #shuffle path
    random.shuffle(path)

    #chromosome1 = chromosome(path)
    population.append(copy.copy(path))                           #without the class of chromosome!!


#ITERATIONS
iterations = 1000
for m in range(0, iterations):
        print(m)

        newGen = []

        sum = 0
        #SELECTION INTERVAL
        for tour in population:
            sum += calFitness(tour)

        proportions = [calFitness(tour) / sum for tour in population]

        # 1 - 100
        startingLimit = 1

        selectionIntervals = []
        for proportion in proportions:
            endingLimit = startingLimit + int(round(proportion * 100, 0) - 1)

            interval = [startingLimit, endingLimit]

            startingLimit = endingLimit + 1
            selectionIntervals.append(interval)

        for i in range(0, int(k / 2)):
            # Now generate random number.
            parentOne = selectParent(selectionIntervals, random.randint(1, 100))
            parentTwo = selectParent(selectionIntervals, random.randint(1, 100))

            while parentOne == parentTwo:
                parentOne = selectParent(selectionIntervals, random.randint(1, 100))
                parentTwo = selectParent(selectionIntervals, random.randint(1, 100))

            New = []
            #CROSSOVER
            #child 1
            New = population[parentOne][0:156]            #first half of P1

            for i in range(0,312):
                if population[parentTwo][i] not in New:
                    New.append(population[parentTwo][i])

            newGen.append(New)

            #child2
            New = []
            New = population[parentTwo][0:156]            #first half of P2

            for i in range(0,312):
                if population[parentOne][i] not in New:
                    New.append(population[parentOne][i])

            newGen.append(New)

        alpha = 70
        #MUTATION
        for i in range(0, k):
            mut = random.randint(0, 100)
            if (mut <= alpha):

                rand = random.randint(0, 311)
                rand2 = random.randint(0, 311)
                while(rand2 == rand):
                    rand2 = random.randint(0, 311)

                newGen[i][rand], newGen[i][rand2] = newGen[i][rand2], newGen[i][rand]      #swap


        #UPDATING POPULATION
        population += newGen

        #sortmax
        population.sort(key=lambda x:calFitness(x), reverse=True)

        #trim to length k
        population = population[:k]


#print(population[0])
BestDistance = calcDist(population[0])
BestFitness = calFitness(population[0])
print("Best Distance = " , BestDistance)
print("Best Fitness = " , BestFitness)


print("TIME(s): " , (time.time() - start_time))

#Plotting
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 12
fig_size[1] = 12
plt.rcParams["figure.figsize"] = fig_size

x = []
y = []
for i in range(0,312):
    x.append(population[0][i].x)
    y.append(population[0][i].y)
plt.scatter(x,y, color="green")
plt.plot(x,y, color="purple")
plt.show()






















