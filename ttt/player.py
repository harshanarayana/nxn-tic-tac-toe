class Player(object):
    def __init__(self, name: str, marker: str):
        self._name: str = name
        self._marker: str = marker

    @property
    def marker(self) -> str:
        return self._marker

    @property
    def name(self) -> str:
        return self._name
