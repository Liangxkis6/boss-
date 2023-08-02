from myApp.models import User,JobInfo
from .publicData import *
import time
import json
def getNowTime():
    timeFormat = time.localtime()
    year = timeFormat.tm_year
    month = timeFormat.tm_mon
    day = timeFormat.tm_mday
    monthList = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    return year,monthList[month - 1],day

def getTagData():
    jobs = getAllJobInfo()
    users = getAllUser()
    educationsTop = "学历不限"
    salaryTop = 0
    salaryMonthTop = 0
    address = {}
    pratice = {}
    for job in jobs:
        if educations[job.educational] < educations[educationsTop]:
            educationsTop = job.educational
        if not job.pratice:
            salary = json.loads(job.salary)[1]
            if salaryTop < salary:
                salaryTop = salary
        if int(job.salaryMonth) > salaryMonthTop:
            salaryMonthTop = int(job.salaryMonth)
        if address.get(job.address,-1) == -1:
            address[job.address] = 1
        else:
            address[job.address] += 1
        if pratice.get(job.pratice,-1) == -1:
            pratice[job.pratice] = 1
        else:
            address[job.address] += 1
    addressStr = sorted(address.items(),key=lambda x:x[1],reverse=True)[:3]
    addressTop = ""
    for i in addressStr:
        addressTop += i[0] + ","
    praticeMax = sorted(pratice.items(),key=lambda x:x[1],reverse=True)
    # a = "普通岗位" ? praticeMax[0][0] == False : "实习岗位"
    return len(jobs),len(users),educationsTop,salaryTop,salaryMonthTop,addressTop,praticeMax[0][0]

def getUserCreateTime():
    users = getAllUser()
    data = {}
    for u in users:
        if data.get(str(u.createTime),-1) == -1:
            data[str(u.createTime)] = 1
        else:
            data[str(u.createTime)] += 1
    result = []
    for k,v in data.items():
        result.append({
            'name':k,
            'value':v
        })
    return result

def getUserTop5():
    users = getAllUser()
    def sort_fn(item):
        return time.mktime(time.strptime(str(item.createTime),'%Y-%m-%d'))
    users = list(sorted(users,key=sort_fn,reverse=True))[:6]
    return users

def getAllJobsPBar():
    jobs = getAllJobInfo()
    tempData = {}
    for job in jobs:
        if tempData.get(str(job.createTime),-1) == -1:
            tempData[str(job.createTime)] = 1
        else:
            tempData[str(job.createTime)] += 1
    def sort_fn(item):
        item = list(item)
        return time.mktime(time.strptime(str(item[0]), '%Y-%m-%d'))
    result = list(sorted(tempData.items(),key=sort_fn,reverse=False))
    def map_fn(item):
        item = list(item)
        item.append(round(item[1] / len(jobs),3))
        return item
    result = list(map(map_fn,result))
    return result

def getTableData():
    jobs = getAllJobInfo()
    for i in jobs:
        i.workTag = '/'.join(json.loads(i.workTag))
        if i.companyTags != "无":
            i.companyTags = '/'.join(json.loads(i.companyTags))
        if i.companyPeople == '[0, 10000]':
            i.companyPeople = '10000人以上'
        else:
            i.companyPeople = json.loads(i.companyPeople)
            i.companyPeople = list(map(lambda x:str(x) + '人',i.companyPeople))
            i.companyPeople = '-'.join(i.companyPeople)
        i.salary = json.loads(i.salary)[1]
    return jobs
    # jobs[0].workTags = '/'.join(json.loads(jobs[0].workTag))
    # def map_fn(item):
    #     item.workTag = "/".join()
    # jobs = list(map(map_fn,jobs))


