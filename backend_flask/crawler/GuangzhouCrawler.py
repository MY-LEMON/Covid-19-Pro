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

jieba.load_userdict("dict.txt")

# 广州市卫健委新闻爬虫
class GetNews:
    def __init__(self):
        self.url = "http://wjw.gz.gov.cn/ztzl/xxfyyqfk/yqtb/"  # 原网址
        self.pages = 20  # todo 网站页数，等待动态返回
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50'}
        self.encoding = 'utf-8'

        self.news_url_all = []
        self.news_dict_all = []

    def get_web(self):
        self.url_all = [self.url] + [self.url + "index_" +
                                     str(i) + ".html" for i in range(2, self.pages + 1)]  # 目录网址
        self.res = [requests.get(i, headers=self.headers)
                    for i in self.url_all]  # request
        self.soup = [BeautifulSoup(i.text) for i in self.res]  # soup处理

    def get_url(self):
        '''
        获取每天url
        :return:
        '''
        for soups in range(0, self.pages - 1):
            news_a = self.soup[soups].find_all('a')
            news_all_href = []
            for i in news_a:
                if i.get("title"):
                    if "新冠肺炎疫情情况" in i.get("title"):
                        news_all_href.append(i.get('href'))
            self.news_url_all.extend(news_all_href)
        return self.news_url_all

    def get_text(self):
        '''
        获取每天url的新闻
        :param news_url_all: 全部新闻网址
        :return: news_dict_all：{}
        '''
        for url in self.news_url_all:
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

    def dump_json(self):
        with open("news_dict_all_data.json", "w") as dump_f:
            json.dump(self.news_dict_all, dump_f)

    def load_json(self):
        with open("news_dict_all_data.json", 'r') as load_f:
            self.news_dict_all = json.load(load_f)
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

    def crawler_basic(self, sentense):
        '''
        基础数据正则化
        :param sentense:
        :return:
        '''
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

    def crawler_extra(self, sentense):
        '''
        额外数据正则化
        :return:
        '''
        re3 = re.search('前往|先后乘坐|先后搭乘|搭乘', self.else_info)
        re4 = []
        if re3:
            if re3.group() == "前往":
                try:
                    re4 = re.findall(
                        r'.+?前往.+[，,](.+?日)从?(.*)乘坐(.+航班)于?(.+?)飞*抵+达*(.+?)入*境*，.+转(.+?)隔离治疗[，。](.*)', self.else_info)[
                        0]

                except IndexError:
                    re4 = ['空', '空', '空', '空', '空', '空', '空']
            elif re3.group() == "先后乘坐":
                try:
                    re4 = re.findall(
                        r'(.+?)[从于](.+?)出发[，,]先后乘坐(.+(?=航班)航班)于(.+?)飞抵(.+?)入*境*，.+转(.+?)隔离治疗[，。](.*)', self.else_info)[
                        0]
                except IndexError:
                    re4 = ['空', '空', '空', '空', '空', '空', '空']
            elif re3.group() == "先后搭乘":
                try:
                    re4 = re.findall(
                        r'(.+?)[从于](.+?)出发[，,]先后(?:搭乘)?(?:乘坐)?(.+(?=航班)航班)于(.+?)飞抵(.+?)入*境*，.+转(.+?)隔离治疗[，。](.*)',
                        self.else_info)[0]
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

    def recrawler(self):
        # 处理out_date
        match_out_time = re.search(r'(\d+)-(\d+)', self.out_date)
        if re.fullmatch(r'\d+-\d+', self.out_date):
            mouthNum = int(match_out_time.group(1))
            dayNum = int(match_out_time.group(2))
            matchRes = re.search(r'(\d+)-(\d+-\d+)', self.date)
            timeNow = time.strptime(matchRes.group(2), "%m-%d")
            timeOut = time.strptime(str(mouthNum) + '-' + str(dayNum), "%m-%d")
            if timeOut > timeNow:
                yearNum = int(matchRes.group(1)) - 1
                self.out_date = str(yearNum) + '-' + self.out_date
            else:
                self.out_date = matchRes.group(1) + '-' + self.out_date

            matchIndate = re.search(r'(\d+)日', self.in_date)
            if matchIndate:
                matchRes = re.search(r'(\d+-\d+-)\d+', self.out_date)
                self.in_date = matchRes.group(1) + matchIndate.group(1)
        if self.in_date == '当天' or self.in_date == "当日":
            self.in_date = self.out_date


class infectorData:

    def __init__(self):
        self.infectors_list = []
        self.infectors_len = 300

    def data_parser(self):
        for day in range(0, 300):
            for sentense in iter(list(news_dict_all[day].values())[0]):
                words = pseg.cut(sentense)
                words = [i for i in words]  # 迭代器转列表
                for i in range(len(words)):
                    if words[i].word == '男' or words[i].word == '女':  # 判断为感染者

                        infector = infectors(sentense)
                        strdate = str(list(news_dict_all[day].keys()))
                        matchObj = re.search(r'(([\d]+年)?[\d]+月[\d]+日)', strdate)
                        fulldate = matchObj.group(1)
                        yearstr = matchObj.group(2)
                        if yearstr == None:
                            fulldate = '2020年' + fulldate
                        fulldate = fulldate.replace('年', '-')
                        fulldate = fulldate.replace('月', '-')
                        fulldate = fulldate.replace('日', '')

                        infector.date = fulldate
                        infector.crawler_basic(sentense)
                        infector.crawler_extra(sentense)
                        self.infectors_list.append(infector)
                    if words[i].word == '相同':
                        words_info = words[i + 2:]
                        else_info = ''.join(
                            [words_info[k].word for k in range(len(words_info))])

                        for i in range(len(self.infectors_list) - 1, -1, -1):
                            if self.infectors_list[i].else_info == '':
                                self.infectors_list[i].else_info = else_info
                                self.infectors_list[i].crawler_extra(sentense)
                            else:
                                break
            for infector in iter(self.infectors_list):
                infector.recrawler()


if __name__ == '__main__':
    flag = input("是否重新爬取数据？  1.是  2.否")
    if flag == '1':
        news = GetNews()  # 类实例化
        news.get_web()
        news_url_all = news.get_url()
        news_dict_all = news.get_text()
        news.dump_json()
    elif flag == '2':
        news = GetNews()  # 类实例化
        news_dict_all = news.load_json()

    infector_data = infectorData()
    infector_data.data_parser()
    for infector in iter(infector_data.infectors_list):
        print(list(infector.__dict__.values()))
