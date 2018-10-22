import numpy as np


def read_coordinate(s):
    sx = ""
    sy = ""
    cpt = 0
    while s[cpt] != ",":
        sx += s[cpt]
        cpt+=1
    sy = s[cpt+1:]
    #print("test x : ",sx)
    #print("test y : ",sy)
    x = float(sx)
    y = float(sy)
    return x,y

def get_index(tab,coord):
    return tab.index(coord)

def traitement(line,dataset,dataset_coordinates):
    x,y = read_coordinate(line[12])
    coord = [x,y]
    rot = 0
    res = 0
    cp = 0
    cb = 0
    mix = 0
    rot2 = 0
    if line[1] == "Rotatif":
        rot = 1
    else:
        res = 1
    if line[2] == "CB":
        cb = 1
    else:
        cp = 1
    if line[9] == "MIX":
        mix  =1
    else:
        rot2 = 1

    line[4] = float(line[4])
    line[3] = float(line[3])
    line[8] = float(line[8])

    if coord not in dataset_coordinates:
        dataset_coordinates.append(coord)
        indx = len(dataset_coordinates)-1

        data = [coord,[line[4]],line[4],[line[3]],line[3],rot,res,cb,cp,line[8],mix,rot2,[line[10]],[line[11]]]
        dataset.append(data)
    else:
        indx = get_index(dataset_coordinates,coord)
        data = dataset[indx]
        data[1].append(line[4])
        data[2] += line[4]
        data[3].append(line[3])
        data[4] += line[3]
        data[5] += rot
        data[6] += res
        data[7] += cb
        data[8] += cp
        data[10] += mix
        data[11] += rot2
        data[12].append(line[10])
        data[13].append(line[11])

print("start loeading data...")
print("=>")
dts0 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_0.npy')
print("===>")
dts1 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_1.npy')
print("====>")
dts2 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_2.npy')
print("=====>")
dts3 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_3.npy')
print("======>")
dts4 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_4.npy')
print("=======>")
dts5 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_5.npy')
print("========>")
dts6 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_6.npy')
print("=========>")
dts7 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_7.npy')
print("=============>")
dts8 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_8.npy')
print("==============>")
dts9 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_9.npy')
print("===============>")
dts10 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_10.npy')
print("================>")
dts11 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_11.npy')
print("=================>")
dts12 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_12.npy')
print("===================>")
dts13 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_13.npy')
print("=====================>")
dts14 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_14.npy')
print("======================>")
dts15 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_15.npy')
print("========================>")
dts16 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_16.npy')
print("==========================>")
dts17 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_17.npy')
print("============================>")
dts18 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_18.npy')
print("==============================>")
dts19 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_19.npy')
print("================================>")
dts20 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_20.npy')
print("=====================================>")
dts21 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_21.npy')
print("=========================================>")
dts22 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_22.npy')
print("===========================================>")
dts23 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_23.npy')
print("=============================================>")
dts24 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_24.npy')
print("data loaded")

dts = [dts0,dts1,dts2,dts3,dts4,dts5,dts6,dts7,dts8,dts9,dts10,dts11,dts12,dts13,dts14,dts15,dts16,dts17,dts18,dts19,dts20,dts21,dts22,dts23,dts24]
#dts = [dts0]
# chaque case représente un parking
new_dts = []
dts_coordinate = []
# elles se présentent dans la forme suivante :
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
print("start data computing...")
for dataset in dts:
    print("start on a new dataset...")
    for i in range(len(dataset)):
        line = dataset[i]
        traitement(line,new_dts,dts_coordinate)
    print("dataset done")

save_name = "/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_by_parking"
np.save(save_name,new_dts)
