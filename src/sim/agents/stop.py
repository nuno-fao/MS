class StopAgent():
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model

    @staticmethod
    def type():
        return "stop"
