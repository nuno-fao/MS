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

    def go_charge(self):
        self.is_moving = False
        # self.is_preparing_charging = True
        self.is_charging = True
        self.charger = self.random.choice(self.model.stations_list)

    def should_charge(self):
        next_point_distance = self.model.get_dist(self.current_point, self.path[0])
        next_point = self.model.stop_points[self.path[0]]
        charger, dist = self.model.closest_charge(next_point)
        print(charger, dist)

    def step(self):
        if self.dist_to_next <= 0.0:
            self.dist_to_next = self.model.get_dist(self.current_point, self.path[0])
            self.current_point = self.path[0]
            self.path = self.path[1:]

        if self.is_moving:
            self.battery_energy -= 8.3 / 1000 * 60 * self.average_consume_per_100_km / 100
            self.km += 8.3 / 1000 * 60
            self.dist_to_next -= 8.3 / 1000 * 60
        # print("CONSUMING :" + str(self.unique_id) + " " + str(self.battery_energy) + " " + str(self.km) + " " +
        #       str(self.max_battery))
        else:
            # if self.is_preparing_charging:
            #     if self.charging_delay >= 2:
            #         self.is_preparing_charging = False
            #         self.is_charging = True
            #         self.charger.start_charge(self)
            #         self.charging_delay = 0
            #     else:
            #         self.charging_delay += 1
            # elif self.is_charging and self.battery_energy >= self.max_battery:
            #     self.battery_energy = self.max_battery
            #     self.charger.stop_charge(self.unique_id)
            #     self.is_charging = False
            #     self.is_moving = True
            if self.is_charging:
                if self.battery_energy >= self.max_battery:
                    self.battery_energy = self.max_battery
                    self.charger.stop_charge(self.unique_id)
                    self.is_charging = False
                    self.is_moving = True
                # print("CHARGING :" + str(self.unique_id) + " " + str(self.battery_energy) + " " + str(self.km) + " " +
                #       str(self.max_battery))

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
