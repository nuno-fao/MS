from geopy import distance

from agents.car import *
from agents.station import StationAgent
from agents.stop import StopAgent

# funcs = [new_tesla_model_s,
#          new_tesla_model_3,
#          new_tesla_model_y,
#          new_chevrolet_bolt,
#          new_mustang_mach_e,
#          new_renault_twizy,
#          new_renault_zoe]

funcs = [new_renault_twizy]

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


class Model(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, cars, stations, width, height):
        self.num_agents = cars + stations + len(stop_points)
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
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
                self.schedule.add(a)
                x = max(int((stations[station][1] - left) / abs(left - right) * self.w) - 1, 0)
                y = max(int((stations[station][0] - bottom) / abs(bottom - top) * self.h) - 2, 0)
                # print(x, y)
                self.grid.place_agent(a, (x, y))
                self.stations_list.append(a)
                ids += 1

        return ids

    def has_finished(self, uid):
        self.finished.add(uid)

    def setup_cars(self, cars):
        for i in range(cars):
            a = self.random.choice(funcs)(i, self, self.random.randint(50, 100) / 100.0)
            idxs = self.random.sample(list(stop_points), 100)
            path = [p for p in idxs]
            a.set_path(path)
            self.schedule.add(a)
            self.cars_list.append(a)

            x, y = self.rand_point()
            self.grid.place_agent(a, (x, y))
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
        closest = 1000000000000
        st = None
        for station in self.stations_list:
            dist1 = distance.geodesic(coords1, station.coords).km
            dist2 = distance.geodesic(station.coords, coords2).km
            if dist1 > car.battery_energy / car.average_consume_per_100_km * 100 or dist2 > car.max_battery / car.average_consume_per_100_km * 100:
                continue
            if dist1 + dist2 < closest:
                st = station
                closest = dist1 + dist2
        if st is None:
            for station in self.stations_list:
                dist1 = distance.geodesic(coords1, station.coords).km
                dist2 = distance.geodesic(station.coords, coords2).km
                if dist1 > car.battery_energy / car.average_consume_per_100_km * 100:
                    continue
                if dist1 + dist2 < closest:
                    st = station
                    closest = dist1 + dist2
        return st, closest

    def step(self):
        self.schedule.step()

    def rand_point(self):
        p = self.random.choice(list(self.stop_points))
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
