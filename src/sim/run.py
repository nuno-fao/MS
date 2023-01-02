import mesa

from model import Model


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Color": "red",
                 "Layer": 1,
                 "r": 0.5}

    if agent.type() == "station":
        portrayal["Color"] = "gray"
        portrayal["r"] = 1.0
        portrayal["Layer"] = 0
    elif agent.type() == "stop":
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.3

    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 160, 80, 1600, 800)
server = mesa.visualization.ModularServer(
    Model, [grid], "Money Model", {"cars": 70, "stations": 3, "width": 160, "height": 80}
)

server.port = 8521  # The default
server.launch()
