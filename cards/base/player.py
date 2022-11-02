class Player:
    def __init__(self, name):
        self._name = name
        self._score = 0

    @property
    def name(self):
        return self._name

    def strategy(self):
        return "No strategy declared"
