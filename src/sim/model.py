import random

from geopy import distance

from agents.car import *
from agents.station import StationAgent
from agents.stop import StopAgent

funcs = [new_tesla_model_s,
         new_tesla_model_3,
         new_tesla_model_y,
         new_chevrolet_bolt,
         new_mustang_mach_e,
         new_renault_zoe]

# funcs = [new_renault_twizy]

with open("../../files/step2.json", "r") as read_file:
    stop_points = json.load(read_file)

left = 1000
right = -1000
top = -1000
bottom = 1000

for idx in stop_points:
    point = stop_points[idx]
    if point[0] < bottom:
        bottom = point[0]
    if point[0] > top:
        top = point[0]
    if point[1] < left:
        left = point[1]
    if point[1] > right:
        right = point[1]


# print((right - left), (top - bottom))


class Model():
    """A model with some number of agents."""

    def __init__(self, cars, stations, width, height):
        self.num_agents = cars + stations + len(stop_points)
        self.schedule = []
        # self.grid = mesa.space.MultiGrid(width, height, True)
        # self.schedule = mesa.time.RandomActivation(self)
        self.cars_list = list()
        self.stations_list = list()
        self.stop_points = stop_points
        # Create agents
        self.w = width
        self.h = height
        ids = self.setup_cars(cars)

        # for i in range(stations):
        ids = self.setup_stations(ids)

        # self.setup_stops(ids)

        self.finished = set()
        self.trafficPerStation = {}
        self.stepCount = 0

    def setup_stops(self, ids):
        for i in stop_points:
            a = StopAgent(ids, self)
            x = max(int((stop_points[i][1] - left) / abs(left - right) * self.w) - 1, 0)
            y = max(int((stop_points[i][0] - bottom) / abs(bottom - top) * self.h) - 1, 0)
            self.grid.place_agent(a, (x, y))
            ids += 1
        return ids

    def setup_stations(self, ids):
        with open("../../files/centroids.json", "r") as read_file:
            stations = json.load(read_file)
            for station in stations:
                a = StationAgent(ids, self, 2, 250, stations[station])
                self.schedule.append(a)
                x = max(int((stations[station][1] - left) / abs(left - right) * self.w) - 1, 0)
                y = max(int((stations[station][0] - bottom) / abs(bottom - top) * self.h) - 2, 0)
                # print(x, y)
                # self.grid.place_agent(a, (x, y))
                self.stations_list.append(a)
                ids += 1

        return ids

    def has_finished(self, uid):
        self.finished.add(uid)

    def setup_cars(self, cars):
        for i in range(cars):
            a = random.choice(funcs)(i, self, random.randint(50, 100) / 100.0)
            idxs = random.sample(list(stop_points), 100)
            path = [p for p in idxs]
            a.set_path(path)
            # a.set_path([
            #     "187",
            #     "148",
            #     "462",
            #     "5",
            #     "406",
            #     "202",
            #     "221",
            #     "471",
            #     "119",
            #     "418",
            #     "284",
            #     "248",
            #     "460",
            #     "222",
            #     "205",
            #     "364",
            #     "230",
            #     "482",
            #     "203",
            #     "496",
            #     "154",
            #     "149",
            #     "214",
            #     "109",
            #     "403",
            #     "363",
            #     "313",
            #     "84",
            #     "27",
            #     "376",
            #     "74",
            #     "348",
            #     "268",
            #     "62",
            #     "116",
            #     "309",
            #     "44",
            #     "310",
            #     "361",
            #     "326",
            #     "121",
            #     "487",
            #     "194",
            #     "453",
            #     "219",
            #     "342",
            #     "133",
            #     "47",
            #     "295",
            #     "20",
            #     "492",
            #     "45",
            #     "352",
            #     "493",
            #     "290",
            #     "13",
            #     "220",
            #     "198",
            #     "279",
            #     "243",
            #     "227",
            #     "252",
            #     "343",
            #     "48",
            #     "332",
            #     "432",
            #     "162",
            #     "124",
            #     "201",
            #     "388",
            #     "153",
            #     "213",
            #     "334",
            #     "125",
            #     "10",
            #     "374",
            #     "481",
            #     "360",
            #     "137",
            #     "365",
            #     "0",
            #     "358",
            #     "422",
            #     "483",
            #     "132",
            #     "306",
            #     "338",
            #     "171",
            #     "98",
            #     "245",
            #     "409",
            #     "112",
            #     "271",
            #     "228",
            #     "454",
            #     "382",
            #     "328",
            #     "17",
            #     "448",
            #     "317"
            # ])
            self.schedule.append(a)
            self.cars_list.append(a)

            # x, y = self.rand_point()
            # self.grid.place_agent(a, (x, y))
        return cars

    def closest_charge(self, coords):
        closest = 10000000
        st = None
        for station in self.stations_list:
            dist = distance.geodesic(coords, station.coords).km
            if dist < closest:
                st = station
                closest = dist
        return st, closest

    def closest_charger_with_initial_point(self, coords1, coords2, car):
        # if (coords1[0] == -22.887983194586603 and coords2[0] == -22.795666862537107) or (
        #         (coords2[0] == -22.887983194586603 and coords1[0] == -22.795666862537107)):
        #     print("okk")
        closest = 1000000000000
        st = None
        out_dist1 = 1000000000
        for station in self.stations_list:
            dist1 = distance.geodesic(coords1, station.coords).km
            dist2 = distance.geodesic(station.coords, coords2).km
            if dist1 > (car.battery_energy / car.average_consume_per_100_km * 100) or dist2 > (
                    car.max_battery / car.average_consume_per_100_km * 100):
                continue
            if dist1 + dist2 < closest:
                st = station
                closest = dist1 + dist2
                out_dist1 = dist1
        if st is None:
            for station in self.stations_list:
                dist1 = distance.geodesic(coords1, station.coords).km
                dist2 = distance.geodesic(station.coords, coords2).km
                if dist1 > (car.battery_energy / car.average_consume_per_100_km * 100):
                    continue
                if dist1 + dist2 < closest:
                    st = station
                    closest = dist1 + dist2
                    out_dist1 = dist1
        return st, out_dist1

    def step(self):
        self.trafficPerStation[self.stepCount] = {}
        for station in self.stations_list:
            if station.unique_id in self.trafficPerStation[self.stepCount].keys():
                self.trafficPerStation[self.stepCount][station.unique_id] += 1
            else:
                self.trafficPerStation[self.stepCount][station.unique_id] = 1
        for car in self.cars_list:
            if car.needToCharge:
                if car.dist_to_next <= 2.0:
                    if car.closestStation.unique_id in self.trafficPerStation[self.stepCount].keys():
                        self.trafficPerStation[self.stepCount][car.closestStation.unique_id] += 1
                    else:
                        self.trafficPerStation[self.stepCount][car.closestStation.unique_id] = 1

        self.stepCount += 1
        for agent in self.schedule:
            agent.step()

    def rand_point(self):
        p = random.choice(list(self.stop_points))
        p = self.stop_points[p]
        x = max(int((p[1] - left) / abs(left - right) * self.w) - 1, 0)
        y = max(int((p[0] - bottom) / abs(bottom - top) * self.h) - 1, 0)
        return x, y

    def get_stop_coords(self, p):
        return self.stop_points[p]

    def get_dist(self, p1, p2):
        coords_1 = p1
        coords_2 = self.stop_points[p2]
        return distance.geodesic(coords_1, coords_2).km
