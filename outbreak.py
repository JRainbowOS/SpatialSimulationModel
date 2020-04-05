import numpy as np 

from typing import List
import matplotlib.pyplot as plt

from scenario import Scenario

from grid import Grid
from person import Person
from community import Community
from cartesian import Cartesian2D

class Outbreak(Scenario):

    def __init__(self,
                 grid: Grid,
                 community: Community):
        self.grid = grid
        self.community = community

    def evolve(self):
        self.community.multistep()

    def plot_traces(self):
        for _id, person in self.community.host_dict.items():
            tr = person.trace
            # print(tr)
            new_tr = self.grid.coord_list_to_toroidal(tr)
            s = [coord.x for coord in new_tr]
            # print(f'trace for id \t {_id}: {s}')
            # t = [coord.y for coord in new_tr]
            # plt.plot(s, t) 
        # plt.show()

    def sketch(self):
        for _id, person in self.community.host_dict.items():
            s = person.trace_x
            t = person.trace_y
            plt.plot(s, t)
        plt.show()


            # for pt in tr:

            #     toroidal_pt = self.grid.toroidal(pt)
            #     traces.append()

def person_generator(grid_size):
    i = 1
    while True:
        start_x, start_y = np.random.uniform(0, grid_size, size=2)
        start = Cartesian2D(start_x, start_y)
        person = Person(_id=i,
                        status='susceptible',
                        position=start)
        i += 1
        yield person

def main():
    
    NUM_PEOPLE = 10  
    GRID_SIZE = 5  

    pg = person_generator(GRID_SIZE)
    people = [next(pg) for _ in range(NUM_PEOPLE)]
    com = Community(people)

    grd = Grid()
    
    ob = Outbreak(grd, com)

    for _ in range(10):
        ob.evolve()

    ob.sketch()

if __name__ == '__main__':
    main()