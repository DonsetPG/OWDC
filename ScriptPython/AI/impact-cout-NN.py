import numpy as np
import math
import time
import folium
import random
import copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
####
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
######## Keras : 
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, BatchNormalization
from keras.optimizers import SGD
##########

print("Loading data...")
dataCoupleX = list(np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-X.npy'))
Y2 = list(np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-Y1.npy'))
Y1old = list(np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-Y2.npy'))
print("data loaded 100%")


ratio = [0.8756584820997221,0.8672629557266442,0.8309602764464986,0.7848630709598966,0.7756545076980699,0.8110615098607352,0.7383929588697733,0.8456268268013157,0.8170646733879411,0.788203060473909,0.7764474734949067,0.7912496050075073,0.8034461291718106,0.7914122023986402,0.7787219847638109,0.7613221590983069,0.746039108451651,0.7067925006666171,0.7747937320959459,0.725192224111263]
paire = [[15,6],[15,7],[14,6],[14,5],[13,5],[12,4],[12,11],[20,11],[19,10],[18,9],[18,10],[17,8],[16,7]]

for i in range(len(dataCoupleX)):
    line = dataCoupleX[i]
    timeSpent = Y1old[i]
    arr = line[1]
    for couple in paire:
        if couple[0] == arr and timeSpent < 500:
            otherArr = couple[1]
            newDataX = copy.deepcopy(line)
            newDataX[1] = otherArr
            newDataY = copy.deepcopy(timeSpent)
            dataCoupleX.append(newDataX)
            Y1old.append(newDataY)
        elif couple[1] == arr and timeSpent < 500:
            otherArr = couple[0]
            newDataX = copy.deepcopy(line)
            newDataX[1] = otherArr
            newDataY = copy.deepcopy(timeSpent)
            dataCoupleX.append(newDataX)
            Y1old.append(newDataY)


tempX = []
tempY = []
for i in range(len(dataCoupleX)):
    if Y1old[i] < 500:
        arr = int(dataCoupleX[i][1])
        Y1old[i] *= ratio[arr-1]
        tempX.append(dataCoupleX[i])
        tempY.append(Y1old[i])


dataCoupleX = np.array(tempX)
Y1old = np.array(tempY)
Y2 = np.array(Y2)
avg2 = []
avg4 = []

for i in range(len(dataCoupleX)):
    if dataCoupleX[i][2] > 3 and Y1old[i] < 1000:
        avg4.append(Y1old[i])
    elif dataCoupleX[i][2] < 3 and Y1old[i] < 1000:
        avg2.append(Y1old[i])


s2 = sum(avg2)
s4 = sum(avg4)
m2 = s2/(len(avg2))
m4 = s4/(len(avg4))
print("average 2.4/hours : ",m2)
print("average 4/hours : ",m4)


for i in range(len(Y1old)):
    if Y1old[i] > 1000:
        Y1old[i] = 0

print(Y1old[0])
print(max(Y1old))
time.sleep(5)
X1 = []
X2 = []
X3 = []
Y1 = []
for i in range(10000):
    indx = random.randint(0,3000000)
    X1.append(dataCoupleX[indx][0])
    X2.append(dataCoupleX[indx][2])
    X3.append(dataCoupleX[indx][1])
    Y1.append(Y1old[indx])


Y1 = np.array(Y1)
X1 = np.array(X1)
X2 = np.array(X2)
X3 = np.array(X3)

####

Y1 = []
for y in Y1old:

    Y1.append([y])

Y1 = np.array(Y1)

########
# Processing the data to normalize it;
print("start proprecessing")
# For dataCoupleX :
# names = ['Heure arrivée','Arrondissement','prix heure']
print("datacoupleX...")
scaler = StandardScaler()
dataCoupleX = scaler.fit_transform(dataCoupleX)
print("done")
#for dataCoupleY1:
print("datacoupleY1...")
scalerY = StandardScaler()
Y1 = scalerY.fit_transform(Y1)
MINY = abs(min(Y1))

for i in range(len(Y1)):
    Y1[i] += MINY
print("done")
# For dataCoupleY2 :
print("datacoupleY2...")
Y2 = (Y2 - np.mean(Y2,axis=0))/(np.std(Y2,axis=0))
print("done")

##########

# Building our NN :

# Very basic NN here, only to see how it reacts to our data, and if the previsions seems legit or not.

model = Sequential()
model.add(Dense(100, activation='relu', input_dim=3))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(32,activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(1, activation='elu'))
model.compile(optimizer='Adam',
              loss='MSE',
              metrics=['accuracy'])


#########
##########
print("start fitting...")

model.fit(x=dataCoupleX, y=Y1,batch_size=256, epochs=50,validation_split=0.3,shuffle=True)
model.save('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/model-hrate-avgcounts.h5')
#reg = LinearRegression()
#reg.fit(dataCoupleX,Y1)
#print(reg.score(dataCoupleX,Y1))
#print(reg.coef_)

print("fitting done")

##########

# let's start to see if the model is smart enough...


X_test = []
for _ in range(10000):


    arrondissement = 11
    hour = 12
    h_rate = random.randint(1,10) + random.random()
    X_test.append([hour,arrondissement,h_rate])

X_test = np.array(X_test)
X_test = scaler.transform(X_test)
print(X_test)
Y_predict =model.predict(X_test)
for i in range(len(Y_predict)):
    Y_predict[i] -= MINY
Y_predict = scalerY.inverse_transform(Y_predict)
X_test = scaler.inverse_transform(X_test)
newX = []
for line in X_test:
    newX.append(line[2])

newX = np.array(newX)


#########
print("start plotting...")
plt.plot(newX,Y_predict, 'ro')
plt.title('counts AVG by h_rate')
plt.xlabel('H_rate')
plt.ylabel('AvgCounts')
plt.show()
plt.gcf().clear()
