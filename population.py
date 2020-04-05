from abc import ABC, abstractclassmethod
from typing import List

from host import Host
from person import Person
from cartesian import Cartesian2D


class Population(ABC):

    def __init__(self,
                 hosts: List[Host]):
        self._hosts = hosts
        self.ids = None
        self.host_dict = self._create_host_dict()
        # self.trace_dict = self._create_trace_dict()

    def _create_host_dict(self):
        ids = [host._id for host in self._hosts]
        self.ids = ids
        host_dict = {i: host for (i, host) in zip(ids, self._hosts)}
        return host_dict

    # def _create_trace_dict(self):
    #     initial_positions = [[host.position] for host in self._hosts]
    #     trace_dict = {_id: initial_positions[j] for _id, j in enumerate(self.ids)}
    #     return trace_dict

    @abstractclassmethod
    def multistep(self):
        pass


def main():

    START = Cartesian2D(0, 0)
    host_list = [Person(i, 'infected', START) for i in range(10)]
    print(host_list)
    pop = Population(host_list)
    print(pop.trace_dict)


if __name__ == '__main__':
    main()



