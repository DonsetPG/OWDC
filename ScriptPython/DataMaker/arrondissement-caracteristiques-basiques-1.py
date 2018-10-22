import numpy as np

print("start loading data ")
dts = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_by_parking.npy')
print("data loaded")
new_dts = []
print(dts.shape)
dts_arrondissement = []

def traitement(line,new_dts,dts_arrondissement):
    arrondissement = line[9]

    if arrondissement not in dts_arrondissement:
        dts_arrondissement.append(arrondissement)
        new_dts.append(line)
    else:
        indx = dts_arrondissement.index(arrondissement)
        prev_line = new_dts[indx]
        for i in range(len(prev_line)):
            if i != 9:
                prev_line[i] += line[i]
        new_dts[indx] = prev_line
print("start computing...")
for i in range(len(dts)):
    if i%250 == 0:
        print("still computing... ",i," th line...")
    line = dts[i]
    traitement(line,new_dts,dts_arrondissement)

print("done with computing")
print("start saving...")
save_name = "/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_by_arrondissement"
np.save(save_name,new_dts)
print("saving is done")
