
import pandas as pd
import h5py
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt

print("Mod imported")

data_case_storage='C:/Users/Arthur/Google Drive/Projets/Autres/OliverWyman/Data/transaction_and_locations_resident.h5'

rev_moy_bord=2259
rev_moy_paris=3417
rev_moy_toul=2047
rev_moy_nice=2018
rev_moy_lille=1821


## Step 4
## Definition of a function reading a table 
def read_HDF_file(file_name, table):
    with pd.HDFStore(file_name, complevel=9, complib='blosc') as store:
         dts = store[table]
         print(dts.shape)
         #tab = np.array(dts[:])
         return dts#,tab

## Calling example: printing the full table /transactions_and_locations(column labels and data) 
df=read_HDF_file(data_case_storage,"/transaction_and_locations")

print("data imported")


"""
Le but est de déterminer quelle répartition de prix donne le meilleur revenu pour Paris, en 2014, le prix d'une heure de parking pour un résident est de 0.065€/h
"""

#revenu_initial=df['amount'].sum()
revenu_initial=11450943.100000003

#info de http://www.leparisien.fr/paris-75/stationnement-a-paris-embouteillage-pour-les-demandes-de-cartes-resident-04-04-2018-7646091.php
n_carte_resident=111165

def repartition_lille_revenu():
    #1/2 journée 1€ type a1
    #1 journée 2€ type a2
    #7 jours 8€ type a3
    #1 mois 25€ (pas présent dans les données car la durée maximale est de 20h)
    
    a1 = df.loc[(df['duration_hours'] < 10)]
    a2 = df.loc[(df['duration_hours'] == 10)]
    a3 = df.loc[(df['duration_hours'] > 10)]
    print('a1: '+str(len(a1)))
    print('a2: '+str(len(a2)))
    print('a3: '+str(len(a3)))
    print('a1+a2+a3: '+str(len(a3)+len(a2)+len(a1)))
    
    revenu = len(a1)*1 + len(a2)*2+ len(a3)*8
    return revenu

def repartition_bordeaux_revenu():
    #1€/journée type a1
    #6€/semaine type a2
    #...
    
    a1 = df.loc[(df['duration_hours'] <= 10)]
    a2 = df.loc[(df['duration_hours'] > 10)]
    print('a1: '+str(len(a1)))
    print('a2: '+str(len(a2)))
    print('a1+a2: '+str(len(a2)+len(a1)))
    
    revenu = len(a1)*1 + len(a2)*6
    return revenu

def repartition_toulouse_revenu():
    #Abonnement 1 an à 135€ qu'on considérera comme le choix général
    #4€/semaine
    
    #On considère uniquement le tarif semaine et on fait la moyenne de temps resté sur tous les parkings et on divise par le nombre de carte de résident
    
    total_temps = df['duration_hours'].sum()
    temps_moyen = total_temps/n_carte_resident
    nombre_de_semaines_moyen=(temps_moyen/10)/7
    revenu=n_carte_resident*135 + 4*nombre_de_semaines_moyen
    
    return revenu
    
def repartition_nice_revenu():
    #Abonnement à 10€/an
    #1.5€/journée type a1
    #7€/semaine type a2
    #...
    
    a1 = df.loc[(df['duration_hours'] <= 10)]
    a2 = df.loc[(df['duration_hours'] > 10)]
    print('a1: '+str(len(a1)))
    print('a2: '+str(len(a2)))
    print('a1+a2: '+str(len(a2)+len(a1)))
    
    revenu = len(a1)*1.5 + len(a2)*7 + n_carte_resident*10
    return revenu

"""
print("Initialement: " +str(revenu_initial))

nice = repartition_nice_revenu()
print("Nice: "+str(nice))

toulouse = repartition_toulouse_revenu()
print("Toulouse: "+str(toulouse))
bordeaux = repartition_bordeaux_revenu()
print("Bordeaux: "+str(bordeaux))

lille = repartition_lille_revenu()
print("Lille: "+str(lille))

paris = revenu_initial
"""

def do_graph():
    
    revenus=(paris, nice, toulouse, bordeaux, lille)
    revenus_id=(1,2,3,4,5)
    
    revenus_ponderes=(paris, nice*(rev_moy_paris/rev_moy_nice), toulouse*(rev_moy_paris/rev_moy_toul), bordeaux*(rev_moy_paris/rev_moy_bord), lille*(rev_moy_paris/rev_moy_lille))
    
    
    ind = np.arange(len(revenus))  # the x locations for the groups
    width = 0.35  # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, revenus, width, yerr=revenus_id,
                    color='SkyBlue', label='non pondéré')
    rects2 = ax.bar(ind + width/2, revenus_ponderes, width, yerr=revenus_id,
                    color='IndianRed', label='pondéré')
    
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Revenu')
    ax.set_title('Revenu des parkings en fonction de différents systèmes')
    ax.set_xticks(ind)
    ax.set_xticklabels(('Paris', 'Nice', 'Toulouse', 'Bordeaux', 'Lille'))
    ax.legend()
    
    
    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.
    
        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """
    
        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
    
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')
    
    
    autolabel(rects1, "left")
    autolabel(rects2, "right")
    
    plt.show()
#do_graph()

NV_IDF = 22522
NV_PACA = 19893
NV_NA = 19991.7
NV_OCC = 19457.2
NV_HDF=18812

def do_graph_niveau_de_vie():
    
    revenus=(paris, nice, toulouse, bordeaux, lille)
    revenus_id=(1,2,3,4,5)
    
    revenus_ponderes=(paris, nice*(NV_IDF/NV_PACA), toulouse*(NV_IDF/NV_OCC), bordeaux*(NV_IDF/NV_NA), lille*(NV_IDF/NV_HDF))
    
    
    ind = np.arange(len(revenus))  # the x locations for the groups
    width = 0.35  # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, revenus, width, yerr=revenus_id,
                    color='SkyBlue', label='non pondéré')
    rects2 = ax.bar(ind + width/2, revenus_ponderes, width, yerr=revenus_id,
                    color='IndianRed', label='pondéré')
    
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Revenu')
    ax.set_title('Revenu des parkings en fonction de différents systèmes')
    ax.set_xticks(ind)
    ax.set_xticklabels(('Paris', 'Nice', 'Toulouse', 'Bordeaux', 'Lille'))
    ax.legend()
    
    
    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.
    
        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """
    
        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
    
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')
    
    
    autolabel(rects1, "left")
    autolabel(rects2, "right")
    
    plt.show()

#do_graph_niveau_de_vie()

"""
Finalement, pour les résidents, la solution suivante va être mise en place:

Il y aura un abonnement à prix dégressif en fonction de la distance au centre de Paris:
* 60€ pour les arrondissements 1 à 4
* 50€ pour les arrondissements 5 à 11
* 40€ pour les arrondissement >= à 12

Les prix seront la moyenne pondérée par rapport au niveau de vie des villes de Lille, Bordeaux, Toulouse et Nice sur 1/2 journée, 1 journée et 1 semaine



soit:
* 1/2 journée : (0.75*NV_IDF/NV_PACA + 1*NV_IDF/NV_HDF + 0.3*NV_IDF/NV_OCC + 0.5*NV_IDF/NV_NA)/4
* 1 journée: (1.5*NV_IDF/NV_PACA + 2*NV_IDF/NV_HDF + 0.6*NV_IDF/NV_OCC + 1*NV_IDF/NV_NA)/4
* 1 semaine: (7*NV_IDF/NV_PACA + 8*NV_IDF/NV_HDF + 4*NV_IDF/NV_OCC+6*NV_IDF/NV_NA)/4

Pour déterminer les revenus par abonnements, on va supposer que le nombre de cartes de résident est proportionnel au counts pour chaque arrondissement

"""



def ratio_by_arr():
    
    """
    id_arr=np.load("C:/Users/Arthur/Google Drive/Projets/Autres/OliverWyman/Data/id_arr.npy")
    d={}
    for a in id_arr:
        d.update({a[0]:a[1]})
        
    
    avg_by_park_by_hour=np.load("C:/Users/Arthur/Google Drive/Projets/Autres/OliverWyman/Data/avg_by_park_by_hour.npy")
    counts_by_arr=[0 for k in range(20)]
    for a in avg_by_park_by_hour:
        counts_by_arr[d[a[0]]-1]+=sum(a[1:])/12
    s=sum(counts_by_arr)
    #Maintenant il faut également prendre en compte le nombre de résidents, pour ce faire on va prendre en compte le pourcentage de résidents par arrondissement grâce à transactions et locations
    data_case_storage_rotatif='C:/Users/Arthur/Google Drive/Projets/Autres/OliverWyman/Data/transaction_and_locations_rotatif.h5'
    
    df_rot =read_HDF_file(data_case_storage_rotatif,"/transaction_and_locations")
    """
    
    #On parcourt maintenant transaction_and_location_resident et on compte pour chaque arrondissement le nombre de transactions
    
    counts_by_arr=[0 for k in range(20)]
    
    for arr in range(20):
        counts_by_arr[arr]+=len(df.loc[df['arrondissement']==arr+1])
    
    #Maintenant on calcule les ratios correspondants
    s=sum(counts_by_arr)
    for i in range(len(counts_by_arr)):
        counts_by_arr[i]/=s
    
    return counts_by_arr


def revenu_final():
    
    dem_journee=(0.75*NV_IDF/NV_PACA + 1*NV_IDF/NV_HDF + 0.3*NV_IDF/NV_OCC + 0.5*NV_IDF/NV_NA)/4
    journee=(1.5*NV_IDF/NV_PACA + 2*NV_IDF/NV_HDF + 0.6*NV_IDF/NV_OCC + 1*NV_IDF/NV_NA)/4
    semaine=(7*NV_IDF/NV_PACA + 8*NV_IDF/NV_HDF + 4*NV_IDF/NV_OCC+6*NV_IDF/NV_NA)/4
    
    #On doit approximer le nombre de carte de résident par arrondissement
    r_by_arr=ratio_by_arr()
    revenu=0
    revenu+=60*n_carte_resident*sum(r_by_arr[0:4])
    revenu+=50*n_carte_resident*sum(r_by_arr[4:11])
    revenu+=40*n_carte_resident*sum(r_by_arr[11:])
    revenu_carte=revenu
    print(revenu)
    
    a1 = df.loc[(df['duration_hours'] < 10)]
    a2 = df.loc[(df['duration_hours'] == 10)]
    a3=df.loc[(df['duration_hours'] > 10)]
    
    revenu += len(a1)*dem_journee + len(a2)*journee + len(a3)*semaine
    
    print(revenu)
    
    
    #Maintenant on augmente le prix par vignette
    #On augmente le prix pour chaque vignette de (n°vignette/5)
    revenu_by_vignette=[revenu*0.24/100, revenu*18/100, revenu*43/100, revenu*27/100, revenu*8.75/100, revenu*1.9/100]
    
    for i in range(len(revenu_by_vignette)):
        revenu_by_vignette[i]*=1+i/5
        
    
    
    
    
    return sum(revenu_by_vignette)
    
    
def revenu_paris_2018():
    #Abonnement à 45€/an
    #1.5€/journée type a1
    #9€/semaine type a2
    
    a1 = df.loc[(df['duration_hours'] <= 10)]
    a2 = df.loc[(df['duration_hours'] > 10)]
    print('a1: '+str(len(a1)))
    print('a2: '+str(len(a2)))
    print('a1+a2: '+str(len(a2)+len(a1)))
    
    revenu = len(a1)*1.5 + len(a2)*9 + n_carte_resident*45
    return revenu
    
        
    
