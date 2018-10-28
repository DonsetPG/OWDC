import numpy as np
import math
import time
import folium
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
####
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, BatchNormalization
from keras.optimizers import SGD
print("Loading data...")

# names = ['Heure arrivée','Arrondissement','prix heure']
ratio = [0.8756584820997221,0.8672629557266442,0.8309602764464986,0.7848630709598966,0.7756545076980699,0.8110615098607352,0.7383929588697733,0.8456268268013157,0.8170646733879411,0.788203060473909,0.7764474734949067,0.7912496050075073,0.8034461291718106,0.7914122023986402,0.7787219847638109,0.7613221590983069,0.746039108451651,0.7067925006666171,0.7747937320959459,0.725192224111263]

dataCoupleX = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-X.npy')
Y2 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-Y1.npy')
Y1 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-Y2.npy')
print("data loaded 100%")

# 20 arrondissements
# x heures (in [0,23])
# --------------> n_labels := 24*20 = 480

newData = []
newDataIndx = []
for i in range(len(dataCoupleX)):
    if i%100000 == 0:
        print("computing...")
    line = dataCoupleX[i]
    timeSpent = Y1[i]
    if timeSpent < 500:

        couple = [line[0],line[1]]

        if couple in newDataIndx:
            indx = newDataIndx.index(couple)
            if line[2] < 3:
                newData[indx][0] += timeSpent
                newData[indx][2] +=1
            else:
                newData[indx][1] += timeSpent
                newData[indx][3] +=1
        else:
            newTab = [0,0,0,0]
            if line[2] < 3:
                newTab[0] += timeSpent
                newTab[2] +=1
            else:
                newTab[1] += timeSpent
                newTab[3] +=1
            newData.append(newTab)
            newDataIndx.append(couple)

data = []

for line in newData:
    t = [0,0]
    if line[0] == 0:
        t[0] = 0
    else:
        t[0] = line[0]/line[2]
    if line[1] == 0:
        t[1] = 0
    else:
        t[1] = line[1]/line[3]
    data.append(t)

paire = [[15,6],[15,7],[14,6],[14,5],[13,5],[12,4],[12,11],[20,11],[19,10],[18,9],[18,10],[17,8],[16,7]]

# Il y a 17 arrondissements : 4 --> 20 ;

dataByArrondissement = []
for i in range(4,21):
    dataHour = [0 for i in range(24)]
    for j in range(len(newDataIndx)):
        if newDataIndx[j][1] == i:
            #print(data[j][0] + data[j][1]," arr : ",newDataIndx[j][1]," hour : ",int(newDataIndx[j][0]))
            indx = int(newDataIndx[j][0])
            dataHour[indx] = data[j][0] + data[j][1]
            dataHour[indx] *= ratio[i-4]
    dataByArrondissement.append(dataHour)

for couple in paire:
    indx1 = couple[0]
    indx2 = couple[1]
    Y = dataByArrondissement[indx1-4]
    Ybis = dataByArrondissement[indx2-4]
    X = np.arange(24)
    print("start plotting...")
    label1 = "arrondissement "+str(indx1)
    label2 = "arrondissement "+str(indx2)
    s1 = 'Arrondissement '+str(indx1)
    s2 = 'Arrondissement '+str(indx2)
    plt.plot(X,Y, "r--",label=s1)
    plt.plot(X,Ybis,"b:o",label=s2)
    plt.title("Nombre d'utilisateurs rotatifs dans les arrondissements "+str(indx1)+" en rouge vs "+str(indx2)+" en bleu (2.4 |vs| 4.0)")
    plt.xlabel('Heure de la journée')
    plt.ylabel('Nombre utilisateurs rotatifs')
    plt.gca().legend((s1,s2))
    plt.show()
    plt.gcf().clear()

for i in range(len(newDataIndx)):
    print("arrondissement : ",newDataIndx[i][1]," et heure : ",newDataIndx[i][0])
    print("avgCounts pour 2.4 : ",data[i][0]," | 4.0 : ",data[i][1]," |")
    print(" _____________________________________________")
