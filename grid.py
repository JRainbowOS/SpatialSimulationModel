from typing import List

from tile import Tile
from cartesian import Cartesian2D

class Grid(Tile):

    GRIDSIZE = 10
    COORD_SYSTEM = Cartesian2D

    def __init__(self):
        self.size = Grid.GRIDSIZE
        self.coord_system = Grid.COORD_SYSTEM

    @classmethod
    def to_toroidal(cls, coord: Cartesian2D):
        x_in, y_in = coord.x, coord.y
        x_out, y_out = x_in % cls.GRIDSIZE, y_in % cls.GRIDSIZE
        new_coord = Cartesian2D(x_out, y_out)
        return new_coord

    @classmethod
    def coord_list_to_toroidal(cls, coord_list: List[Cartesian2D]):
        toroidal_list = [cls.to_toroidal(coord) for coord in coord_list]
        return toroidal_list

    def draw(self):
        pass


def main():

    grid = Grid()
    in_coords = [Cartesian2D(12, -14), Cartesian2D(3, 19)]
    out_coords = grid.coord_list_to_toroidal(in_coords)
    print(out_coords)
    # grid.draw()

if __name__ == '__main__':
    main()