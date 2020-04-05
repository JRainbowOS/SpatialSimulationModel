import numpy as np 

from typing import List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from scenario import Scenario

from grid import Grid
from person import Person
from community import Community
from cartesian import Cartesian2D

class Outbreak(Scenario):

    DT = 1 

    def __init__(self,
                 grid: Grid,
                 community: Community):
        self.grid = grid
        self.community = community
        self._ids = []
        self.toroidal_trace_dict_x = {}
        self.toroidal_trace_dict_y = {}

    def evolve(self):
        self.community.multistep()

    def toroidal_trace(self, plot=False):
        for _id, person in self.community.host_dict.items():
            s = self.grid.trace_list_to_toroidal(person.trace_x)
            self.toroidal_trace_dict_x[_id] = s
            t = self.grid.trace_list_to_toroidal(person.trace_y)
            self.toroidal_trace_dict_y[_id] = t
            self._ids.append(_id)
            if plot:
                plt.scatter(s, t)
        if plot:
            plt.show()

    def animate(self):
        """
        Produce an animation of the pursuit processed so far
        """
        dt = Outbreak.DT

        fig = plt.figure()
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(0, self.grid.size),
                                                      ylim=(0, self.grid.size))
        ax.set_aspect('equal')

        time_template = 'time = %.1fs'
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        
        community_xdata = {}
        community_ydata = {}
        lines = []
        for _id in self._ids:
            person_xdata, person_ydata = [], []
            community_xdata[_id] = person_xdata
            community_ydata[_id] = person_ydata
            ln, = ax.plot([], [], 'ro', linewidth=2, markersize=1)
            lines.append(ln)

        def init_animation():
            # for _id in self._ids:
            #     ln = community_ln[_id]
            #     ln.set_data([], [])
            for ln in lines:
                ln.set_data([], [])
            time_text.set_text('')
            return lines[0], time_text

        def animate(i):
            for i, _id in enumerate(self._ids):
                community_xdata[_id].append(self.toroidal_trace_dict_x[_id][i])
                community_ydata[_id].append(self.toroidal_trace_dict_y[_id][i])
                lines[i].set_data(community_xdata[_id], community_ydata[_id])

            time_text.set_text(time_template % (i * dt))
            return lines[0], time_text
            # return ln_chaser, ln_chased, time_text

        FuncAnimation(fig, 
                      animate,
                      len(self.toroidal_trace_dict_x[_id]), # not very nice!
                      init_func=init_animation,
                      interval=500,
                      blit=True,
                      repeat=False)
        plt.show()



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
    TIME_STEPS = 5

    pg = person_generator(GRID_SIZE)
    people = [next(pg) for _ in range(NUM_PEOPLE)]
    com = Community(people)

    grd = Grid()
    
    ob = Outbreak(grd, com)

    for _ in range(TIME_STEPS):
        ob.evolve()

    ob.toroidal_trace(plot=False)
    # print(ob.toroidal_trace_dict_x)
    # print(ob._ids)
    ob.animate()

if __name__ == '__main__':
    main()