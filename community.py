from typing import List

from population import Population
from person import Person
from cartesian import Cartesian2D

class Community(Population):

    def __init__(self,
                 people: List[Person]):
        self._hosts = people
        self.ids = None
        self.host_dict = self._create_host_dict()
        # self.trace_dict = self._create_trace_dict()

    def multistep(self):
        for _id, person in self.host_dict.items():
            person.step()
        # return self.host_dict
    
def main():

    START = Cartesian2D(0, 0)
    people_list = [Person(i, 'infected', START) for i in range(10)]
    com = Community(people_list)
    bearing_list = [person.bearing for person in people_list]
    print(bearing_list)
    # print(com.trace_dict)
    for _ in range(10):
        com.multistep()
    tr = com.host_dict[1].trace_x
    # print(tr)

if __name__ == '__main__':
    main()
