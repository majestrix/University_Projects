from timeTable import TimeTable
from gene import Gene

import pandas as pd
import collections
import datetime
import xlwt
import xlrd

class Chromosome:

    fitness=1000
    def __init__(self,groups,examiners, days=2, fromTime=9,toTime=15, sessionTime=1.2, parallel=5):
        self.days = days
        self.fromTime = fromTime
        self.toTime = toTime
        self.sessionTime = sessionTime
        self.parallel = parallel
        self.timeTable = TimeTable(days, toTime-fromTime, sessionTime, parallel)
        self.projectGroups = groups
        self.examiners = examiners
        self.combine()

    def combine(self):
        #Check if times are sufficent before randomly scheduling
        maxSlots = int( ( (self.toTime - self.fromTime) / self.sessionTime) * self.parallel * self.days )
        slots = (len(self.projectGroups.groups))
        if(maxSlots < slots):
            print("ERROR: No sufficent slots! Required:" + str(slots) +" Available: " + str(maxSlots))
            exit(1)
        #Random Scheduling
        for group in self.projectGroups.groups:
            genom = Gene(group, self.examiners)
            self.timeTable.scheduleRandomly(genom)

    def getFitness(self):
        conflicts = self.getSessionConflictsAndFrequency() + self.getThreeSessionConflict()
        res = -1 if conflicts == 0 else conflicts
        return res

    def getSessionConflictsAndFrequency(self):
        #Make sure there are no two same examiners in the same hour
        conflicts = 0
        frequencyList = []
        for sessionGroup in self.timeTable.slots:
            sessionExaminers = []
            for gene in sessionGroup:
                if type(gene) != str:
                    sessionExaminers.extend(gene.getExaminers())
                    frequencyList.extend(gene.getExaminers())
            conflictCounter = collections.Counter(sessionExaminers)
            for count in conflictCounter.values():
                if count > 1:
                    conflicts += 1
        frequencyCounter = collections.Counter(frequencyList)
        #Determine MAX and MIN projects each examiner
        for count in frequencyCounter.values():
            if(count > 6 or count < 3):
                conflicts += 1
        return conflicts

    def getThreeSessionConflict(self):
        conflicts = 0
        iterations = int(len(self.timeTable.slots))
        #iterate in a window of 3 sessions until we reach index out of bounds
        #if UNION of examiners exist then we have a conflict!
        for i in range(iterations):
            firstSessionExaminers = []
            secondSessionExaminers = []
            thirdSessionExaminers = []
            try:
                for (gene1,gene2,gene3) in zip(self.timeTable.slots[i],self.timeTable.slots[i+1],self.timeTable.slots[i+2]):
                    if gene1 != None and type(gene1) != str:
                        firstSessionExaminers.extend(gene1.getExaminers())
                    if gene2 != None and type(gene2) != str:
                        secondSessionExaminers.extend(gene2.getExaminers())
                    if gene3 != None and type(gene3) != str:
                        thirdSessionExaminers.extend(gene3.getExaminers())
                inter = list(set(firstSessionExaminers) & set(secondSessionExaminers) & set(thirdSessionExaminers))
                conflicts += len(inter)
            except IndexError:
                #reached out of index
                return conflicts

    def printChromosome(self):
        dt = pd.DataFrame(self.timeTable.slots)
        axis = []
        fromTime = datetime.timedelta(hours=self.fromTime)
        toTime = datetime.timedelta(hours=self.toTime)
        hours = int(self.sessionTime)
        mins = (self.sessionTime - hours)*100
        incTime = datetime.timedelta(hours=hours,minutes=mins)


        for day in range(self.days):
            for x in range(int(self.timeTable.arrayHeight/self.timeTable.days)):
                time = ":".join(str(fromTime + incTime*x).split(":")[:2])
                txt = "D"+str(day) + " " + time.rjust(5)
                axis.extend([txt])
        dt.set_axis(axis, axis=0, inplace=True)
        print(dt.to_string())

    def exportToExcel(self):
        wb = xlwt.Workbook()
        ws = wb.add_sheet("Output")

        style = xlwt.easyxf('font: name Calibri, color-index black, bold on, height 220;align: wrap on, horiz center, vert center;')
        styleB = xlwt.easyxf('font: name Calibri, color-index white, bold on, height 220;'
                             'align: horiz center, vert center;'
                             'pattern:pattern solid, fore_colour light_blue;'
                             'border: left medium,top medium,right medium,bottom medium, top_color black, bottom_color black, right_color black, left_color black;')
        styleTime = xlwt.easyxf('font: name Calibri, color-index black, bold on, height 220;align: wrap on, horiz center, vert center;'
                                'pattern: pattern bricks, fore-color sky_blue')

        fromTime = datetime.timedelta(hours=self.fromTime)
        toTime = datetime.timedelta(hours=self.toTime)
        hours = int(self.sessionTime)
        mins = (self.sessionTime - hours)*100
        incTime = datetime.timedelta(hours=hours,minutes=mins)

        dayTime = []
        for day in range(self.days):
            for x in range(int(self.timeTable.arrayHeight/self.timeTable.days)):
                time = ":".join(str(fromTime + incTime*x).split(":")[:2])
                txt = ["D"+str(day), time]
                dayTime.extend([txt])
        row = 1
        col = 0
        sessionIndex = 0
        for session in self.timeTable.slots:

            #sheet.write_merge(top_row, bottom_row, left_column, right_column, 'Long Cell')
            ws.write_merge(row,row+3,col,col, dayTime[sessionIndex][0] + " " + dayTime[sessionIndex][1] ,styleTime)
            col += 1
            sessionIndex += 1

            for group in session:
                if type(group) != str:
                    dataCaps = ["Project","Students","Supervisor","Examiners"]
                    ws.write(row   , col, dataCaps[0] ,styleB)
                    ws.write(row+1 , col, dataCaps[1] ,styleB)
                    ws.write(row+2 , col, dataCaps[2] ,styleB)
                    ws.write(row+3 , col, dataCaps[3] ,styleB)
                    col+=1

                    titleId = "Project("+str(group.id)+")\n" + group.title
                    students = ",".join(group.students)
                    if type(group) != str:
                        examiners = "\n".join(group.examiners)
                    else:
                        examiners = ""
                    ws.write(row   , col, titleId           ,style)
                    ws.write(row+1 , col, students          ,style)
                    ws.write(row+2 , col, group.supervisor  ,style)
                    ws.write(row+3 , col, examiners         ,style)
                    col += 1
            row += 5
            col = 0

        wb.save("output.xls")
        readerSheet = xlrd.open_workbook("output.xls").sheet_by_index(0)
        for row in range(readerSheet.nrows):
            for column in range(readerSheet.ncols):
                thisCell = readerSheet.cell(row, column)
                neededWidth = int((1 + len(str(thisCell.value))) * 200)
                if ws.col(column).width < neededWidth:
                    ws.col(column).width = neededWidth
        wb.save("output.xls")



