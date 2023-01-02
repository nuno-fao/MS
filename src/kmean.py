import math
import numpy as np
import pandas as pd
import osmnx as ox
import networkx as nx
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

file_url = "../files/step2.json"
data = pd.read_json(file_url)

### Verify if streetnetwork.graphml file has been created
# if (not os.path.isfile('streetnetwork.graphml')):
#     area_graph = ox.graph_from_place('Rio de Janeiro, RJ, Brazil')
#     ox.save_graphml(area_graph, 'streetnetwork.graphml')
# else:
#     area_graph = ox.load_graphml('streetnetwork.graphml')


def initialize_centroids(k, data):
    '''
    Initialize k centroids randomly within the range of the data itself
    '''
    n_dims = data.shape[1]
    centroid_min = data.min().min()
    centroid_max = data.max().max()
    centroids = []

    for centroid in range(k):
        centroid = np.random.uniform(centroid_min, centroid_max, n_dims)
        centroids.append(centroid)

    centroids = pd.DataFrame(centroids, columns = data.columns)

    return centroids

centroids = initialize_centroids(3, data)
# print(centroids)

def calculate_error(a,b):
    '''
    Given two Numpy Arrays, calculates the root of the sum of squared errores.
    '''
    error = np.square(np.sum((a-b)**2))

    '''
    Given two Numpy Arrays, calculates the Distance between two coordinates.
    '''
    # distance = nx.shortest_path_length(area_graph, (data.iloc[0][0], data.iloc[0][1]), (centroids.iloc[0][0], centroids.iloc[0][1]), weight="length")

    return error 

for i, centroid in enumerate(range(centroids.shape[0])):
    err = calculate_error(centroids.iloc[centroid,:], data.iloc[36,:])
    print('Error for centroid {0}: {1:.2f}'.format(i, err))



def centroid_assignation(dset, centroids):
    '''
    Given a dataframe `dset` and a set of `centroids`, we assign each
    data point in `dset` to a centroid. 
    '''
    k = centroids.shape[0]
    n = dset.shape[0]
    assignation = []
    assign_errors = []

    for obs in range(n):
        # Estimate error
        all_errors = np.array([])
        for centroid in range(k):
            err = calculate_error(centroids.iloc[centroid, :], dset.iloc[obs,:])
            all_errors = np.append(all_errors, err)

        # Get the nearest centroid and the error
        nearest_centroid =  np.where(all_errors==np.amin(all_errors))[0].tolist()[0]
        nearest_centroid_error = np.amin(all_errors)

        # Add values to corresponding lists
        assignation.append(nearest_centroid)
        assign_errors.append(nearest_centroid_error)

    return assignation, assign_errors

### Add two columns to our data, one containing the centroid assigned and other the error incurred.
data['centroid'], data['error'] = centroid_assignation(data, centroids)
data.head()

def kmeans(dset, k=3, tol=1e-4):
    '''
    K-means implementationd for a 
    `dset`:  DataFrame with observations
    `k`: number of clusters, default k=2
    `tol`: tolerance=1E-4
    '''
    # Let us work in a copy, so we don't mess the original
    working_dset = data.copy()
    # We define some variables to hold the error, the 
    # stopping signal and a counter for the iterations
    err = []
    goahead = True
    j = 0
    
    # Step 2: Initiate clusters by defining centroids 
    centroids = initialize_centroids(k, dset)

    while(goahead):
        # Step 3 and 4 - Assign centroids and calculate error
        working_dset['centroid'], j_err = centroid_assignation(working_dset, centroids) 
        err.append(sum(j_err))
        
        # Step 5 - Update centroid position
        centroids = working_dset.groupby('centroid').agg('mean').reset_index(drop = True)

        # Step 6 - Restart the iteration
        if j>0:
            # Is the error less than a tolerance (1E-4)
            if err[j-1]-err[j]<=tol:
                goahead = False
        j+=1

    working_dset['centroid'], j_err = centroid_assignation(working_dset, centroids)
    centroids = working_dset.groupby('centroid').agg('mean').reset_index(drop = True)
    return working_dset['centroid'], j_err, centroids

data['centroid'], data['error'], centroids =  kmeans(data, 3)
data.head()
print(data.sort_values(by=['centroid']))