from agents.car import *
from agents.station import StationAgent

funcs = [new_tesla_model_s,
         new_tesla_model_3,
         new_tesla_model_y,
         new_chevrolet_bolt,
         new_mustang_mach_e,
         new_renault_twizy,
         new_renault_zoe]


class Model(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, cars, stations, width, height):
        self.num_agents = cars + stations
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.cars_list = list()
        self.stations_list = list()
        # Create agents
        for i in range(cars):
            a = self.random.choice(funcs)(i, self, self.random.randint(0, 100) / 100.0)
            self.schedule.add(a)
            self.cars_list.append(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        # for i in range(stations):
        a = StationAgent(cars, self, 2, 250)
        self.schedule.add(a)
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(a, (x, y))
        self.stations_list.append(a)

        a = StationAgent(1 + cars, self, 5, 44)
        self.schedule.add(a)
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(a, (x, y))
        self.stations_list.append(a)

        a = StationAgent(2 + cars, self, 1, 44)
        self.schedule.add(a)
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(a, (x, y))
        self.stations_list.append(a)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
