import json

from model import Model

cars = 1000
model = Model(cars, 3, 16, 8)
i = 0
while len(model.finished) < cars:
    model.step()
    i += 1
    if i > 100000:
        with open("unfinished.json", "w") as outfile:
            car_logs = {}
            for car in model.cars_list:
                if car.finished == False:
                    car_logs[car.unique_id] = car.logs
            json.dump(car_logs, outfile)
        break

with open("logs.json", "w") as outfile:
    car_logs = {}
    for car in model.cars_list:
        car_logs[car.unique_id] = [car.logs, car.path]
        json.dump(car_logs, outfile)
        break

with open("car_distances.json", "w") as outfile:
    final = {}
    for car in model.cars_list:
        final[car.unique_id] = {"total": car.km, "km_spent_to_charge": car.kmToCharge}
    json.dump(final, outfile)

wait_times = {}
occupancies = {}
for station in model.stations_list:
    wait_times[station.unique_id] = station.waitTimePerCar
    occupancies[station.unique_id] = station.occupancyPerStep

with open("wait_times.json", "w") as outfile:
    json.dump(wait_times, outfile)
with open("occupancies.json", "w") as outfile:
    json.dump(occupancies, outfile)

with open("traffic_per_station.json", "w") as outfile:
    json.dump(model.trafficPerStation, outfile)
