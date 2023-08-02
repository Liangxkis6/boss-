import random
import re

import pymysql
import requests
from bs4 import BeautifulSoup

cookie = '__snaker__id=jPZ1BUxntnWz1Bvw; wd_guid=21cf3f35-9204-4d40-9a0f-3fc44042133c; historyState=state; _bl_uid=2wl95kOhdptm2UiypuaCkaygRqyw; lastCity=101250100; YD00951578218230:WM_NI=9sVL6Bqio7/i6d7nWNNlt3DFl+TpjCXzCfHCnYs34+GOencGnCRWrjTS8A9cLw04aM4ebebQUyslSrsgFBYNceXAas4DFbR2jGAi4ncW9ojZu4x5a7agFz6bqpSKHNBwdW4=; YD00951578218230:WM_NIKE=9ca17ae2e6ffcda170e2e6eea3cb7ab3f18588ec659b928fa3d85f929b8ab1c164f89f9b89f56a958bfed6c62af0fea7c3b92afbad9aadb54ab3b7a1d8ae63f6bcf98fd6468eb4bcd4c74eb0f59c91e9499ca68d87cb49ae87bdd4b7218591ab8fe24dae9d9eb8f162988df8a2bc6990a900d5e447f8bbae86e15b97a7bd8dd27ab1b98aa3dc46a1bb98a2e479f89c8a83d13aaa998f8ab766a189f790e952b7ecb8d6e43da3b98a9bb56ab3b09daccb4682a9acb8b737e2a3; YD00951578218230:WM_TID=EMIhpIRpT6xABABUQFPVhsEQh+bCUnoG; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1690006985,1690033035,1690078527,1690080544; __fid=f182e1d8b53c6a765a84902e2866e38e; boss_login_mode=sms; gdxidpyhxdE=U9O0fheVj/U\vUx8gtbaq5TfGAyzSvuiG64cZGcti2SMP3puavXhkVDZ/C7BNooa8l+iDxKUQmwIYGAACq1oENK\osB64ucan5IDI/Gz+P14zoR60BZ\/GgErnGEnroCpClnEzC\IRIj3kzZfU7OgKnSy1jvZJHMzDkCBd/CHhjIL17w:1690097346414; wt2=DjZXZ_mhEPZJqyWfp9lvYO-BJpi-uDDTHisuwsAhS1mJpbdwARBAm5zizpqxBgYHQzIj_gHBH2t1YqNU3Qt2Ycg~~; wbg=0; __l=l=/www.zhipin.com/web/geek/job?query=%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8%2AI%E8%AE%AD%E7%BB%83%E5%B8%88&city=100010000&page=4&r=&g=&s=3&friend_source=0&s=3&friend_source=0; __c=1690080516; __a=39789500.1690006984.1690078526.1690080516.3525.4.1896.3525; geek_zp_token=V1R9smGOz12ldqVtRvxh0YICyy7D7fxy8~; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1690096666; __zp_stoken__=e346eC3ZEOngMMxsNIl4tej5lahdMcTEpdCF2FWBkS1pBTCMIPXhQJgkfK3NNQG5Sfm5fE05VJAduEnRdM2dkdnEUQBABRCdQZHsdEhQkNmxGCSxiISFHVQobBm4TSwkuPFdtbD9fUA1RIXo='
conn = pymysql.connect(
    host="127.0.0.1",
    user="root", password="root",
    database="test",
    charset="utf8")
cursor = conn.cursor()

base_url = "https://www.zhipin.com"

job_type = ["Java", "PHP", "web前端", "iOS", "Android", "算法工程师", "数据分析师", "数据架构师", "数据挖掘", "人工智能", " 机器学习", "深度学习"]
city_name = ["北京", "上海", "广州", "深圳", "杭州", "天津", "西安", "苏州", "武汉", "厦门", "长沙", "成都", "郑州", "重庆"]
city_num = ["c101010100", "c101020100", "c101280100", "c101280600", "c101210100", "c101030100", "c101110100",
            "c101190400", "c101200100", "c101230200",
            "c101250100", "c101270100", "c101180100", "c101040100"]


def get_user_agent():
    user_list = [
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
        "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
        "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
        "Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00",
        "Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00",
        "Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0",
        "Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62",
        "Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52",
        "Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51",
        "Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50",
        "Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50",
        "Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (X11; Linux i686; U; es-ES) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11",
        "Opera/9.80 (X11; Linux x86_64; U; bg) Presto/2.8.131 Version/11.10",
        "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10",
        "Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10",
        "Opera/9.80 (Windows NT 6.1; Opera Tablet/15165; U; en) Presto/2.8.149 Version/11.1",
        "Opera/9.80 (X11; Linux x86_64; U; Ubuntu/10.10 (maverick); pl) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (X11; Linux i686; U; ja) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (X11; Linux i686; U; fr) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; en-US) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; cs) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 5.1; U;) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01",
        "Mozilla/5.0 (Windows NT 6.1; U; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01",
        "Mozilla/5.0 (Windows NT 6.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; de) Opera 11.01",
        "Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (X11; Linux i686; U; it) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.6.37 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; ko) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1 x64; U; en) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.7.39 Version/11.00"
    ]
    user_agent = random.choice(user_list)
    return user_agent


def get_page(url):
    headers = {
        'user-agent': "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'cookie': cookie,
        'cache-control': "no-cache",
        'referer': 'https://www.zhipin.com/?ka=header-home'

    }

    try:
        response = requests.get(url, headers=headers)
        print(response)
        print(response.status_code)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            return response.text


    except requests.ConnectionError as e:
        print('Error', e.args)


def translate(str):
    line = str.strip()  # 处理前进行相关的处理，包括转换成Unicode等
    pattern = re.compile('[^\u4e00-\u9fa50-9]')  # 中文的编码范围是：\u4e00到\u9fa5
    zh = " ".join(pattern.split(line)).strip()
    outStr = zh  # 经过相关处理后得到中文的文本
    return outStr


def get_job(url, conn, cursor, city_name_x):
    html = get_page(url)
    soup = BeautifulSoup(html, 'lxml')
    job_all = soup.find_all('div', class_="job-primary")
    if (job_all == []):
        print("cookie已过期")
    for job in job_all:
        try:
            # 职位名
            job_title = job.find('span', class_="job-name").string
            # 薪资
            job_salary = job.find('span', class_="red").string
            # 职位标签
            job_tag1 = job.p.text
            # 公司
            job_company = job.find('div', class_="company-text").a.text
            # 招聘详情页链接
            job_url = base_url + job.find('div', class_="company-text").a.attrs['href']
            # 公司标签
            job_tag2 = job.find('div', class_="company-text").p.text
            # 发布时间
            job_time = job.find('span', class_="job-pub-time").text

            job_acquire = translate(str(job.find('p')))
            print(job_title, job_salary, job_tag1, job_company, job_url, job_tag2, job_time, job_acquire, city_name_x)
            store_data(job_title, job_salary, job_tag1, job_company, job_url, job_tag2, job_time, job_acquire,
                       city_name_x, conn, cursor, )

        except Exception as e:
            print(str(e))


def store_data(job_title1, job_salary1, job_lable1, job_company1, job_url1, job_company_tag1, job_time1, job_acquire1,
               company_city1, conn, cursor):
    try:
        cursor.execute(
            'insert into job_data (job_title,job_salary,job_lable,job_company,job_url,job_company_tag,job_time,job_acquire,company_city) '
            'values ("{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(job_title1, job_salary1, job_lable1,
                                                                           job_company1, job_url1,
                                                                           job_company_tag1, job_time1,
                                                                           job_acquire1, company_city1))
    except:
        print("存入数据库失败")

    conn.commit()


city_no = 5  # 城市编号
page = str(1)
key = job_type[11]
url = base_url + "/" + "c101190100" + "/?" + "query=" + key + "&page=" + page + "&ka=page-" + page
print(url)
get_job(url=url, conn=conn, cursor=cursor, city_name_x="南京")

cursor.close()
conn.close()

