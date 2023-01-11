import json

from agents.station import StationAgent


class CarAgent():
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, battery_energy, max_battery, average_consume_per_100_km):
        self.unique_id = unique_id
        self.model = model
        self.path = None
        self.battery_energy = battery_energy  # battery in W.h
        self.max_battery = max_battery
        self.average_consume_per_100_km = average_consume_per_100_km
        self.km = 0.0
        self.is_moving = True
        self.is_charging = False
        self.is_preparing_charging = False
        self.charging_delay = 0
        self.charger = StationAgent
        self.dist_to_next = 0
        self.current_point = None
        self.needToCharge = False
        self.closestStation = None
        self.finished = False
        self.dist_per_minute = 8.3 / 1000 * 60
        self.consume_per_minute = self.dist_per_minute * self.average_consume_per_100_km / 100
        self.kmToCharge = 0.0
        self.logs = []

    def start_movement(self):
        self.is_moving = True

    def stop_movement(self):
        self.is_moving = False

    def charge(self, energy):
        self.battery_energy += energy

    def set_path(self, path):
        self.logs.append(path)
        self.path = path
        self.current_point = path[0]
        self.path = self.path[1:]
        self.model.get_real_distance(self.current_point, self.path[0])

    def go_charge(self, station):
        self.is_moving = False
        # self.is_preparing_charging = True
        self.is_charging = True
        self.charger = station
        self.charger.start_charge(self)

    def should_charge(self):
        next_point_distance = self.model.get_real_distance(self.current_point, self.path[0])
        if len(self.path) == 1 and next_point_distance <= self.battery_energy / self.average_consume_per_100_km * 100:
            return None, next_point_distance
        if len(self.path) == 0:
            return None, 0

        next_point = self.path[0]
        naive_charger, naive_dist = self.model.closest_charge(next_point)

        naive_distance = (next_point_distance + naive_dist) * 1.05

        if naive_distance > self.battery_energy / self.average_consume_per_100_km * 100:
            smart_charge, smart_distance = self.model.closest_charger_with_initial_point(
                self.current_point,
                self.path[0], self)
            if smart_charge is not None:
                return smart_charge, smart_distance
            with open("unfinished" + str(self.unique_id) + ".json", "w") as outfile:
                car_logs = {self.unique_id: self.logs}
                json.dump(car_logs, outfile)
            raise Exception("Cant get to next point")
        else:
            return None, naive_dist

    def stop_charge(self):
        self.battery_energy = self.max_battery
        self.charger.stop_charge(self.unique_id)
        self.is_charging = False
        self.is_moving = True
        self.handle_departure()

    def step(self):
        if self.is_charging:
            return
        if self.dist_to_next <= 0.0:
            self.battery_energy -= self.dist_to_next * self.average_consume_per_100_km / 100
            self.dist_to_next = 0.0
            if len(self.path) == 0:
                return self.check_finished()
            if self.needToCharge:
                self.go_charge(self.closestStation)
                self.current_point = self.closestStation.ref_id
                self.logs.append({"Station": [self.current_point, len(self.closestStation.waiting)]})
                self.logs.append({"Battery": [self.max_battery, self.battery_energy]})
                self.needToCharge = False
            else:
                self.current_point = self.path[0]
                self.path = self.path[1:]
                self.logs.append({"Current": self.current_point})
                if len(self.path) == 0:
                    return self.check_finished()
                self.handle_departure()

        if self.is_moving:
            # self.logs.append({"Moving": self.dist_to_next})
            self.battery_energy -= self.consume_per_minute
            self.km += self.dist_per_minute
            if self.needToCharge:
                self.kmToCharge += self.dist_per_minute
            self.dist_to_next -= self.dist_per_minute

    def handle_departure(self):
        station, dist = self.should_charge()
        if station is not None:
            self.closestStation = station
            self.dist_to_next = dist
            self.needToCharge = True
            self.logs.append({"Next": self.model.stop_points[self.path[0]]})
        else:
            self.dist_to_next = self.model.get_real_distance(self.current_point, self.path[0])
            self.logs.append(
                {"Travel": [self.current_point, self.model.stop_points[self.path[0]], self.dist_to_next]})

    def check_finished(self):
        if self.finished:
            return
        else:
            self.logs.append("Finished service")
            self.model.has_finished(self.unique_id)
            self.finished = True
            return

    @staticmethod
    def type():
        return "car"


def new_tesla_model_s(i, model, bt):
    return CarAgent(i, model, 71 * bt, 71, 17.85)


def new_tesla_model_3(i, model, bt):
    return CarAgent(i, model, 54 * bt, 54, 15.25)


def new_tesla_model_y(i, model, bt):
    return CarAgent(i, model, 75 * bt, 75, 15.36)


def new_chevrolet_bolt(i, model, bt):
    return CarAgent(i, model, 66 * bt, 66, 15.83)


def new_mustang_mach_e(i, model, bt):
    return CarAgent(i, model, 68 * bt, 68, 20.0)


def new_renault_twizy(i, model, bt):
    return CarAgent(i, model, 6.1 * bt, 6.1, 6.8)


def new_renault_zoe(i, model, bt):
    return CarAgent(i, model, 52 * bt, 52, 13.16)
