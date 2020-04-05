from abc import ABC, abstractclassmethod

from tile import Tile
from population import Population

class Scenario(ABC):

    def __init__(self, tile: Tile, population: Population):
        self.tile = tile
        self.population = population

    @abstractclassmethod
    def evolve(self):
        pass

def main():
    pass

    # h = Host()
    # t = Tile()
    # s = Scenario(t, h)

if __name__ == '__main__':
    main()