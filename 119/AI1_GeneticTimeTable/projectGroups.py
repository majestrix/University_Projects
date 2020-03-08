import itertools

class Group:
    reserved = False
    def __init__(self,topic,students):
        self.topic = topic
        self.students = students

    def __str__(self):
        return str(self.topic) + '[' + ' '.join(map(str, self.pref)) + ']'