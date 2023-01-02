import json
import sys
from os import listdir
from os.path import exists

path = sys.argv[1]

# if(exists("files/step1.json")):
# with open("files/step1.json", "r") as read_file:
#    points = json.load(read_file)
#    print(len(points))
# print(points)
# else:
if not exists("files/step1.json"):
    files = listdir(path)
    points = []
    for file in files:
        with open(path + "/" + file, "r") as read_file:
            data = json.load(read_file)
            for point in data["deliveries"]:
                points.append((point["point"]["lat"], point["point"]["lng"]))

    # print(len(points))
    points = json.dumps(points)
    with open("files/step1.json", "w") as write_file:
        write_file.write(points)
    # print(points)
