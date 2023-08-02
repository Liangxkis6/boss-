import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boss直聘数据可视化分析.settings')
django.setup()
# 但是还是需要在文件开头添加两行配置环境变量的配置语句，让程序知道该去哪儿寻找 models 中的文件。
from myApp.models import *


class Spider:
    def __init__(self, type, page):
        self.type = type
        self.page = page
        self.spiderUrl = "https://www.zhipin.com/web/geek/job?query=%s&city=100010000&page=%s"

    def startBrower(self):
        option = webdriver.ChromeOptions()
        # option.add_experimental_option("debuggerAddress", "localhost:9222")
        # option.add_argument("--headless")
        # option.add_argument("--disable-gpu")
        option.add_experimental_option("excludeSwitches", ['enable-automation'])
        # s = Service("./chromedriver.exe")
        browser = webdriver.Chrome(options=option)
        return browser

    def main(self, **info):
        if info['page'] < self.page:
            return
        brower = self.startBrower()
        print('列表页面URL:' + self.spiderUrl % (self.type, self.page))
        brower.get(self.spiderUrl % (self.type, self.page))
        time.sleep(30)
        # return
        job_list = brower.find_elements(by=By.XPATH, value="//ul[@class='job-list-box']/li")
        for index, job in enumerate(job_list):
            try:
                print("爬取的是第 %d 条" % (index + 1))
                jobData = []
                # title  工作名字
                title = job.find_element(by=By.XPATH,
                                         value=".//div[contains(@class,'job-title')]/span[@class='job-name']").text
                # address  地址
                addresses = job.find_element(by=By.XPATH,
                                             value=".//div[contains(@class,'job-title')]//span[@class='job-area']").text.split(
                    '·')
                address = addresses[0]
                # dist 行政区
                if len(addresses) != 1:
                    dist = addresses[1]
                else:
                    dist = ''
                # type  工作类型
                type = str(self.type).replace('%2F', '/').replace('%2B', '+')

                tag_list = job.find_elements(by=By.XPATH,
                                             value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li")
                if len(tag_list) == 2:
                    educational = job.find_element(by=By.XPATH,
                                                   value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li[2]").text
                    workExperience = job.find_element(by=By.XPATH,
                                                      value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li[1]").text
                else:
                    educational = job.find_element(by=By.XPATH,
                                                   value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li[3]").text
                    workExperience = job.find_element(by=By.XPATH,
                                                      value=".//div[contains(@class,'job-info')]/ul[@class='tag-list']/li[2]").text
                # hr
                hrWork = job.find_element(by=By.XPATH,
                                          value=".//div[contains(@class,'job-info')]/div[@class='info-public']/em").text
                hrName = job.find_element(by=By.XPATH,
                                          value=".//div[contains(@class,'job-info')]/div[@class='info-public']").text
                print(hrName)

                # workTag 工作标签
                workTag = job.find_elements(by=By.XPATH,
                                            value="./div[contains(@class,'job-card-footer')]/ul[@class='tag-list']/li")
                workTag = json.dumps(list(map(lambda x: x.text, workTag)))

                # salary 薪资
                salaries = job.find_element(by=By.XPATH,
                                            value=".//div[contains(@class,'job-info')]/span[@class='salary']").text
                # 是否为实习单位
                pratice = 0
                if salaries.find('K') != -1:
                    salaries = salaries.split('·')
                    if len(salaries) == 1:
                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        salaryMonth = '0薪'
                    else:
                        # salaryMonth 年底多薪
                        salary = list(map(lambda x: int(x) * 1000, salaries[0].replace('K', '').split('-')))
                        salaryMonth = salaries[1]
                else:
                    salary = list(map(lambda x: int(x), salaries.replace('元/天', '').split('-')))
                    salaryMonth = '0薪'
                    pratice = 1

                # companyTitle 公司名称
                companyTitle = job.find_element(by=By.XPATH, value=".//h3[@class='company-name']/a").text
                # companyAvatar 公司头像
                companyAvatar = job.find_element(by=By.XPATH,
                                                 value=".//div[contains(@class,'job-card-right')]//img").get_attribute(
                    "src")
                companyInfoList = job.find_elements(by=By.XPATH,
                                                    value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li")
                if len(companyInfoList) == 3:
                    companyNature = job.find_element(by=By.XPATH,
                                                     value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[1]").text
                    companyStatus = job.find_element(by=By.XPATH,
                                                     value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[2]").text
                    try:
                        companyPeople = list(map(lambda x: int(x), job.find_element(by=By.XPATH,
                                                                                    value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[3]").text.replace(
                            '人', '').split('-')))
                    except:
                        companyPeople = [0, 10000]
                else:
                    companyNature = job.find_element(by=By.XPATH,
                                                     value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[1]").text
                    companyStatus = "未融资"
                    try:
                        companyPeople = list(map(lambda x: int(x), job.find_element(by=By.XPATH,
                                                                                    value=".//div[contains(@class,'job-card-right')]//ul[@class='company-tag-list']/li[2]").text.replace(
                            '人', '').split('-')))
                    except:
                        companyPeople = [0, 10000]
                # companyTag 公司标签
                companyTag = job.find_element(by=By.XPATH,
                                              value="./div[contains(@class,'job-card-footer')]/div[@class='info-desc']").text
                if companyTag:
                    companyTag = json.dumps(companyTag.split(','))
                else:
                    companyTag = '无'

                # 详情地址
                detailUrl = job.find_element(by=By.XPATH,
                                             value="./div[@class='job-card-body clearfix']/a").get_attribute('href')
                # 公司详情
                companyUrl = job.find_element(by=By.XPATH, value="//h3[@class='company-name']/a").get_attribute('href')

                jobData.append(title)
                jobData.append(address)
                jobData.append(type)
                jobData.append(educational)
                jobData.append(workExperience)
                jobData.append(workTag)
                jobData.append(salary)
                jobData.append(salaryMonth)
                jobData.append(companyTag)
                jobData.append(hrWork)
                jobData.append(hrName)
                jobData.append(pratice)
                jobData.append(companyTitle)
                jobData.append(companyAvatar)
                jobData.append(companyNature)
                jobData.append(companyStatus)
                jobData.append(companyPeople)
                jobData.append(detailUrl)
                jobData.append(companyUrl)
                jobData.append(dist)

                self.save_to_csv(jobData)
            except:
                pass
        time.sleep(1)
        self.page += 1
        self.main(page=info['page'])

    def save_to_csv(self, rowData):
        with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(rowData)

    def clear_numTemp(self):
        with open('./numTemp.txt', 'w', encoding='utf-8') as f:
            f.write('')

    def init(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["title", "address", "type", "educational", "workExperience", "workTag", "salary", "salaryMonth",
                     "companyTags", "hrWork", "hrName", "pratice", "companyTitle", "companyAvatar", "companyNature",
                     "companyStatus", "companyPeople", "detailUrl", "companyUrl", "dist"])

    def save_to_sql(self):
        data = self.clearData()
        for job in data:
            JobInfo.objects.create(
                title=job[0],
                address=job[1],
                type=job[2],
                educational=job[3],
                workExperience=job[4],
                workTag=job[5],
                salary=job[6],
                salaryMonth=job[7],
                companyTags=job[8],
                hrWork=job[9],
                hrName=job[10],
                pratice=job[11],
                companyTitle=job[12],
                companyAvatar=job[13],
                companyNature=job[14],
                companyStatus=job[15],
                companyPeople=job[16],
                detailUrl=job[17],
                companyUrl=job[18],
                dist=job[19]
            )

        print("导入数据库成功")

        # os.remove("./temp.csv")

    def clearData(self):
        df = pd.read_csv('./temp.csv')
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        df['salaryMonth'] = df['salaryMonth'].map(lambda x: x.replace('薪', ''))
        print("总条数为%d" % df.shape[0])
        return df.values


if __name__ == '__main__':
    names = ["电气设计工程师", "集成电路IC设计", "IC验证工程师",
             "版图设计工程师", "FAE", "硬件工程师", "嵌入式", "自动化", "FPGA开发", "单片机", "驱动开发", "PCB工艺", "射频工程师", "电路设计", "系统集成",
             "光学工程师", "DSP开发", "通信项目专员", "通信项目经理", "通信技术工程师", "通信研发工程师", "无线%2F射频通信工程师", "移动通信工程师", "电信网络工程师", "数据通信工程师",
             "通信测试工程师", "光通信工程师", "光传输工程师", "光网络工程师", "通信电源工程师", "有线传输工程师", "通信设备工程师", "核心网工程师", "通信标准化工程师"]
    for name in names:
        # print(name)
        spiderObj = Spider(name, 8)
        spiderObj.init()
        spiderObj.main(page=10)
        time.sleep(1)
    # spiderObj.save_to_sql()
