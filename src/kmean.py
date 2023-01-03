import math
import numpy as np
import pandas as pd
import osmnx as ox
import networkx as nx
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import json

with open('../files/step2.json', 'r') as f:
  data = json.load(f)

def convert_to_array(data):
    result = []

    for key in data:
        result.append([data[key][0], data[key][1]])

    return result

def convert_to_dict(data):
    result = {}

    for arr in range(len(data)):
        result["{0}".format(arr)] = data[arr]

    return result

def initialize_centroids(k, data):
    '''
    Initialize k centroids randomly within the range of the data itself
    '''
    # Initialize min_coords and max_coords to very large and small values, respectively
    min_coords = [float('inf'), float('inf')]
    max_coords = [float('-inf'), float('-inf')]

    # Find the minimum and maximum values for each coordinate
    for row in data.values():
        for i, coord in enumerate(row):
            if coord < min_coords[i]:
                min_coords[i] = coord
            if coord > max_coords[i]:
                max_coords[i] = coord

    # Initialize k centroids randomly within the range of the data
    centroids = np.random.uniform(low=min_coords, high=max_coords, size=(k, len(min_coords)))
    return convert_to_dict(centroids)  # 3x2 array of random centroids

def calculate_distances(centroids, data):

    '''
    Calculates the Distance between each centroid to all points in data .
    `centroid`: coordinates of each centroid in dict format
    `data`: dataset in dict format
    '''

    result = {}

    return result 

def centroid_assignation(dset, centroids):
    '''
    Given a dataframe `dset` and a set of `centroids`, we assign each data point in `dset` to a centroid. 
    '''
    assignation = {}

    osm_distances = calculate_distances(centroids, dset)
    distances = osm_distances["distance"]

    for point in dset['distance']:

        min_value = float('inf')  # initialize min_value to a very large number
        min_key = int
        for key, outer_dict in distances.items():
            for key, value in outer_dict.items():
                value = float(value)  # convert value to a float
                if value < min_value:
                    min_value = value
                    min_key = key

        assignation[point] = [min_key, min_value] # para cada ponto guarda um array com o identificador do cluster mais perto e a sua distancia

    return assignation, osm_distances['converged']

def recalculate_centroids(data, n_clusters):
    centroids = {}
    for i in range(n_clusters):
        cluster = [k for k, v in data.items() if v == i] # get the data points in cluster i
        # cluster = data[labels == i]  # get the data points in cluster i
        centroids[i] = {}
        for j in range(cluster.shape[1]):
            centroids[i][j] = cluster[:, j].mean()  # calculate the mean of each column
    return centroids

def kmeans(dset, k=3):
    '''
    K-means implementationd for a 
    `dset`:  DataFrame with observations
    `k`: number of clusters, default k=3
    '''
    # Let us work in a copy, so we don't mess the original
    working_dset = dset.copy()

    # We define some variables to hold the error, the 
    # stopping signal and a counter for the iterations
    goahead = True
    j = 0
    
    # Step 2: Initiate clusters by defining centroids 
    centroids = initialize_centroids(k, working_dset)

    while(goahead):
        # Step 3 and 4 - Assign centroids and calculate error
        assigned_data, flag = centroid_assignation(working_dset, centroids) 
        
        # Step 5 - Update centroid position
        centroids = recalculate_centroids(assigned_data, k)

        # Step 6 - Restart the iteration
        if j>0:
            # Is the error less than a tolerance (1E-4)
            if flag:
                goahead = False
        j+=1

    assigned_data, flag = centroid_assignation(working_dset, centroids)
    centroids = recalculate_centroids(assigned_data, k)
    return assigned_data, centroids

# data['centroid'], data['error'], centroids =  kmeans(data, 3)
# data.head()
# print(data.sort_values(by=['centroid']))

# centroids = initialize_centroids(3, data)

print(initialize_centroids(3, data))
