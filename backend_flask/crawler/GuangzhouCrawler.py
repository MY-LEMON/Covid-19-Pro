import csv
from pickle import NONE
from numpy.core.numeric import full
import pandas as pd
import jieba.posseg as pseg
import jieba
import json
from bs4 import BeautifulSoup
import requests
import re
import time


class GetNews:
    def __init__(self):
        self.url = "http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/"  # 原网址
        self.pages = 20  # 页数，等待动态返回
        self.url_all = [self.url]+[self.url+"index_" +
                                   str(i)+".html" for i in range(2, self.pages+1)]  # 目录网址
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50'}
        self.encoding = 'utf-8'
        self.res = [requests.get(i, headers=self.headers)
                    for i in self.url_all]  # request
        self.soup = [BeautifulSoup(i.text) for i in self.res]  # soup处理
        self.news_url_all = []
        self.news_dict_all = []

    def __getInfo__(self):
        pass

    def __main__(self):
        pass

    # 获取每天url
    def get_url(self):
        for soups in range(0, self.pages-1):
            news_a = self.soup[soups].find_all('a')
            news_all_href = []
            for i in news_a:
                if i.get("title"):
                    if "新冠肺炎疫情情况" in i.get("title"):
                        news_all_href.append(i.get('href'))
            self.news_url_all.extend(news_all_href)
        return self.news_url_all

    # 获取每天url的新闻
    def get_text(self, news_url_all):

        for url in news_url_all:
            soup_news = BeautifulSoup(
                requests.get(url, headers=self.headers).text)
            news_text = []
            news_text_dict = {}

            for i in soup_news.find_all('p'):
                text_p = i.text
                text_p_nonSpace = ''.join(text_p.split())
                if text_p_nonSpace == "附件：":
                    break
                if text_p_nonSpace != '':
                    news_text.append(text_p_nonSpace)
            news_text_dict[soup_news.find('h4').text] = news_text
            self.news_dict_all.append(news_text_dict)

        return self.news_dict_all

class infectors:
    def __init__(self, sentense):

        self.date = '空'
        self.symptom = '空'
        self.gender = '空'
        self.age = '空'
        self.native_place = '空'
        self.permanent = '空'
        self.job = '空'
        self.else_info = '空'
        self.out_date = '空'
        self.from_place = '空'
        self.transport = '空'
        self.in_date = '空'
        self.to_place = '空'
        self.hospital = '空'
        self.chemeth = '空'
# 数据正则化

    def build_basic(self, sentense):

        try:
            re1 = re.findall(
                # r'新增\d*例*(.+?)情*况*\d*[：:](.)，(\d+(?=岁))岁，籍*贯*(.+?)[，。](.*)', sentense)[0]
                r'(?:(.+?)情*况*\d*[：:])?(.)，(\d+(?=岁))岁，籍*贯*(.+?)[，。](.*)', sentense)[0]
            re2 = re.findall(r'常住(.+?)，(.+?)。(.*)', re1[4])

        except IndexError:
            re1 = ['空', '空', '空', '空', '空']
            re2 = [['空', '空', '空']]

        self.symptom = re1[0]
        self.gender = re1[1]
        self.age = re1[2]
        self.native_place = re1[3]
        if re2:
            self.permanent = re2[0][0]
            self.job = re2[0][1]
            self.else_info = re2[0][2]
        else:
            self.else_info = re1[4]

    def build_extra(self, sentense):

        re3 = re.search('前往|先后乘坐|先后搭乘|搭乘', self.else_info)
        re4 = []
        if re3:
            if re3.group() == "前往":
                try:
                    re4 = re.findall(
                        r'.+?前往.+[，,](.+?日)从?(.*)乘坐(.+航班)于?(.+?)飞*抵+达*(.+?)入*境*，.+转(.+?)隔离治疗[，。](.*)', self.else_info)[0]

                except IndexError:
                    re4 = ['空', '空', '空', '空', '空', '空', '空']
            elif re3.group() == "先后乘坐":
                try:
                    re4 = re.findall(
                        r'(.+?)[从于](.+?)出发[，,]先后乘坐(.+(?=航班)航班)于(.+?)飞抵(.+?)入*境*，.+转(.+?)隔离治疗[，。](.*)', self.else_info)[0]
                except IndexError:
                    re4 = ['空', '空', '空', '空', '空', '空', '空']
            elif re3.group() == "先后搭乘":
                try:
                    re4 = re.findall(
                        r'(.+?)[从于](.+?)出发[，,]先后(?:搭乘)?(?:乘坐)?(.+(?=航班)航班)于(.+?)飞抵(.+?)入*境*，.+转(.+?)隔离治疗[，。](.*)', self.else_info)[0]
                except IndexError:
                    re4 = ['空', '空', '空', '空', '空', '空', '空']
            elif re3.group() == "搭乘":
                try:
                    re4 = re.findall(
                        r'(.+?)[从于](.+?)搭乘(.*航班).*，?.*于(.*)飞抵(.*)入境。?.*转(.+?)隔离治疗[，。](.*)', self.else_info)[0]
                except IndexError:
                    re4 = ['空', '空', '空', '空', '空', '空', '空']
        else:
            try:
                re4 = re.findall(
                    r'(.+?)从(.+?)乘坐(.+)于(.+?)飞*抵+达*(.+?)入*境*，.+转(.+?)隔离治疗[，。](.*)', self.else_info)[0]
            except:
                re4 = ['空', '空', '空', '空', '空', '空', '空']

        if re4[6] != '':
            if re4[6] == '空':
                self.chemeth = '空'
            else:
                if re.findall(r'新冠病毒无症状感染者', self.else_info):
                    self.chemeth = '转'
                else:
                    try:
                        self.chemeth = re.findall(
                            r'经(.*?)，诊断为.+', self.else_info)[0]
                    except:
                        self.chemeth = '空'
        else:
            self.chemeth = '空'

        self.out_date = re4[0]
        self.in_date = re4[3]
        if self.in_date == '当天' or self.in_date == "当日":
            self.in_date = self.out_date
        self.from_place = re4[1]
        self.transport = re4[2]
        self.to_place = re4[4]
        self.hospital = re4[5]

        self.out_date = self.out_date.replace('月', '-')
        self.out_date = self.out_date.replace('日', '')

        matchOutTime = re.search(r'(\d+)-(\d+)', self.out_date)

        # 处理out_date
        if(re.fullmatch(r'\d+-\d+', self.out_date)):
            mouthNum = int(matchOutTime.group(1))
            dayNum = int(matchOutTime.group(2))
            matchRes = re.search(r'(\d+)-(\d+-\d+)', self.date)
            # print(matchRes.group(2))
            timeNow = time.strptime(matchRes.group(2), "%m-%d")
            timeOut = time.strptime(str(mouthNum)+'-'+str(dayNum), "%m-%d")
            if timeOut > timeNow:
                yearNum = int(matchRes.group(1)) - 1
                self.out_date = str(yearNum)+'-' + self.out_date
            else:
                self.out_date = matchRes.group(1)+'-' + self.out_date

            matchIndate = re.search(r'(\d+)日',self.in_date)
            if matchIndate:
                matchRes = re.search(r'(\d+-\d+-)\d+',self.out_date)
                self.in_date = matchRes.group(1) + matchIndate.group(1)


    def rebuild(self):
        if self.in_date == '当天' or self.in_date == "当日":
            self.in_date = self.out_date


with open("data.json", 'r') as load_f:
    news_dict_all = json.load(load_f)

jieba.load_userdict("dict.txt")

infectors_list = []  # 感染者列表

for day in range(0, 301):

    for sentense in iter(list(news_dict_all[day].values())[0]):
        #     print(sentense)
        words = pseg.cut(sentense)
        words = [i for i in words]  # 迭代器转列表
        for i in range(len(words)):
            if words[i].word == '男' or words[i].word == '女':  # 判断为感染者
                # print(sentense)
                infector = infectors(sentense)
                strdate = str(list(news_dict_all[day].keys()))
                matchObj = re.search(r'(([\d]+年)?[\d]+月[\d]+日)', strdate)
                fulldate = matchObj.group(1)
                yearstr = matchObj.group(2)
                if yearstr == None:
                    fulldate = '2020年'+fulldate
                fulldate = fulldate.replace('年', '-')
                fulldate = fulldate.replace('月', '-')
                fulldate = fulldate.replace('日', '')

                # infector.date = ''.join(list(news_dict_all[day].keys()))[5:-11]
                infector.date = fulldate
                infector.build_basic(sentense)
                infector.build_extra(sentense)
                infectors_list.append(infector)
            if words[i].word == '相同':
                words_info = words[i+2:]
                else_info = ''.join(
                    [words_info[k].word for k in range(len(words_info))])
                # print(len(infectors_list)-1,0)
                for i in range(len(infectors_list)-1, -1, -1):
                    if infectors_list[i].else_info == '':
                        infectors_list[i].else_info = else_info
                        infectors_list[i].build_extra(sentense)
                    else:
                        break

    for infector in iter(infectors_list):
        infector.rebuild()
        # print(infector.__dict__)

with open("test.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(list(infectors_list[0].__dict__.keys()))
    for infector in iter(infectors_list):
        writer.writerow(list(infector.__dict__.values()))

df = pd.read_csv('test.csv', parse_dates=[
                 'date', 'in_date', 'out_date'], encoding='gbk')
