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
        self.traced = False
        self.toroidal_trace_dict_x = {}
        self.toroidal_trace_dict_y = {}

    def evolve(self, radius=1):
        self.community.multistep()
        self.community.spread_infection(radius=radius)
        self.sir_statistics()

    def sir_statistics(self):
        s_id, i_id, r_id = self.community._sir_id()
        print(f'\nNumber of Susceptible: \t {len(s_id)}')
        print(f'Number of Infected: \t {len(i_id)}')
        print(f'Number of Removed: \t {len(r_id)} \n')

    def toroidal_trace(self, plot=False):
        for _id, person in self.community.host_dict.items():
            s = self.grid.trace_list_to_toroidal(person.trace_x)
            self.toroidal_trace_dict_x[_id] = s
            t = self.grid.trace_list_to_toroidal(person.trace_y)
            self.toroidal_trace_dict_y[_id] = t
            self._ids.append(_id)
            self.traced = True
            if plot:
                plt.scatter(s, t)
        if plot:
            plt.show()

    def animate_outbreak(self):
        """
        Produce an animation of the pursuit processed so far
        """
        if not self.traced:
            self.toroidal_trace()

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
            if self.community.host_dict[_id].status == 'infected':
                col = 'ro'
            else:
                col = 'go'
            ln, = ax.plot([], [], col, linewidth=2, markersize=1)
            lines.append(ln)

        def init_animation():
            for ln in lines:
                ln.set_data([0, 1], [1, 2])
            # time_text.set_text('')
            return lines #, time_text

        def animate(i):
            self.sir_statistics()
            for lnum, _id in enumerate(self._ids):
                community_xdata[_id].append(self.toroidal_trace_dict_x[_id][i])
                community_ydata[_id].append(self.toroidal_trace_dict_y[_id][i])
                lines[lnum].set_data(community_xdata[_id], community_ydata[_id])

            # time_text.set_text(time_template % (i * dt))
            return lines #, time_text
            # return ln_chaser, ln_chased, time_text

        print('Creating animation')
        FuncAnimation(fig, 
                      animate,
                      len(self.toroidal_trace_dict_x[_id]), # not very nice!
                      init_func=init_animation,
                      interval=50,
                      blit=True,
                      repeat=True)
        plt.show()


def person_generator(grid_size, num_people, num_infected):
    assert num_infected < num_people, 'Cannot be more infected than total people!'
    i = 1
    while i < num_people + 1:
        start_x, start_y = np.random.uniform(0, grid_size, size=2)
        start = Cartesian2D(start_x, start_y)
        if i < num_infected + 1:
            infected = True
        else:
            infected = False
        if infected:
            person = Person(_id=i,
                            status='infected',
                            position=start)
        else:
            person = Person(_id=i,
                            status='susceptible',
                            position=start)
        i += 1
        yield person

def main():
    
    NUM_PEOPLE = 25
    NUM_INFECTED = 1
    GRID_SIZE = 5  
    TIME_STEPS = 50
    RADIUS_OF_INFECTION = 1

    pg = person_generator(grid_size=GRID_SIZE, 
                          num_people=NUM_PEOPLE,
                          num_infected=NUM_INFECTED)
    people = [next(pg) for _ in range(NUM_PEOPLE)]

    com = Community(people)

    grd = Grid()
    
    ob = Outbreak(grd, com)

    for _ in range(TIME_STEPS):
        ob.evolve(radius=RADIUS_OF_INFECTION)

    # ob.toroidal_trace(plot=False)
    ob.animate_outbreak()

if __name__ == '__main__':
    main()