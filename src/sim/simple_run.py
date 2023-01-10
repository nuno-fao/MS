from model import Model
import json

cars = 500
model = Model(cars, 3, 16, 8)
i = 0
while len(model.finished) < cars:
    print(i, len(model.finished))
    model.step()
    i += 1
    if i > 10000:
        with open("unfinished.json", "w") as outfile:
            car_logs = {}
            for car in model.cars_list:
                if car.finished == False:
                    car_logs[car.unique_id] = car.logs
            json.dump(car_logs,outfile)
        break

with open("logs.json", "w") as outfile:
    car_logs = {}
    for car in model.cars_list:
        car_logs[car.unique_id] = car.logs
    json.dump(car_logs,outfile)

    
