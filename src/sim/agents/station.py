import mesa

percentage_cut = 0.5
distance_cut = 50
number_of_cars_to_cut = 4

shall_cut = True
shall_order = True


class StationAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, spots, power, coords):
        super().__init__(unique_id, model)
        self.spots = spots  # battery in W.h
        self.power = power / 60
        self.using = list()
        self.waiting = list()
        self.coords = coords
        self.order_waiting = self.order_waiting_fastest_first
        self.cut_car = self.cut_on_percentage

        self.ignore_limit = set()

    def order_waiting_fastest_first(self, car):
        # print(car.max_battery - car.battery_energy, self.power,
        #       (car.max_battery - car.battery_energy) / (self.power * 60))
        return (car.max_battery - car.battery_energy) / (self.power * 60)

    def start_charge(self, car):
        if len(self.using) < self.spots:
            self.using.append(car)
        else:
            self.waiting.append(car)
        if shall_order:
            self.waiting.sort(key=self.order_waiting)
        if shall_cut:
            if (car.battery_energy / car.max_energy) >= percentage_cut:
                self.ignore_limit.add(car.unique_id)

    def stop_charge(self, unique_id):
        self.using = [x for x in self.using if not x.unique_id == unique_id]
        if len(self.waiting) > 0:
            self.using.append(self.waiting.pop(0))
        if shall_cut and unique_id in self.ignore_limit:
            self.ignore_limit.remove(unique_id)

    def step(self):
        for car in self.using:
            car.charge(self.power)
            if car.battery_energy >= car.max_battery:
                car.stop_charge()
            elif shall_cut and self.cut_car(car):
                car.stop_charge()

    def cut_on_percentage(self, car):
        return car.unique_id not in self.ignore_limit and len(self.waiting) >= number_of_cars_to_cut and \
            (car.battery_energy / car.max_energy) >= percentage_cut

    def cut_on_distance(self, car):
        return car.unique_id not in self.ignore_limit and \
            len(self.waiting) >= number_of_cars_to_cut and (
                        car.battery_energy / car.average_consume_per_100_km * 100) >= distance_cut

    @staticmethod
    def type():
        return "station"
