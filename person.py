from host import Host
from cartesian import Cartesian2D

from math import pi 
import numpy as np

class Person(Host):

    DT = 1
    SPEED = 1
    CURVATURE = pi / 3

    def __init__(self, 
                 _id,
                 status, 
                 position: Cartesian2D):
        self._id = _id
        self.status = status
        self.position = position
        self.bearing = 2 * pi * np.random.random()
        self.trace = [position]

    def step(self):
        dx, dy = self._find_displacement()
        self.position.x += dx
        self.position.y += dy
        self.trace.append(self.position)
        return self.position

    def _find_displacement(self):
        angle_inc = Person._get_random_angle()
        new_bearing = self.bearing + angle_inc
        self.bearing = new_bearing
        dx = Person.DT * Person.SPEED * np.cos(new_bearing)
        dy = Person.DT * Person.SPEED * np.sin(new_bearing)
        return dx, dy

    @classmethod
    def _get_random_angle(cls):
        angle = np.random.normal(0, cls.CURVATURE)
        return angle

def main():
    import matplotlib.pyplot as plt

    START = Cartesian2D(0, 0)
    man = Person(_id=1,
                 status='infected',
                 position=START)
    x_trace = []
    y_trace = []
    for _ in range(10):
        new_position = man.step()
        x_trace.append(new_position.x)
        y_trace.append(new_position.y)
    plt.plot(x_trace, y_trace)
    plt.show()

if __name__ == '__main__':
    main()