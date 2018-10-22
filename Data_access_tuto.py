
## This is a tutorial for reading the data 
print("This is a basic tutorial for reading the data")


## Step 1
## This import pandas functions and library, useful to read and manipulate hd5 format data
## Pandas library will be used in next fonction (see pd. prefix)
import pandas as pd
import h5py
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt

CONST = 1000000

print("panda imported : OK ")

## Step 2
## Putting the path of the data file into a variable (more convenient for next steps)
## Replace the path below by the path of your personal computer (where you stored the data) 
## Note: '\' won't be recognised on Windows computers, use '//' instead
data_case_storage='/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/stored_data_case.h5'

print("data imported : OK ")

## Step 3
## Definition of a function listing all tables in the datafile
def list_HDF_file(file_name):
     with pd.HDFStore(file_name, complevel=9, complib='blosc') as store:
             result = store.keys()   
     return result

## Calling example
print(list_HDF_file(data_case_storage))


## Step 4
## Definition of a function reading a table 
def read_HDF_file(file_name, table,i):
    with pd.HDFStore(file_name, complevel=9, complib='blosc') as store:
         dts = store[table]
         print(dts.shape)
         tab = np.array(dts[i*CONST:(i+1)*CONST])
         return dts,tab

## Calling example: printing the full table /transactions_and_locations(column labels and data) 


def main():
        print("Starting to process...")
        for i in range(0,24):
                save_name = "/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/t_and_l_full"+"_"+str(i)
                print("Saving dataset from ",i," millions to ",(i+1)," millions ...")
                df,df_array = read_HDF_file(data_case_storage,"/transaction_and_locations",i)
                np.save(save_name,df_array)
                print("saved")

main()

#df,df_array=read_HDF_file(data_case_storage,"/transaction_and_locations")

#np.save("/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/t_and_l_full",df_array)

# Printing only the top 10 rows
#print(df.head(2))




## Step 5
## A few select / calculations on the data
#5.1 Select of distinct values for column system
#df.system.drop_duplicates()

#5.2 Select of total sales
#df.amount.sum()

#5.3 Select of total sales per group
#df.groupby(['user_type'])['amount'].sum()


## Step 6
## Your turn to play!
## Remember: the internet is full of resources to learn you everything you need to crack that case! 
## Good luck!



