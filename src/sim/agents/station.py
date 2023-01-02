import mesa


class StationAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, spots, power):
        super().__init__(unique_id, model)
        self.spots = spots  # battery in W.h
        self.power = power
        self.using = list()
        self.waiting = list()

    def start_charge(self, car):
        if len(self.using) < self.spots:
            self.using.append(car)
        else:
            self.waiting.append(car)

    def stop_charge(self, unique_id):
        self.using = [x for x in self.using if not x.unique_id == unique_id]
        if len(self.waiting) > 0:
            self.using.append(self.waiting.pop(0))

    def step(self):
        for car in self.using:
            car.charge(self.power / 60)

    @staticmethod
    def type():
        return "station"
