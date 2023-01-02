import json
from csv import DictReader
import geopy.distance


with open('files/edges.csv', 'r') as edges_obj:
    # pass the file object to DictReader() to get the DictReader object
    dict_reader = DictReader(edges_obj)
    # get a list of dictionaries from dct_reader
    list_of_dict = list(dict_reader)
    # print list of dict i.e. rows
    edges = list_of_dict

with open('files/nodes.csv', 'r') as edges_obj:
    # pass the file object to DictReader() to get the DictReader object
    dict_reader = DictReader(edges_obj)
    # get a list of dictionaries from dct_reader
    list_of_dict = list(dict_reader)
    # print list of dict i.e. rows
    nodes = list_of_dict

f = open('files/step3.json')
distances = json.load(f)

n_nodes = {}

for node in nodes:
    n_nodes[node["Code"]] = node

nodes = n_nodes

distance = 10000000
point = ""

find_points = [(-22.958356300000002,-43.265045300000004)]

for p in find_points:
    for node in nodes:
        node = nodes[node]
        if geopy.distance.geodesic(p, (float(node["Latitude"]),float(node["Longitude"]))).km < distance:
            point = node["Code"]

print(distance,point)


