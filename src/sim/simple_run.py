from model import Model

model = Model(70, 3, 16, 8)
i = 0
while len(model.finished) < 70:
    print(i, len(model.finished))
    model.step()
    i += 1
