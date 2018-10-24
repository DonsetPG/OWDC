import numpy as np
import matplotlib.pyplot as plt

path="C:/Users/Arthur/Google Drive/Projets/Autres/OliverWyman/Data/"

df=np.load(path+"parking_counts.npy")

#Le but est de faire un graphe par jour sur les moyennes (sur tous les parkings) des occupations par heure (moyenné sur l'année 2014)

#Les données pour chaque jours toutes les 5 min de 9h à 20h55
#(20*60+55-9*60)/5 = 143, donc 144 données par jour
#Soit 144*7=1008 données par semaine (donc par parking)

data_per_day = 144
data_per_week = 1008

n_parkmeter=int(len(df)/1008)

#Retourne un tableau de 7 tableaux (pour chaque jour de la semaine) et chaque tableau interne contenant 144 données pour le parkmeter n
def week_for(n):
    i=0
    while df[i][0]!=n:
        i+=data_per_week
    if(i>len(df)):
        print("Parkmeter not found")
        return []
    parkmeter=[]
    for j in range(1,8):
        day=[]
        for k in range(i+j*data_per_day):
            day.append(df[k][-1])
        parkmeter.append(day)
    return parkmeter
    

#Retourne un tableau de 7 tableaux de 144 élements correspondants à la moyenne sur ce moment pour les p premiers parkings

def avg_count(p):

    avg=[[0 for k in range(data_per_day)] for j in range(7)]
    for park in range(p):
        for day in range(7):
            for time in range(data_per_day):
                avg[day][time]+=df[park*data_per_week + day*data_per_day + time][-1]
    for i in range(len(avg)):
        for j in range(len(avg[i])):
            avg[i][j]=avg[i][j]/p
    return avg
    
def avg_total():

    return avg_count(n_parkmeter)

#Le graphe voulu
def graph_total():
    avg=avg_total()
    for i in range(len(avg)):
        avg[i]=avg[i][1:133]
    days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    hours=list(range(9*60, 21*60, 5))
    hours=["" for k in range(144)]
    hours=hours[1:133]
    #hours[0]="9:00"
    #hours[72]="15:00"
    #hours[-1]="20:55"
    hours[0]="9:05"
    hours[72]="15:05"
    hours[-1]="20:00"
    """
    for i in range(len(hours)):
        if(i%48==0):
            if(hours[i]%60>=10):
                hours[i]=str(hours[i]//60)+":"+str(hours[i]%60)
            else:
                hours[i]=str(hours[i]//60)+":0"+str(hours[i]%60)
        else:
            hours[i]=""
    """
    
    plt.figure(1, figsize=(len(avg)*len(avg[0]), len(avg)))
    
    for i in range(len(avg)):
        plt.subplot(170+i+1)
        x=list(range(len(avg[i])))
        plt.subplots_adjust(wspace = 0.4)
        plt.ylim(125,300)
        plt.xticks(x, hours)
        plt.tick_params(axis='x', bottom=False)
        plt.plot(x,avg[i])
        plt.title(days[i])
        
    plt.suptitle('Average count of all parkmeters in a week')
    plt.show()
    

             

