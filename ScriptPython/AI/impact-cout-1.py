import numpy as np
import math
import time
import folium
import random

######




import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble.partial_dependence import plot_partial_dependence
from sklearn.ensemble.partial_dependence import partial_dependence


#######

coupleParking = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple.npy')
dataParkingById = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_by_parking_3.npy')
print("data loaded")
dataCountsById = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/avg_by_park_by_hour.npy')


print(dataCountsById[0])
print(dataCountsById[0][1])
time.sleep(5)

listId = []
cpt = 0
#for line in dataCountsById:
    #cpt+=1
    #if cpt%1000000 == 0:
        #print("line ",cpt," done...")
    #listId.append(line[0])


print("ddata precomputed")
## On compare pour chaque couple,

## On ne vas regarder que si il existe une loi linéaire entre HRate et le taux de fréquentation/le temps passé

## Pour chaque couple de parking, que l'on va finalement considérer comme un seul et unique parking,
# on réalise une GBoosting dessus pour regarder si le prix influe. On récupère les paramètres de ce GB pour chaque couple, et
# ensuite on les compares

#dataCoupleX = []
#dataCoupleY1 = []
#dataCoupleY2 = []
#print("nombre de couple : ",len(coupleParking))
#start = time.time()
#for i in range(len(coupleParking)):
    #if i == 1:
        #end = time.time()
        #delta = (end-start)
        #remaining = delta*(len(coupleParking)-1)
        #print("time remaining ==> ",remaining)

    #if i > 1:
        ##end = time.time()
        #remaining = remaining - (end-start)
        #print("time remaining ==> ",remaining)

    #print("traitement du ",i," eme couples ")
    #id1,id2 = coupleParking[i][0],coupleParking[i][1]
    #dataCouple = []
    #cpt = 0
    #for line in dataParkingById:



        #cpt+=1
        #if line[0] == id1 or line[0] == id2:
            #line = list(line)
            #dataCouple.append(line)
    #print("start processing dataCouple...")
    #for line in dataCouple:
        #id = line[0]
        #indx = listId.index(id)
        #hour = min(int(line[2]),20)
        #avgCountByHour = dataCountsById[indx][hour-8]
        #line.append(avgCountByHour)

    #for line in dataCouple:
        #dataX = [line[2],line[3],line[4]]
        #dataY1 = line[1]
        #dataY2 = line[5]
        #dataCoupleX.append(dataX)
        #dataCoupleY1.append(dataY1)
        #dataCoupleY2.append(dataY2)

print("data computed")

#np.save('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-X',dataCoupleX)
#np.save('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-Y1',dataCoupleY1)
#np.save('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-Y2',dataCoupleY2)

dataCoupleX = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-X.npy')
dataCoupleY1 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-Y1.npy')
dataCoupleY2 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple-Y2.npy')


print("data built, saved in a npy")

#print("Training GBRT for Y1...")

names = ['Heure arrivée','Arrondissement','prix heure']

#clf1 = GradientBoostingRegressor(n_estimators=100, max_depth=4,
                                    #learning_rate=0.1, loss='huber',
                                    #
                                    #
                                    random_state=1)
#clf1.fit(dataCoupleX,dataCoupleY1)
#print(" done.")

print("Training GBRT for Y2...")

clf2 = GradientBoostingRegressor(n_estimators=100, max_depth=4,learning_rate=0.1, loss='huber',random_state=1)
clf2.fit(dataCoupleX,dataCoupleY2)
print(" done.")

#print('Convenience plot with ``partial_dependence_plots`` for Y1')

#features = [2]
#fig, axs = plot_partial_dependence(clf1,dataCoupleX, features,
                                       #feature_names=names,
                                       #n_jobs=3, grid_resolution=50)
#fig.suptitle('Partial dependence of parking value on nonlocation features\n'
                 #'for the parking dataset based on timeSpent')
#plt.subplots_adjust(top=0.9)
#plt.ylim(3,6)
#plt.show()
#plt.gcf().clear()

print('Convenience plot with ``partial_dependence_plots`` for Y2')

features = [0,1,2,(0,1),(2, 1),(0,2)]
fig, axs = plot_partial_dependence(clf2,dataCoupleX, features,
                                       feature_names=names,
                                       n_jobs=3, grid_resolution=50)
fig.suptitle('Partial dependence of parking value on nonlocation features for the parking dataset based on AvgCounts')
plt.subplots_adjust(top=0.9)

plt.show()
plt.gcf().clear()

############
print('Custom 3d plot via ``partial_dependence``')
fig = plt.figure()

target_feature = (0, 1)
pdp, axes = partial_dependence(clf2, target_feature,
                                   X=dataCoupleX, grid_resolution=50)
XX, YY = np.meshgrid(axes[0], axes[1])
Z = pdp[0].reshape(list(map(np.size, axes))).T
ax = Axes3D(fig)
surf = ax.plot_surface(XX, YY, Z, rstride=1, cstride=1,
                           cmap=plt.cm.BuPu, edgecolor='k')
ax.set_xlabel(names[target_feature[0]])
ax.set_ylabel(names[target_feature[1]])
ax.set_zlabel('Partial dependence')
    #  pretty init view
ax.view_init(elev=22, azim=122)
plt.colorbar(surf)
plt.suptitle('Partial dependence of avgCount on heure arrivée et arrondissement')
plt.subplots_adjust(top=0.9)

plt.show()
plt.gcf().clear()
##############
print('Custom 3d plot via ``partial_dependence``')
fig = plt.figure()

target_feature = (0, 2)
pdp, axes = partial_dependence(clf2, target_feature,
                                   X=dataCoupleX, grid_resolution=50)
XX, YY = np.meshgrid(axes[0], axes[1])
Z = pdp[0].reshape(list(map(np.size, axes))).T
ax = Axes3D(fig)
surf = ax.plot_surface(XX, YY, Z, rstride=1, cstride=1,
                           cmap=plt.cm.BuPu, edgecolor='k')
ax.set_xlabel(names[target_feature[0]])
ax.set_ylabel(names[target_feature[1]])
ax.set_zlabel('Partial dependence')
    #  pretty init view
ax.view_init(elev=22, azim=122)
plt.colorbar(surf)
plt.suptitle('Partial dependence of avgCount on heure arrivée et prix_heure')
plt.subplots_adjust(top=0.9)

plt.show()
plt.gcf().clear()
##############
print('Custom 3d plot via ``partial_dependence``')
fig = plt.figure()

target_feature = (1, 2)
pdp, axes = partial_dependence(clf2, target_feature,
                                   X=dataCoupleX, grid_resolution=50)
XX, YY = np.meshgrid(axes[0], axes[1])
Z = pdp[0].reshape(list(map(np.size, axes))).T
ax = Axes3D(fig)
surf = ax.plot_surface(XX, YY, Z, rstride=1, cstride=1,
                           cmap=plt.cm.BuPu, edgecolor='k')
ax.set_xlabel(names[target_feature[0]])
ax.set_ylabel(names[target_feature[1]])
ax.set_zlabel('Partial dependence')
    #  pretty init view
ax.view_init(elev=22, azim=122)
plt.colorbar(surf)
plt.suptitle('Partial dependence of avgCount on arrondissement et prix_heure')
plt.subplots_adjust(top=0.9)

plt.show()
plt.gcf().clear()
##############
