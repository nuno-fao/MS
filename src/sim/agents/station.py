class StationAgent():
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, spots, power, coords):

        self.unique_id = unique_id
        self.model = model
        self.spots = spots  # battery in W.h
        self.power = power / 60
        self.using = list()
        self.waiting = list()
        self.coords = coords
        self.waitTimePerCar = {}
        self.occupancyPerStep = []

    def start_charge(self, car):
        if len(self.using) < self.spots:
            self.using.append(car)
        else:
            self.waiting.append(car)

        if car.unique_id in self.waitTimePerCar.keys():
            self.waitTimePerCar[car.unique_id].append(0)
        else:
            self.waitTimePerCar[car.unique_id] = [0]

    def stop_charge(self, unique_id):
        self.using = [x for x in self.using if not x.unique_id == unique_id]
        if len(self.waiting) > 0:
            self.using.append(self.waiting.pop(0))

    def step(self):
        self.occupancyPerStep.append((len(self.using) + len(self.waiting)) * 100 / self.spots)

        for car in self.waiting:
            self.waitTimePerCar[car.unique_id][-1] += 1

        for car in self.using:
            car.charge(self.power)
            if car.battery_energy >= car.max_battery:
                car.stop_charge()

    @staticmethod
    def type():
        return "station"
