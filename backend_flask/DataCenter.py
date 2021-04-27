import requests
import json
import pandas as pd
import numpy as np


class GetData:
    def __init__(self):
        self.url = "https://lab.isaaclin.cn/nCoV/"  # 原网址
        self.url_area = 'api/area?latest=1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50'}
        self.encoding = 'utf-8'
        self.res = requests.get(self.url + self.url_area, headers=self.headers)  # request
        self.data = self.res.content.decode(self.encoding)

        self.data_china_2front = []

    def get_china_data(self):
        data_dict = json.loads(self.data)
        data_china = []

        for city in data_dict['results']:
            city_data = {'name': '', 'value': []}
            if city['countryName'] == '中国':
                data_china.append(city)
                city_data['name'] = city['provinceShortName']
                city_data['value'] = [city['confirmedCount'], city['suspectedCount'], city['curedCount'],
                                      city['deadCount'], city['currentConfirmedCount']]
                self.data_china_2front.append(city_data)


class CsvData:
    def __init__(self):
        self.vaccinations = pd.read_csv(r'data_csv/vaccinations.csv')
        self.vaccinations_data = pd.read_csv('data_csv/data_vaccinations.csv')
        self.head_num = 20

    def get_vaccinations_data(self):
        self.vaccinations.index = self.vaccinations.location
        self.vaccinations = self.vaccinations.drop(
            ['World', 'Asia', 'North America', 'Europe', 'Africa', 'European Union', 'South America'])
        self.vaccinations.reset_index(drop=True, inplace=True)
        for i in self.vaccinations.location.unique():  # 遍历国家
            for j in self.vaccinations.date.unique():  # 遍历日期
                if self.vaccinations.loc[
                    (self.vaccinations.location == i) & (self.vaccinations.date == j)].empty:  # 如果该日期没有数据，新增一行空数据
                    temp = pd.DataFrame({'location': i, 'date': j}, index=['new'])
                    self.vaccinations = pd.concat([self.vaccinations, temp])
        self.vaccinations['date_'] = pd.to_datetime(self.vaccinations.date)  # 创建时间序列
        self.vaccinations = self.vaccinations.sort_values(by='date_')  # 按时间排序
        temp1 = pd.DataFrame()
        for i in self.vaccinations.location.unique():  # 按国家补全数据
            r = self.vaccinations.loc[self.vaccinations.location == i]
            r = r.fillna(method='ffill', axis=0)  # 先按最近一次数据进行补全
            temp1 = pd.concat([temp1, r])
        temp1 = temp1.fillna(0)  # 若仍有空值，认为是0

        # 为了减少可视化的数据量，保留总接种量及每百人接种量最高的10个国家
        country1 = list(
            temp1.reset_index(drop=True).groupby('location').total_vaccinations.max().sort_values(ascending=False).head(
                self.head_num).index)
        country2 = list(
            temp1.reset_index(drop=True).groupby('location').total_vaccinations_per_hundred.max().sort_values(
                ascending=False).head(self.head_num).index)
        country1.extend(country2)
        country_list = set(country1)
        drop_list = list(set(temp1.location.unique()) - country_list)

        # 排除其余数据
        temp1.index = temp1.location
        temp1.drop(drop_list, inplace=True)
        temp1.reset_index(drop=True, inplace=True)

        temp1.to_csv('data_csv/data_vaccinations.csv')


if __name__ == "__main__":
    get_data = CsvData()
    data = get_data.vaccinations_data
    print(data)
