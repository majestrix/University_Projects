class Gene:

    def __init__(self,group,examiners):
        self.group = group
        self.examinersObject = examiners
        self.id = group["id"]
        self.pref = group["pref"]
        self.students = group["students"]
        self.title = group["title"]
        self.supervisor = group["supervisor"]
        self.examiners = examiners.selectExaminers(group["pref"],group["supervisor"])


    def getExaminers(self):
        return self.examiners + [self.supervisor]

    def mutate(self):
        self.examiners = self.examinersObject.selectExaminers(self.group["pref"], self.group["supervisor"])

    def __str__(self):
        people = self.examiners + [self.supervisor]
        people = [name.rsplit(" ")[-1] for name in people]
        people = "|".join(people)
        return (self.id +" "+ people).ljust(10)
