from timeTable import TimeTable
from projectGroups import Groups
from examiners import Examiners
from gene import Gene
import pandas as pd

class Chromosomes:
    days = 2
    timePerDay = 6
    sessionTime = 2
    parallel = 4

    def __init__(self,path):
        self.chromosomes = []
        self.timeTable = TimeTable(self.days, self.timePerDay, self.sessionTime, self.parallel)
        self.projectGroups = Groups(path)
        self.examiners = Examiners(path)

    def populate(self):
        for group in self.projectGroups.groups:
            genom = Gene(group, self.examiners)
            self.timeTable.scheduleRandomly(genom)

    def printChromosome(self):
        dt = pd.DataFrame(self.timeTable.slots)
        axis = []
        x = int(self.timeTable.arrayHeight/self.timeTable.days)
        for day in range(self.days):
            txt = "D"+str(day)
            axis.extend([txt]*x)
        print(axis)
        print(self.timeTable.slots)
        dt.set_axis(axis, axis=0, inplace=True)
        print(dt)







