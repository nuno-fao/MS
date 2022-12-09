import json
from geopy import distance

distances = {}
ps = {}
with open("files/step2.json", "r") as read_file:
    points = json.load(read_file)
    i = 0
    for point in points:
        ps[str(point[0]) + "_" + str(point[1])] = i
        distances[i] = {}
        i += 1

    i = 0
    for point in points:
        i += 1
        current_point = ps[str(point[0]) + "_" + str(point[1])]
        print(current_point)
        for op in points[i:]:
            other_point = ps[str(op[0]) + "_" + str(op[1])]
            a = (point[0], point[1])
            b = (op[0], op[1])
            d = distance.distance(a, b).km
            distances[current_point][other_point] = d
            #distances[other_point][current_point] = d

    print(distances)

    with open("files/step3.json", "w") as write_file:
        write_file.write(json.dumps(distances))
