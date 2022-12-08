import random 
import json 
import sys 

with open("files/step1.json", "r") as read_file:
        points = json.load(read_file)

        bLat = -1000
        bLng = -1000
        sLat = 1000
        sLng = 1000
        for p in points:
            if p[0] > bLat:
                bLat = p[0]
            if p[0] < sLat:
                sLat = p[0]
            if p[1] > bLng:
                bLng = p[1]
            if p[1] < sLng:
                sLng = p[1]
        print(bLat,sLng,sLat,bLng)

        points = json.dumps(random.sample(points, int(sys.argv[1])))
        with open("files/step2.json", "w") as write_file:
            write_file.write(points)


