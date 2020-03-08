# x = "Ahmad"
# list = [["Wasel Ghanem","Abdelkarim"],["Khalid","Ahmad"]]
#
# for bigIndex,smallIndex in enumerate(list):
#     if x in smallIndex:
#         print(bigIndex, smallIndex.index(x))

# x = ["Hanani","Wasel","Amjad"]
# y = ["Hanani","Qaroush","Hassan"]
# z = ["Hanani"]
#
# print(len(list(set(x) & set(y) & set(z))))
# print(lol())
# import datetime
#
# sessionTime = 1.2
# hours = int(sessionTime)
# mins = (sessionTime - hours)*100
#
# time = datetime.timedelta(hours=hours,minutes=mins)
# print(time*2)
# # time2=datetime.timedelta(hours=hours,minutes=mins)
# # print(time2)
# # oneHour = datetime.timedelta(hours=1,minutes=20)
# # print(time + datetime.timedelta(hours=2))
# # print(time + oneHour)

# x = [1,2,3,0,0,6]
# # print(all(i != 0 for i in x))
# print(sorted(x,reverse=False))

# x=[[1,5,2,3],[6,0,None,18,12],[13,None,18,16,17],[None,19,20,21,23]]
# conflicts = 0
# inter = list(set(x[1]) & set(x[2]) & set(x[3]))
# print(inter)
# iterations = int(len(x))
# for i in range(iterations):
#     firstSessionExaminers = []
#     secondSessionExaminers = []
#     thirdSessionExaminers = []
#     try:
#         for gene1,gene2,gene3 in zip(x[i],x[i+1],x[i+2]):
#             if type(gene1) != str:
#                 firstSessionExaminers.extend([gene1])
#             if type(gene2) != str:
#                 secondSessionExaminers.extend([gene2])
#             if type(gene3) != str:
#                 thirdSessionExaminers.extend([gene3])
#         inter = list(set(firstSessionExaminers) & set(secondSessionExaminers) & set(thirdSessionExaminers))
#         conflicts += len(inter)
#     except IndexError:
#         #reached out of index
#         print(conflicts)
