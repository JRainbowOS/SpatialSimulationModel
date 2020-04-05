from typing import List

from tile import Tile
from cartesian import Cartesian2D

class Grid(Tile):

    GRIDSIZE = 5
    COORD_SYSTEM = Cartesian2D

    def __init__(self):
        self.size = Grid.GRIDSIZE
        self.coord_system = Grid.COORD_SYSTEM

    @classmethod
    def cartesian_to_toroidal(cls, coord: Cartesian2D):
        x_in, y_in = coord.x, coord.y
        x_out, y_out = x_in % cls.GRIDSIZE, y_in % cls.GRIDSIZE
        new_coord = Cartesian2D(x_out, y_out)
        return new_coord

    @classmethod
    def float_to_toroidal(cls, coord: float):
        new_coord = coord % cls.GRIDSIZE
        return new_coord

    @classmethod
    def coord_list_to_toroidal(cls, coord_list: List[Cartesian2D]):
        toroidal_list = [cls.to_toroidal(coord) for coord in coord_list]
        return toroidal_list

    @classmethod
    def trace_list_to_toroidal(cls, trace_list: List[float]):
        toroidal_list = [cls.float_to_toroidal(coord) for coord in trace_list]
        return toroidal_list

    def draw(self):
        pass


def main():

    grid = Grid()
    # in_coords = [Cartesian2D(12, -14), Cartesian2D(3, 19)]
    # out_coords = grid.coord_list_to_toroidal(in_coords)
    in_trace = [2,4,7,13,-4]
    out_trace = grid.trace_list_to_toroidal(in_trace)
    print(out_trace)
    # grid.draw()

if __name__ == '__main__':
    main()