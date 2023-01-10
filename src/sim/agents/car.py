import mesa

from agents.station import StationAgent

class CarAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, battery_energy, max_battery, average_consume_per_100_km):
        super().__init__(unique_id, model)
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
        self.logs = []

    def start_movement(self):
        self.is_moving = True

    def stop_movement(self):
        self.is_moving = False

    def charge(self, energy):
        self.battery_energy += energy

    def set_path(self, path):
        self.path = path
        self.current_point = path[0]
        self.path = self.path[1:]
        self.model.get_dist(self.current_point, self.path[0])

    def go_charge(self, station):
        self.is_moving = False
        # self.is_preparing_charging = True
        self.is_charging = True
        self.charger = station
        self.charger.start_charge(self)

    def should_charge(self):
        next_point_distance = self.model.get_dist(self.current_point, self.path[0])
        next_point = self.model.stop_points[self.path[0]]
        charger, dist = self.model.closest_charge(next_point)
        if next_point_distance + dist > self.battery_energy / self.average_consume_per_100_km * 100:
            return charger, dist
        else:
            return None, dist

    def stop_charge(self):
        self.battery_energy = self.max_battery
        self.charger.stop_charge(self.unique_id)
        self.is_charging = False
        self.is_moving = True

    def step(self):
        
        if self.dist_to_next <= 0.0:
            self.logs.append("Arrived at destination")
            if len(self.path) == 0:
                self.logs.append("Finished service")
                if self.finished:
                    return
                else:
                    self.model.has_finished(self.unique_id)
                    self.finished = True
                    return
            if self.needToCharge:
                # print(self.battery_energy) 
                self.logs.append("Charging" + str(self.closestStation.unique_id) )
                self.go_charge(self.closestStation)
                self.needToCharge = False
            elif self.is_charging:
                return
            else:
                station, dist = self.should_charge()
                if station is not None:
                    self.logs.append("Needs to charge, going to closest station" )
                    self.closestStation = station
                    self.dist_to_next = dist
                    self.needToCharge = True
                else:
                    self.logs.append("Going to next point" )
                    self.dist_to_next = self.model.get_dist(self.current_point, self.path[0])
                    self.current_point = self.path[0]
                    self.path = self.path[1:]

        if self.is_moving:
            self.battery_energy -= self.consume_per_minute
            self.km += self.dist_per_minute
            self.dist_to_next -= self.dist_per_minute

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
