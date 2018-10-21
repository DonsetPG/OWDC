#===>

#Path: /parking_counts/axis0
#Shape: (1,)
#Data type: |S5
#Path: /parking_counts/axis1_label0
#Shape: (7867440,)
#Data type: int16
#Path: /parking_counts/axis1_label1
#Shape: (7867440,)
#Data type: int8
#Path: /parking_counts/axis1_label2
#Shape: (7867440,)
#Data type: int8
#Path: /parking_counts/axis1_label3
#Shape: (7867440,)
#Data type: int8
#Path: /parking_counts/axis1_level0
#Shape: (7805,)
#Data type: int64
#Path: /parking_counts/axis1_level1
#Shape: (7,)
#Data type: |S9
#Path: /parking_counts/axis1_level2
#Shape: (12,)
#Data type: int64
#Path: /parking_counts/axis1_level3
#Shape: (12,)
#Data type: int64
#Path: /parking_counts/block0_items
#Shape: (1,)
#Data type: |S5
#Path: /parking_counts/block0_values
#Shape: (7867440, 1)
#Data type: int64

###

#Path: /parkmeters_zones_12_12/axis0
#Shape: (2,)
#Data type: |S12
#Path: /parkmeters_zones_12_12/axis1
#Shape: (7810,)
#Data type: int64
#Path: /parkmeters_zones_12_12/block0_items
#Shape: (1,)
#Data type: |S12
#Path: /parkmeters_zones_12_12/block0_values
#Shape: (7810, 1)
#Data type: int64
#Path: /parkmeters_zones_12_12/block1_items
#Shape: (1,)
#Data type: |S4
#Path: /parkmeters_zones_12_12/block1_values
#Shape: (1,)
#Data type: object

###


#Path: /transaction_and_locations/axis0
#Shape: (13,)
#Data type: |S21
#Path: /transaction_and_locations/axis1
#Shape: (24251633,)
#Data type: int64
#Path: /transaction_and_locations/block0_items
#Shape: (2,)
#Data type: |S13
#Path: /transaction_and_locations/block0_values
#Shape: (24251633, 2)
#Data type: int64
#Path: /transaction_and_locations/block1_items
#Shape: (3,)
#Data type: |S14
#Path: /transaction_and_locations/block1_values
#Shape: (24251633, 3)
#Data type: float64
#Path: /transaction_and_locations/block2_items
#Shape: (2,)
#Data type: |S14
#Path: /transaction_and_locations/block2_values
#Shape: (24251633, 2)
#Data type: int64
#Path: /transaction_and_locations/block3_items
#Shape: (6,)
#Data type: |S21
#Path: /transaction_and_locations/block3_values
#Shape: (1,)
#Data type: object

########


import pandas as pd
import h5py
import matplotlib
import matplotlib.pyplot as plt

data_case_storage='/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/stored_data_case.h5'

f = h5py.File(data_case_storage, 'r')


print(list(f.keys()))

# ===> ['parking_counts', 'parkmeters_zones_12_12', 'transaction_and_locations'] 

dts_p_c = f['parking_counts']

#

dts_p_c_a0 = f['/parking_counts/axis0']
dts_p_c_al0 = f['/parking_counts/axis1_label0']
dts_p_c_al1 = f['/parking_counts/axis1_label1']
dts_p_c_al2 = f['/parking_counts/axis1_label2']
dts_p_c_al3 = f['/parking_counts/axis1_label3']
dts_p_c_alvl0 = f['/parking_counts/axis1_level0']
dts_p_c_alvl1 = f['/parking_counts/axis1_level1']
dts_p_c_alvl2 = f['/parking_counts/axis1_level2']
dts_p_c_alvl3 = f['/parking_counts/axis1_level3']
dts_p_c_bi0 = f['/parking_counts/block0_items']
dts_p_c_bv0 = f['/parking_counts/block0_values']

###

dts_p_z = f['parkmeters_zones_12_12']

#

dts_p_z_a0 = f['/parkmeters_zones_12_12/axis0']
dts_p_z_a1 = f['/parkmeters_zones_12_12/axis1']
dts_p_z_bi0 = f['/parkmeters_zones_12_12/block0_items']
dts_p_z_bv0 = f['/parkmeters_zones_12_12/block0_values']
dts_p_z_bi1 = f['/parkmeters_zones_12_12/block1_items']
dts_p_z_bv1 = f['/parkmeters_zones_12_12/block1_values']

###

dts_t_l = f['transaction_and_locations']

#

dts_t_l_a0 = f['/transaction_and_locations/axis0']
dts_t_l_a1 = f['/transaction_and_locations/axis1']
dts_p_z_bi0 = f['/transaction_and_locations/block0_items']
dts_p_z_bv0 = f['/transaction_and_locations/block0_values']
dts_p_z_bi1 = f['/transaction_and_locations/block1_items']
dts_p_z_bv1 = f['/transaction_and_locations/block1_values']
dts_p_z_bi2 = f['/transaction_and_locations/block2_items']
dts_p_z_bv2 = f['/transaction_and_locations/block2_values']
dts_p_z_bi3 = f['/transaction_and_locations/block3_items']
dts_p_z_bv3 = f['/transaction_and_locations/block3_values']


####### 


def traverse_datasets(hdf_file):

    def h5py_dataset_iterator(g, prefix=''):
        for key in g.keys():
            item = g[key]
            path = f'{prefix}/{key}'
            if isinstance(item, h5py.Dataset): # test for dataset
                yield (path, item)
            elif isinstance(item, h5py.Group): # test for group (go down)
                yield from h5py_dataset_iterator(item, path)

    with h5py.File(hdf_file, 'r') as f:
        for path, _ in h5py_dataset_iterator(f):
            yield path

def plotImage(arr) :
    fig  = plt.figure(figsize=(5,5), dpi=80, facecolor='w',edgecolor='w',frameon=True)
    imAx = plt.imshow(arr, origin='lower', interpolation='nearest')
    fig.colorbar(imAx, pad=0.01, fraction=0.1, shrink=1.00, aspect=20)
 
def plotHistogram(arr) :
    fig  = plt.figure(figsize=(5,5), dpi=80, facecolor='w',edgecolor='w',frameon=True)
    plt.hist(arr.flatten(), bins=100)


def read_HDF_file(file_name, table):
    with pd.HDFStore(file_name, complevel=9, complib='blosc') as store:
         return store[table]

for dset in traverse_datasets(data_case_storage):
    #print('Path:', dset)
    #print('Shape:', f[dset].shape)
    #print('Data type:', f[dset].dtype)
    print(f[dset])
    




