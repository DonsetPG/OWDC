import numpy as np
import random
import time
import matplotlib.pyplot as plt
size = 0
print("starting to load data...")
dts1 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_rotatif5.npy')
print(dts1[0])
print("5 to go...")
dts2 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_rotatif10.npy')
print("4 to go...")

dts3 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_rotatif15.npy')
print("3 to go...")

dts4 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_rotatif20.npy')
print("2 to go...")

dts5 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_rotatif25.npy')
print("1 to go...")

dts6 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_rotatif26.npy')
print("done")
basique = 50479465.4067654

size += len(dts1)
size += len(dts2)
size += len(dts3)
size += len(dts4)
size += len(dts5)
size += len(dts6)
dts = [dts1,dts2,dts3,dts4,dts5,dts6]
RATIO = size/100000
newDts = []

rev = 0

for _ in range(100000):
    indx1 = random.randint(0,5)
    dt = dts[indx1]
    indx2 = random.randint(0,len(dt)-1)
    line = dt[indx2]
    rev += line[3]
    newDts.append(line)
dts = [newDts]
RATIO_BIS = basique/rev

print(RATIO_BIS," ",RATIO)
print(1/RATIO_BIS," ",1/RATIO)

# On veut ici optimiser les revenues sur les utilisateurs rotatifs. On va utiliser un algorithme génétique

RATIO = min(RATIO,RATIO_BIS)
NB_WEEKS = 52.1429
PROBA_MUTATE = 0.06
POPULATION_SIZE = 50
RATIO_TOURNOI = POPULATION_SIZE/2
ELITE_SIZE = 1

############


def deltaTimeSpent(h,oldPrice,newPrice,oldTime):
    y = 0.999 - h*0.1195 + 0.0482*h**2 - 0.0072*h**3 + 0.0005*h**4 - 0.00001639*h**5 + 0.0000002059*h**6
    deltaPrice = oldPrice - newPrice
    deltaTime = y*(deltaPrice/1.6)
    actualTime = oldTime + deltaTime
    actualTime = min(2.0,max(0.1,actualTime))
    return actualTime

def deltaFreq(h,oldPrice,newPrice):
    y = 20.53 + h*15.773 - 4.2409*h**2 + 0.4187*h**3 - 0.0158*h**4 + 0.0001*h**5 - 0.00000346*h**6
    deltaPrice = oldPrice - newPrice
    deltaFreqA = y*(deltaPrice/1.6)
    deltaFreqA = min(100,max(-250,deltaFreqA))
    return deltaFreqA

############

# On considère qu'une solution est représentée par un tableau : chaque colonne est le prix à l'heure
# dans un arrondissement donnée
# Les solutions vont aussi posseder un attribut score : les revenues obtenus sur un an avec la politique de prix
# associée;


class Solution:

    def __init__(self):
        self.score = 0
        self.prix = [0 for i in range(20)]
        self.alpha = 0
        self.revenue = 0
        self.revenuePerArrondissement = [0 for i in range(20)]
        self.usersPerArrondissement = [0 for i in range(20)]
        self.deltaFreqPerArrondissement = [0 for i in range(20)]

# On veut ensuite pouvoir créer des solutions aléatoirements. On va ici restreindre nos prix à [1,10]

    def generateRandom(self):
        self.alpha = random.random()
        for i in range(len(self.prix)):
            self.prix[i] = random.randint(2,7) + random.random()

    def reset(self):
        self.score = 0
        self.revenue = 0
        self.revenuePerArrondissement = [0 for i in range(20)]
        self.usersPerArrondissement = [0 for i in range(20)]
        self.deltaFreqPerArrondissement = [0 for i in range(20)]

# On doit pouvoir calculer son score. Ici, il faut, pour chaque utilisateurs rotatifs, regarder son arrondissement, et le prix
# que l'on propose. En fonction du prix, on va mettre à jour le temps que l'utilisateur va passer garer (impact du prix).
# Une fois ce travail réalisé pour tout les utilisateurs, on regarde comment nos prix vont influencer la frequentation, et
# ajouter/enlever au revenue le changement de freq*le revenue moyen de l'arrondissement
# (Pour prendre en compte les personnes décidant de ne pas se garer, ou d'aller dans un parking souterrain)

# Pour ce faire, on utilise dataRotatif pour le calcul du revenue, et les fonctions deltaFreq et deltaTimeSpent

    def simulation(self):
        self.reset()
        for dataset in dts:
            for line in dataset:
                hour = int(line[5].hour)
                arrondissement = int(line[8])
                timeSpent = float(line[4])
                oldHRate = float(line[11])
                newHRate = float(self.prix[arrondissement-1])

                if float(line[4]) ==0 or float(line[11]) ==0:
                    timePaid = 1
                else:
                    timePaid = min(1,float(line[3])/(float(line[4])*float(line[11])))

                newTime = deltaTimeSpent(hour,
                                        oldHRate,
                                        newHRate,
                                        timeSpent)
                deltafreq = deltaFreq(hour,oldHRate,newHRate)
                if (arrondissement == 1 or arrondissement == 2 or arrondissement == 3) and newHRate < 7.1:
                    newTime = timeSpent
                    deltafreq = 0
                if hour < 13.1 and hour > 10.1:
                    money = newTime*(newHRate + newHRate*self.alpha)*timePaid
                else:
                    money = newTime*newHRate*timePaid

                if oldHRate < newHRate and deltafreq > 0:
                    deltafreq = - deltafreq
                if oldHRate > newHRate and deltafreq < 0:
                    deltafreq = - deltafreq
                self.revenue += money
                self.revenuePerArrondissement[arrondissement-1] += money
                self.usersPerArrondissement[arrondissement-1] += 1
                self.deltaFreqPerArrondissement[arrondissement-1] += deltafreq

    def computeScore(self):
        self.score = self.revenue
        if self.usersPerArrondissement == 0:
            self.usersPerArrondissement = 1
        #print("revenue de la solution pre freq ; ",self.revenue*RATIO)
        #print("revenue de la solution pre freq ; ",self.revenue)
        manque = 0
        for i in range(len(self.revenuePerArrondissement)):
            #print("Prix : ",self.prix[i])
            averageRevArr = self.revenuePerArrondissement[i]/self.usersPerArrondissement[i]
            averageFreq = self.deltaFreqPerArrondissement[i]/self.usersPerArrondissement[i]
            #print("averageRevArr : ",averageRevArr)
            #print("averageFreq : ",averageFreq)

            manque += averageFreq*averageRevArr


        #print("somme des freq*revArr := ",manque)
        self.score += manque*24
        self.score = self.score*RATIO



###########


# On met maintenant en place les différentes fonctions d'un algorithme génétique :

    def mutate(self):
        if random.random() < PROBA_MUTATE:
            self.alpha = random.random()
        for i in range(len(self.prix)):
            if random.random() < PROBA_MUTATE:
                self.prix[i] = random.randint(2,7) + random.random()

    def get_child(self,solutionBis):
        child = Solution()
        if random.random() <  0.5:
            child.alpha = self.alpha
        else:
            child.alpha = solutionBis.alpha

        for i in range(len(child.prix)):
            if random.random() <  0.5:
                child.prix[i] = self.prix[i]
            else:
                child.prix[i] = solutionBis.prix[i]
        return child

# On peut maintenant créer nos différentes population :

class Population:

    def __init__(self,generation):
        self.size = POPULATION_SIZE
        self.generation = generation
        self.population = []
        self.best = None
        self.bestScore = 0

    def firstPopulation(self):
        for _ in range(self.size):
            solution = Solution()
            solution.generateRandom()
            self.population.append(solution)
        self.best = self.population[0]

    def computeScore(self):
        self.best = self.population[0]
        cpt = 0
        for solution in self.population:
            cpt +=1
            if cpt%10 == 0:
                print("Still computing a solution...")
            solution.simulation()
            solution.computeScore()
            print(sum(solution.usersPerArrondissement))
            if solution.score > self.bestScore:
                self.bestScore = solution.score
                self.best = solution

    def tournoi(self):
        indx1 = random.randint(0,self.size-1)
        indx2 = random.randint(0,self.size-1)
        while indx2 == indx1:
            indx2 = random.randint(0,self.size-1)

        indx3 = random.randint(0,self.size-1)
        while indx3 == indx1 or indx3 == indx2:
            indx3 = random.randint(0,self.size-1)

        indx4 = random.randint(0,self.size-1)
        while indx4 == indx1 or indx4 == indx2 or indx4 == indx3:
            indx4 = random.randint(0,self.size-1)

        if self.population[indx1].score > self.population[indx2].score:
            best1 = indx1
        else:
            best1 = indx2

        if self.population[indx3].score > self.population[indx4].score:
            best2 = indx3
        else:
            best2 = indx4


        if self.population[best1].score > self.population[best2].score:
            best = best1
        else:
            best = best2

        return self.population[best]


    def computeNextPopulation(self,x,y):
        newP = Population(self.generation+1)
        self.computeScore()
        x.append(self.generation)
        y.append(self.bestScore)
        for _ in range(self.size//2):
            winner = self.tournoi()
            newP.population.append(winner)

        for _ in range(self.size//2,self.size-10):
            indx1 = random.randint(0,self.size//2-1)
            indx2 = random.randint(0,self.size//2-1)
            while indx2 == indx1:
                indx2 = random.randint(0,self.size//2-1)
            child = newP.population[indx1].get_child(newP.population[indx2])
            newP.population.append(child)
        #print(self.best)
        newP.population.append(self.best)
        for _ in range(9):
            s = Solution()
            s.generateRandom()
            newP.population.append(s)
        print(len(self.population))
        print(len(newP.population))
        for solution in newP.population:
            #print(solution)
            solution.reset()
            solution.mutate()
        return newP



####################################

# on peut maintenant faire tourner notre algorithme génétique. On ne va pour le moment que tracer le score de la meilleure
# solution en fonction de la generation
print("DTS size ==> ",len(dts[0]))
print("Start computing...")
start = time.time()
end = time.time()
X = []
Y = []
droite = []
basique = 50479465.4067654
population = Population(0)
population.firstPopulation()



while population.generation < 20:
    start = time.time()
    print("STARTING GENERATION ",population.generation)
    population = population.computeNextPopulation(X,Y)
    print("Current bestScore => ",Y[-1])
    print(" de delta with 2014 ",(Y[-1]-basique))

    droite.append(basique)
    end = time.time()
    remaining = (end-start)*(10 - population.generation)
    print("Time remaining : ",remaining)

population.computeScore()
print("Le bestScore est ",population.bestScore)
print("Grâce à la solution ===> ")
print(population.best.prix)
print(population.best.revenuePerArrondissement)
print(population.best.usersPerArrondissement)
print(population.best.deltaFreqPerArrondissement)
print(population.best.alpha)
print(" went to generation ",population.generation)

plt.plot(X,Y,'b+')
plt.plot(X,droite,'r--')
plt.title('score par generation')
plt.xlabel('generation')
plt.ylabel('score')
plt.gca().legend(('size := 50','with 2014 policy'))
plt.show()
plt.gcf().clear()

