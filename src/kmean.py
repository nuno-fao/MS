import json

import numpy as np
import requests

with open('../files/step2.json', 'r') as f:
    data = json.load(f)


def api_setup(data):
    url = 'http://localhost:8001/setup'

    x = requests.post(url, json=data)

    # print(x.status_code)


def convert_to_dict(data):
    '''
    Util function to converte an array to a dictionary
    `data`: dataset in array format
    '''
    result = {}

    for arr in range(len(data)):
        result["{0}".format(arr)] = data[arr].tolist()

    return result


def initialize_centroids_random(k, data):
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

    return convert_to_dict(centroids)


def initialize_centroids(w, h, stations, data):
    min_coords = [float('inf'), float('inf')]
    max_coords = [float('-inf'), float('-inf')]

    # Find the minimum and maximum values for each coordinate
    for row in data.values():
        for i, coord in enumerate(row):
            if coord < min_coords[i]:
                min_coords[i] = coord
            if coord > max_coords[i]:
                max_coords[i] = coord

    x_size = (max_coords[1] - min_coords[1]) / w
    y_size = (max_coords[0] - min_coords[0]) / h

    matrix = []

    print(min_coords, max_coords)
    for y in range(h):
        matrix.append([])
        for x in range(w):
            matrix[y].append(0)
    print(matrix)
    for y in range(h):
        for x in range(w):
            for p in data:
                if check_if_in((min_coords[0] + y * y_size, min_coords[1] + x * x_size),
                               (min_coords[0] + (y + 1) * y_size, min_coords[1] + (x + 1) * x_size), data[p]):
                    matrix[y][x] += 1
    print(matrix)

    numbers = []
    for y in range(h):
        for x in range(w):
            for d in range(stations):
                numbers.append((matrix[y][x] / (d + 1), (x, y)))

    numbers.sort(reverse=True, key=order_districts)

    stations_allocation = []
    for y in range(h):
        stations_allocation.append([])
        for x in range(w):
            stations_allocation[y].append(0)

    for v in range(stations):
        v = numbers[v]
        stations_allocation[v[1][1]][v[1][0]] += 1
    print(stations_allocation)

    # Initialize k centroids randomly within the range of the data
    # centroids = np.random.uniform(low=min_coords, high=max_coords, size=(k, len(min_coords)))

    centroids = []
    print()
    for y in range(h):
        for x in range(w):
            tmp_centroids = np.random.uniform(low=(min_coords[0] + y * y_size, min_coords[1] + x * x_size),
                                              high=(min_coords[0] + (y + 1) * y_size, min_coords[1] + (x + 1) * x_size),
                                              size=(stations_allocation[y][x], len(min_coords)))
            centroids += tmp_centroids.tolist()

    result = {}

    for arr in range(len(centroids)):
        result["{0}".format(arr)] = centroids[arr]
    return result


def order_districts(e):
    return e[0]


def check_if_in(min, max, point):
    # print(min)
    # print(max)
    # print(point)
    # print()
    return min[0] <= point[0] <= max[0] and min[1] <= point[1] <= max[1]


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

    response = requests.request("POST", url, headers=headers, json=payload)

    # print(response.text)

    return json.loads(response.text)


def centroid_assignation(data, centroids):
    '''
    Given a dataframe `data` and a set of `centroids`, we assign each data point in `data` to a centroid. 
    `data`: dataset in dictionary format
    `centroids`: coordinates of each centroid in dictionary format
    '''
    assignation = {}

    # print("")
    # print("--------------------------------------------------------------------------------------------------")
    # print(data)
    # print(centroids)

    # Calculate distances between each point to each centroid
    osm_distances = calculate_distances(centroids)

    # print('OSM:')
    # print(osm_distances)

    distances = osm_distances.get("distances")

    # print('Distances:')
    # print(distances)

    for key in data.keys():  # for each point
        min_value = float('inf')
        min_key = int
        for centrois_key, outer_dict in distances.items():  # for each centroid, where outer_dict corresponds to an dictionary (point, distance)
            value = float(outer_dict[key])
            if value < min_value:
                min_value = value
                min_key = centrois_key

        # assignation[key] = [min_key, min_value] # each point is assigned an array with the closest cluster identifier and its respective distance
        assignation[key] = min_key

    sum = 0
    count = 0
    for c in centroids:
        for p in distances[c]:
            count += 1
            sum += distances[c][p]
    print("Mean Distance")
    print(sum / count)

    # print('Centroids:')
    # print(centroids)
    # print('Assignation:')
    # print(assignation)

    return assignation


def recalculate_centroids(assignation, data, n_clusters, old_centroids):
    centroids = {}
    for i in range(n_clusters):
        cluster = [k for k, v in assignation.items() if int(v) == i]  # get the assignation points in cluster i

        if len(cluster) == 0:
            centroids[i] = old_centroids[str(i)]
            continue

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
        error += np.mean((data1[key] - data2[key]) ** 2)

    return error


def kmeans(dset, k):
    '''
    K-means implementationd 
    `dset`:  DataFrame with observations
    `k`: number of clusters
    '''

    working_dset = dset.copy()

    goahead = True  # stopping flag
    j = 0  # counter for the iterations

    # Defining centroids 
    # centroids = initialize_centroids_random(k, working_dset)
    centroids = initialize_centroids(3, 2, k, working_dset)

    while (goahead):

        # Assign centroids and calculate distances
        assigned_data = centroid_assignation(working_dset, centroids)

        # Update centroids position
        new_centroids = recalculate_centroids(assigned_data, data, k, centroids)
        print()

        # Restart the iteration
        if j > 0:
            # If centroids position already converged (position does't change re-alocate anymore)
            # if calculate_error(new_centroids, centroids) > 0.5:
            if j > 6:
                # print(calculate_error(new_centroids, centroids) > 0.5)
                goahead = False
        j += 1

        centroids = {}
        # print("Centroids")
        # print(new_centroids.keys())
        for n_k in new_centroids:
            centroids[str(n_k)] = new_centroids[n_k]

    # Assign centroids and calculate distances
    assigned_data = centroid_assignation(working_dset, centroids)

    # Update centroids position
    centroids = recalculate_centroids(assigned_data, data, k, centroids)

    return assigned_data, centroids


# api_setup(data)

assigned_data, centroids = kmeans(data, 20)
