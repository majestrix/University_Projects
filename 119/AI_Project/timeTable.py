import random
class TimeTable:

    def __init__(self,days,timePerDay,sessionTime,parallel):
        self.days = days
        self.timePerDay = timePerDay
        self.sessionTime = sessionTime
        self.arrayDepth = parallel
        self.arrayHeight = int(self.days*self.timePerDay/self.sessionTime)
        self.slots = self.createTimeSlots()

    def createTimeSlots(self):
        return [["N/A" for col in range(self.arrayDepth)] for row in range(self.arrayHeight)]

    def randomSlot(self):
        x = self.arrayDepth
        y = self.arrayHeight
        return (random.randint(0,x-1) , random.randint(0,y-1))

    def randomGene(self):
        x,y = self.randomSlot()
        return self.slots[y][x]

    def scheduleRandomly(self,gene):
        depth,height = self.randomSlot()
        while True:
            if(self.slots[height][depth] == "N/A"):
                self.slots[height][depth] = gene
                break
            depth, height = self.randomSlot()

    def findById(self,gene):
        for bigIndex, smallIndex in enumerate(self.slots):
            ids = []
            for item in smallIndex:
                if type(item) == str:
                    ids.append('N/A')
                else:
                    ids.append(item.id)
            try:
                if gene.id in ids:
                    return ids.index(gene.id),bigIndex
            except:
                if gene in ids:
                    return ids.index(gene),bigIndex



