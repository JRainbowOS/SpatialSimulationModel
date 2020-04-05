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

    def sketch(self):
        traces = [] 
        for _id, person in self.community.host_dict.items():
            tr = person.trace
            traces.append(tr)


def main():
    
    START = Cartesian2D(0, 0)
    
    people = [Person(_id=i,
                 status='infected',
                 position=START) for i in range(10)]    
    com = Community(people)
    grd = Grid()
    
    ob = Outbreak(grd, com)
    ob.evolve()

if __name__ == '__main__':
    main()