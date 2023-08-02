from myApp.models import History
import json
from django.db.models import F
def addHistory(userInfo,jobId):
    hisData = History.objects.filter(job_id=jobId,user=userInfo)
    if len(hisData):
        hisData[0].count = F("count") + 1
        hisData[0].save()
    else:
        History.objects.create(job_id=jobId, user=userInfo)

def removeHistory(hisId):
    his = History.objects.get(id=hisId)
    his.delete()

def getHistoryData(userInfo):
     data = list(History.objects.filter(user=userInfo).order_by("-count"))
     def map_fn(item):
         item.job.salary = json.loads(item.job.salary)
         item.job.companyPeople = json.loads(item.job.companyPeople)
         item.job.workTag = json.loads(item.job.workTag)
         if item.job.companyTags == '无':
             item.job.companyTags = []
         else:
             item.job.companyTags = json.loads(item.job.companyTags)
         if not item.job.pratice:
             item.job.salary = list(map(lambda x:str(int(x / 1000)),item.job.salary))
         else:
             item.job.salary = list(map(lambda x: str(x), item.job.salary))

         item.job.salary = '-'.join(item.job.salary)
         item.job.companyPeople = list(map(lambda x: str(x), item.job.companyPeople))
         item.job.companyPeople = '-'.join(item.job.companyPeople)
         return item

     data = list(map(map_fn,data))
     return data
