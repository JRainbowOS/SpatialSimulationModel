from abc import ABC, abstractclassmethod
from math import pi

from coordinate import Coordinate

class Host(ABC):

    DT = 1
    SPEED = 1
    CURVATURE = pi/2

    def __init__(self, 
                 _id,
                 status,
                 position: Coordinate):
        self._id = id
        self.status = status
        self.position = position

    @abstractclassmethod
    def step(self):
        pass