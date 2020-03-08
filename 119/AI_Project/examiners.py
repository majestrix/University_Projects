import xlrd
import random
class Examiners:
    def __init__(self,path):
        self.examiners = self.importExaminers(path)

    def importExaminers(self,path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(1)
        gen = sheet.get_rows()
        examiners = []
        for row in gen:
            name = row[0].value
            pref = row[1].value
            examiner = {"name": name,
                        "pref": pref}
            examiners.append(examiner)
        return examiners

    def selectExaminers(self,pref,expt):
        selectedPref = [dr["name"] for dr in self.examiners if dr["pref"] == pref]
        selected = [sub for sub in selectedPref if sub not in expt]
        if(selected.__len__() > 1):
            return random.sample(selected,2)
        else:
            return selected
