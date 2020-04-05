from abc import ABC, abstractclassmethod

class Tile(ABC):

    SIZE = 1

    def __init__(self):
        self.size = Tile.size

    @abstractclassmethod
    def draw(self):
        pass