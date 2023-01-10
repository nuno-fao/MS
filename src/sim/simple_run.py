from model import Model

cars = 500
model = Model(cars, 3, 16, 8)
i = 0
while len(model.finished) < cars:
    print(i, len(model.finished))
    model.step()
    i += 1
