import numpy as np
import matplotlib.pyplot as plt
import time
dts = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_by_arrondissement.npy')

def get_time_avg(line):
    length = len(line[1])
    avg = line[2]/length
    return avg

def get_cost_avg(line):
    length = len(line[3])
    avg = line[4]/length
    return avg

def get_ratio_rot(line):
    length = line[5]+line[6]
    avg = line[5]/length
    return avg
def get_ratio_res(line):
    length = line[5]+line[6]
    avg = line[6]/length
    return avg
def get_ratio_cb(line):
    length = line[7]+line[8]
    avg = line[7]/length
    return avg
def get_ratio_cp(line):
    length = line[7]+line[8]
    avg = line[8]/length
    return avg
## Reminder :

# 0 : coordinates
# 1 : tab des horaires
# 2 : sommes des horaires
#3 : tab des couts
#4 : somme des couts
#5 : nb users rotatifs
#6 : nb users résidents
#7 : nb payments cb
#8 : nb payments cp
#9 : arrondissement
#10 : nb systeme mix
#11 : nb system ROT
#12 : residential AREA
#13 : hourly rate

avgTime = [0 for i in range(20)]
avgCout = [0 for i in range(20)]
ratioRotatif = [0 for i in range(20)]
ratioResidents = [0 for i in range(20)]
ratioCb = [0 for i in range(20)]
ratioCp = [0 for i in range(20)]

for i in range(20):
    line = dts[i]
    arrondissement = int(line[9])-1
    print("Arrondissement : ",(arrondissement+1))
    avgTime[arrondissement] = get_time_avg(line)
    avgCout[arrondissement] = get_cost_avg(line)
    ratioRotatif[arrondissement] = get_ratio_rot(line)
    ratioResidents[arrondissement] = get_ratio_res(line)
    ratioCb[arrondissement] = get_ratio_cb(line)
    ratioCp[arrondissement] = get_ratio_cp(line)

######################

ind = np.arange(1,21)  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, ratioCb, width,
                color='SkyBlue', label='RatioCB')
rects2 = ax.bar(ind + width/2, ratioCp, width,
                color='IndianRed', label='RatioCp')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Ratio')
ax.set_title('Ratio de CB/Carte Paris en fonction des arrondissements')
ax.set_xticks(ind)
ax.set_xticklabels(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))
ax.legend()

plt.show()
plt.gcf().clear()
#########################

ind = np.arange(1,21)  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, ratioRotatif, width,
                color='SkyBlue', label='RatioRot')
rects2 = ax.bar(ind + width/2, ratioResidents, width,
                color='IndianRed', label='RatioRes')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Ratio')
ax.set_title('Ratio de rotatifs/résidents en fonction des arrondissements')
ax.set_xticks(ind)
ax.set_xticklabels(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))
ax.legend()

plt.show()
plt.gcf().clear()
#########################

ind = np.arange(1,21)  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, avgCout, width,
                color='SkyBlue', label='AvgCost')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('En euro')
ax.set_title('Cout moyen en fonction des arrondissements')
ax.set_xticks(ind)
ax.set_xticklabels(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))
ax.legend()

plt.show()
plt.gcf().clear()
#########################

ind = np.arange(1,21)  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, avgTime, width,
                color='SkyBlue', label='avgTime')


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('En Heure')
ax.set_title('Temps passé en fonction des arrondissements')
ax.set_xticks(ind)
ax.set_xticklabels(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11', '12', '13', '14', '15', '16', '17', '18', '19', '20'))
ax.legend()

plt.show()
plt.gcf().clear()
#########################
