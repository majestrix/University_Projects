import xlrd

class Groups:

    def __init__(self,path):
        self.groups = self.importProjects(path)

    def importProjects(self,path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        gen = sheet.get_rows()

        groups = []
        student = []
        i = 0
        for row in gen:
            x = i % 4
            if (x == 0):
                i += 1
                continue
            if (x == 1):
                student.append(row[0].value)
                s = row[1].value
                project = s[s.find("(") + 1:s.find(")")]
            if (x == 2):
                student.append(row[0].value)
                s = row[1].value
                title = s[s.find(":") + 1:s.find("(") - 1]
                supervisor = s[s.find("(") + 1:s.find(")")]
            if (x == 3):
                student.append(row[0].value)
                group = {"id": project,
                         "pref": row[1].value,
                         "title": title,
                         "supervisor": supervisor,
                         "students": student}
                groups.append(group)
                student = []
                title = []
            i += 1
        return groups
