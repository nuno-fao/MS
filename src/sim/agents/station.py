percentage_cut = 0.5 # percentage of battery to cut
distance_cut = 50 # distance in km to cut
time_cut = 20 # time in minutes to cut

number_of_cars_to_cut = 4 # length of the queue to apply the cut

shall_cut = True # if the cut policy sould be applied
shall_order = True # if the non fifo ordering should be applied


class StationAgent():
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, spots, power, coords, ref_id):

        self.unique_id = unique_id
        self.model = model
        self.spots = spots  # battery in W.h
        self.power = power / 60
        self.using = list()
        self.waiting = list()
        self.coords = coords
        self.ref_id = ref_id

        self.waitTimePerCar = {}
        self.occupancyPerStep = []

        self.order_waiting = self.order_waiting_fastest_first
        self.cut_car = self.cut_on_distance # can be = self.cut_on_distance or self.cut_on_percentage or self.cut_on_time

        self.ignore_limit = set()
        self.time = dict()

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
            if (car.battery_energy / car.max_battery) >= percentage_cut:
                self.ignore_limit.add(car.unique_id)
            self.time[car.unique_id] = 0

        if car.unique_id in self.waitTimePerCar.keys():
            self.waitTimePerCar[car.unique_id].append(0)
        else:
            self.waitTimePerCar[car.unique_id] = [0]

    def stop_charge(self, unique_id):
        self.using = [x for x in self.using if not x.unique_id == unique_id]
        if len(self.waiting) > 0:
            self.using.append(self.waiting.pop(0))
        if shall_cut and unique_id in self.ignore_limit:
            self.ignore_limit.remove(unique_id)
        if shall_cut and unique_id in self.time.keys():
            self.time.pop(unique_id)

    def step(self):
        self.occupancyPerStep.append((len(self.using) + len(self.waiting)) * 100 / self.spots)

        for car in self.waiting:
            self.waitTimePerCar[car.unique_id][-1] += 1

        for car in self.using:
            if shall_cut:
                self.time[car.unique_id] += 1
            car.charge(self.power)
            if car.battery_energy >= car.max_battery:
                car.stop_charge()
            elif shall_cut and self.cut_car(car):
                print(car.battery_energy / car.max_battery)
                car.stop_charge()

    def cut_on_percentage(self, car):
        return car.unique_id not in self.ignore_limit and len(self.waiting) >= number_of_cars_to_cut and \
            (car.battery_energy / car.max_battery) >= percentage_cut

    def cut_on_time(self, car):
        return len(self.waiting) >= number_of_cars_to_cut and self.time[car.unique_id] >= time_cut

    def cut_on_distance(self, car):
        return car.unique_id not in self.ignore_limit and \
            len(self.waiting) >= number_of_cars_to_cut and (
                    car.battery_energy / car.average_consume_per_100_km * 100) >= distance_cut

    @staticmethod
    def type():
        return "station"
