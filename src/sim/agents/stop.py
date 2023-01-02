import mesa


class StopAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    @staticmethod
    def type():
        return "stop"
