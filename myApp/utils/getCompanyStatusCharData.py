from myApp.models import JobInfo
from .publicData import *
import json
def getPageData():
    return getTypes()

def getCompanyStatusData():
    jobs = JobInfo.objects.all()
    statusData = {}
    for job in jobs:
        if statusData.get(job.companyStatus,-1) == -1:
            statusData[job.companyStatus] = 1
        else:
            statusData[job.companyStatus] += 1
    result = []
    for k,v in statusData.items():
        result.append({
            'name':k,
            'value':v
        })
    return result

def getTeachnologyData(type):
    if type == '不限':
        jobs = JobInfo.objects.all()
    else:
        jobs = JobInfo.objects.filter(type=type)
    workTagData = {}
    for job in jobs:
        workTag = json.loads(job.workTag)
        for w in workTag:
            if not w: break;
            if workTagData.get(w,-1) == -1:
                workTagData[w] = 1
            else:
                workTagData[w] += 1
    result = sorted(workTagData.items(), key=lambda x:x[1],reverse=True)[:20]
    TeachnologyDataRow = []
    TeachnologyDataColumn = []
    for k,v in result:
        TeachnologyDataRow.append(k)
        TeachnologyDataColumn.append(v)
    return TeachnologyDataRow,TeachnologyDataColumn