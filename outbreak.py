import numpy as np 
import os
from typing import List
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib.animation as animation

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
        self._ids = []
        self.traced = False
        self.toroidal_trace_dict_x = {}
        self.toroidal_trace_dict_y = {}

    def evolve(self, radius=1, 
                     chance_of_infection=1,
                     duration_of_infection=10):
        self.community.multistep()
        self.community.spread_infection(radius=radius, 
                                        chance_of_infection=chance_of_infection,
                                        grid_size=self.grid.size)
        rem = self.community.remove_infected(duration_of_infection=duration_of_infection)
        # print(rem)
        stat_str = self.sir_statistics()
        print(stat_str)

    def sir_statistics(self):
        s_id, i_id, r_id = self.community._sir_id()
        stat_str = f'\nNumber of Susceptible: \t {len(s_id)} \n' + \
                f'Number of Infected: \t {len(i_id)} \n' + \
                f'Number of Removed: \t {len(r_id)}'
        return stat_str

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

        # dt = Outbreak.DT

        fig = plt.figure()
        ax = fig.add_subplot(111, autoscale_on=False, xlim=(0, self.grid.size),
                                                      ylim=(0, self.grid.size))
        ax.set_aspect('equal')
        plt.title('Epidemic Simulation')

        time_template = 'time = %.1fs'
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

        community_xdata = {}
        community_ydata = {}
        lines = []
        s_num, i_num, r_num = 0, 0, 0
        for _id in self._ids:
            person_xdata, person_ydata = [], []
            community_xdata[_id] = person_xdata
            community_ydata[_id] = person_ydata
            if self.community.status_history_dict[_id][0] == 'susceptible':
                col = 'go'
                s_num += 1
            elif self.community.status_history_dict[_id][0] == 'infected':
                col = 'ro'
                i_num += 1
            elif self.community.status_history_dict[_id][0] == 'removed':
                col = 'k'
                r_num += 1
            ln, = ax.plot([], [], col, linewidth=2, markersize=2)
            lines.append(ln)

        stat_str = f'\nNumber of Susceptible: {s_num} \n' + \
                f'Number of Infected: {i_num} \n' + \
                f'Number of Removed: {r_num}'
        # place a text box in upper left in axes coords
        ax.text(0.05, 0.95, stat_str, transform=ax.transAxes, fontsize=8,
                verticalalignment='top', bbox=props)

        def init_animation():
            for ln in lines:
                ln.set_data([], [])
            # time_text.set_text('')
            return lines #, time_text

        def animate(i):
            s_num, i_num, r_num = 0, 0, 0
            for lnum, _id in enumerate(self._ids):
                # community_xdata[_id].append(self.toroidal_trace_dict_x[_id][i])
                # community_ydata[_id].append(self.toroidal_trace_dict_y[_id][i])
                community_xdata[_id] = [self.toroidal_trace_dict_x[_id][i]]
                community_ydata[_id] = [self.toroidal_trace_dict_y[_id][i]]
                lines[lnum].set_data(community_xdata[_id], community_ydata[_id])
                if self.community.status_history_dict[_id][i] == 'susceptible':
                    col = 'g'
                    s_num += 1
                elif self.community.status_history_dict[_id][i] == 'infected':
                    col = 'r'
                    i_num += 1
                elif self.community.status_history_dict[_id][i] == 'removed':
                    col = 'k'
                    r_num += 1
                lines[lnum].set_color(col)

            stat_str = f'\nNumber of Susceptible: {s_num} \n' + \
                    f'Number of Infected: {i_num} \n' + \
                    f'Number of Removed: {r_num}'
            ax.text(0.05, 0.95, stat_str, transform=ax.transAxes, fontsize=8,
                    verticalalignment='top', bbox=props)

            # time_text.set_text(time_template % (i * dt))
            return lines #, time_text
            # return ln_chaser, ln_chased, time_text

        print('Creating animation')
        ani = animation.FuncAnimation(fig, 
                                        animate,
                                        len(self.toroidal_trace_dict_x[_id]), # not very nice!
                                        init_func=init_animation,
                                        interval=50,
                                        blit=True,
                                        repeat=False)
        plt.show()
        return ani


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
    
    NUM_PEOPLE = 50
    NUM_INFECTED = 2
    GRID_SIZE = 10  
    TIME_STEPS = 200
    RADIUS_OF_INFECTION = 1
    CHANCE_OF_INFECTION = 0.01
    DURATION_OF_INFECTION = 25
    SAVE = True

    pg = person_generator(grid_size=GRID_SIZE, 
                          num_people=NUM_PEOPLE,
                          num_infected=NUM_INFECTED)
    people = [next(pg) for _ in range(NUM_PEOPLE)]

    com = Community(people)

    grd = Grid()
    
    ob = Outbreak(grd, com)

    for _ in range(TIME_STEPS):
        ob.evolve(radius=RADIUS_OF_INFECTION,
                  chance_of_infection=CHANCE_OF_INFECTION,
                  duration_of_infection=DURATION_OF_INFECTION)

    # ob.toroidal_trace(plot=False)
    ani = ob.animate_outbreak()

    if SAVE:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(artist='JRainbow'), bitrate=1800)
        ani.save(os.path.join('animations', f'{NUM_PEOPLE}_people_{NUM_INFECTED}_infected_with_removed_radius_1_chance_0_01_final.mp4'), writer=writer)

if __name__ == '__main__':
    main()