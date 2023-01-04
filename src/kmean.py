import math
import numpy as np
import pandas as pd
import osmnx as ox
import networkx as nx
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import json
import requests

with open('../files/step2.json', 'r') as f:
  data = json.load(f)

def api_setup(data):
    url = 'http://localhost:8001/setup'

    x = requests.post(url, json = data)

    print(x.status_code)


def convert_to_dict(data):
    '''
    Util function to converte an array to a dictionary
    `data`: dataset in array format
    '''
    result = {}

    for arr in range(len(data)):
        result["{0}".format(arr)] = data[arr].tolist()

    return result

def initialize_centroids(k, data):
    '''
    Initialize k centroids randomly within the range of the data itself
    `k`: number of clusters
    `data`: dataset in dictionary format
    '''
    
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

    return json.dumps(convert_to_dict(centroids))

def calculate_distances(centroids):

    '''
    Calculates the Distance between each centroid to all points in data .
    `centroid`: coordinates of each centroid in dictionary format
    `data`: dataset in dictionary format
    '''

    url = "http://localhost:8001/distances"

    payload = centroids

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text) 

def centroid_assignation(data, centroids):
    '''
    Given a dataframe `data` and a set of `centroids`, we assign each data point in `data` to a centroid. 
    `data`: dataset in dictionary format
    `centroids`: coordinates of each centroid in dictionary format
    '''
    assignation = {}

    # Calculate distances between each point to each centroid
    osm_distances = calculate_distances(centroids) 

    print('OSM:')
    print(osm_distances)

    distances = osm_distances.get("distances")

    print('Distances:')
    print(distances)

    for key in data.keys(): # for each point
        min_value = float('inf') 
        min_key = int
        for centrois_key, outer_dict in distances.items(): # for each centroid, where outer_dict corresponds to an dictionary (point, distance)
            value = float(outer_dict[key])
            if value < min_value:
                min_value = value
                min_key = centrois_key

        # assignation[key] = [min_key, min_value] # each point is assigned an array with the closest cluster identifier and its respective distance
        assignation[key] = min_key
    
    print('Centroids:')
    print(centroids)
    print('Assignation:')
    print(assignation)

    return assignation

def recalculate_centroids(assignation, data, n_clusters):
    centroids = {}
    for i in range(n_clusters):
        cluster = [k for k, v in assignation.items() if int(v) == i] # get the assignation points in cluster i

        # Extract the coordinates from the data dictionary that belong to the cluster
        coords = [data[key] for key in cluster]

        # Calculate the mean values of the coordinates
        mean_coords = np.mean(coords, axis=0)

        centroids[i] = mean_coords.tolist()

    return centroids

def calculate_error(data1, data2):
    # Calculate the error
    error = 0
    for key in data1.keys():
        error += np.mean((data1[key] - data2[key])**2)

    return error

def kmeans(dset, k):
    '''
    K-means implementationd 
    `dset`:  DataFrame with observations
    `k`: number of clusters
    '''

    working_dset = dset.copy()

    goahead = True # stopping flag
    j = 0 # counter for the iterations
    
    # Defining centroids 
    centroids = initialize_centroids(k, working_dset)

    while(goahead):

        # Assign centroids and calculate distances
        assigned_data = centroid_assignation(working_dset, centroids) 
        
        # Update centroids position
        new_centroids = recalculate_centroids(assigned_data, data, k)

        # Restart the iteration
        if j>0:
            # If centroids position already converged (position does't change re-alocate anymore)
            # if calculate_error(new_centroids, centroids) > 0.5:
            if j > 6:
                print(calculate_error(new_centroids, centroids) > 0.5)
                goahead = False
        j+=1

        centroids = new_centroids

    # Assign centroids and calculate distances
    assigned_data = centroid_assignation(working_dset, centroids)

    # Update centroids position
    centroids = recalculate_centroids(assigned_data, data, k)

    return assigned_data, centroids

# api_setup(data)

assigned_data, centroids = kmeans(data, 3)