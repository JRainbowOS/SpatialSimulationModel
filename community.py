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
        self.status_history_dict = self._create_status_history_dict()

    def multistep(self):
        for _id, person in self.host_dict.items():
            person.step()

    def spread_infection(self, radius):
        at_risk_susceptibles = self._at_risk_susceptibles(radius=radius)
        for _id in self.host_dict.keys():
            if _id in at_risk_susceptibles:
                # Status changes
                self.status_history_dict[_id].append('infected')
                self.host_dict[_id].status = 'infected'
            else:
                # Status persists
                self.status_history_dict[_id].append(self.status_history_dict[_id][-1])
        return at_risk_susceptibles

    def _at_risk_susceptibles(self, radius):
        sus, inf, rem = self._sir_id()
        infected_positions = [self._get_location(_id) for _id in inf]
        at_risk_susceptibles = []
        for s in sus:
            sus_pos = self._get_location(s)
            for inf_pos in infected_positions:
                if inf_pos.distance_to(sus_pos) < radius: # THIS NEEDS TO BE MOD GRID!
                    at_risk_susceptibles.append(s)
        return at_risk_susceptibles

    def _get_location(self, _id):
        return self.host_dict[_id].position


    def _sir_id(self):
        # Could include this in multistep?
        susceptible_ids = []
        infectious_ids = []
        removed_ids = []
        for _id, person in self.host_dict.items():
            if person.status == 'susceptible':
                susceptible_ids.append(_id)
            elif person.status == 'infected':
                infectious_ids.append(_id)
            elif person.status == 'removed':
                removed_ids.append(_id)
            else:
                continue
        return susceptible_ids, infectious_ids, removed_ids

    
def main():

    START = Cartesian2D(0, 0)
    people_list = [Person(i, 'infected', START) for i in range(10)]
    man = Person(1, 'infected', Cartesian2D(1, 1))
    woman = Person(2, 'susceptible', Cartesian2D(1, 3))
    com = Community([man, woman])
    s, i, r = com._sir_id()
    print(s, i, r)
    risk = com._at_risk_susceptibles(radius=3)
    com.spread_infection(radius=3)
    s, i, r = com._sir_id()
    print(s, i, r)
    shd = com.status_history_dict
    print(shd)

if __name__ == '__main__':
    main()
