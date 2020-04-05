from tile import Tile

class Grid(Tile):

    GRIDSIZE = 10

    def __init__(self):
        self.size = Grid.GRIDSIZE

    def draw(self):
        pass


def main():

    grid = Grid()
    grid.draw()

if __name__ == '__main__':
    main()