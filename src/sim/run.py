import mesa

from model import Model


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.type() == "car":
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
        portrayal["r"] = 1.0

    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = mesa.visualization.ModularServer(
    Model, [grid], "Money Model", {"cars": 70, "stations": 3, "width": 20, "height": 20}
)

server.port = 8521  # The default
server.launch()
