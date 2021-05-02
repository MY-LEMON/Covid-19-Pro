import requests
import json
import pandas as pd
import time
import os


class GetDataApi:
    def __init__(self):
        self.url = "https://lab.isaaclin.cn/nCoV/"  # 原网址
        self.url_area = 'api/area?latest=1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50'}
        self.encoding = 'utf-8'
        self.res = ''
        self.data = ''

        self.data_china = []
        self.data_province = {}
        self.countries_bar = {'country': [], 'data': []}
        self.countries_pie = {}
        self.provinces_bar = {'country': [], 'data': []}
        self.provinces_pie = {}

        self.load_data()
        self.get_china_data()
        self.get_province_data()
        self.get_data_chart()

        self.dict2front = {"China": self.data_china, "Provinces": self.data_province,
                           "bar_country": self.countries_bar, "bar_province": self.provinces_bar,
                           "pie_country": self.countries_pie, "pie_province": self.provinces_pie}

    def load_data(self):
        if not os.path.exists("./data_covid19/" + time.strftime("%Y%m%d", time.localtime()) + "data.json"):
            self.res = requests.get(self.url + self.url_area, headers=self.headers)  # request
            self.data = self.res.content.decode(self.encoding)

            self.data_dict = json.loads(self.data)
            with open("./data_covid19/" + time.strftime("%Y%m%d", time.localtime()) + "data.json", "w") as f:
                json.dump(self.data_dict, f)
        else:
            with open("./data_covid19/" + time.strftime("%Y%m%d", time.localtime()) + "data.json", 'r') as load_f:
                self.data_dict = json.load(load_f)

    def get_china_data(self):
        china = []

        for pro in self.data_dict['results']:
            city_data = {'name': '', 'value': []}
            if pro['countryName'] == '中国':
                china.append(pro)
                city_data['name'] = pro['provinceShortName']
                city_data['value'] = [pro['confirmedCount'], pro['suspectedCount'], pro['curedCount'],
                                      pro['deadCount'], pro['currentConfirmedCount']]
                self.data_china.append(city_data)

        return self.data_china

    def get_province_data(self):
        province = []

        for pro in self.data_dict['results']:
            if pro['countryName'] == '中国' and pro['provinceName'] != '中国':
                province.append(pro)
                self.data_province[pro['provinceEnglishName']] = []
                for city in pro['cities']:
                    city_data = {'name': city['cityName'],
                                 'value': [city['confirmedCount'], city['suspectedCount'], city['curedCount'],
                                           city['deadCount'], city['currentConfirmedCount']]}
                    self.data_province[pro['provinceEnglishName']].append(city_data)

        return self.data_province

    def get_data_chart(self):
        countries = {}
        provinces = {}
        for pro in self.data_dict['results']:
            if pro['countryName'] == pro['provinceName'] and pro['currentConfirmedCount'] >= 0:
                countries[pro['countryName']] = pro['currentConfirmedCount']
            elif pro['countryName'] == '中国' and pro['provinceName'] != '中国' and pro['currentConfirmedCount'] >= 0:
                provinces[pro['provinceName']] = pro['currentConfirmedCount']
        for ct in sorted(countries.items(), key=lambda item: item[1], reverse=True):
            self.countries_bar['country'].append(ct[0])
            self.countries_bar['data'].append(ct[1])
            self.countries_pie[ct[0]] = ct[1]
        for ct in sorted(provinces.items(), key=lambda item: item[1], reverse=True):
            self.provinces_bar['country'].append(ct[0])
            self.provinces_bar['data'].append(ct[1])
            self.provinces_pie[ct[0]] = ct[1]

        print(self.countries_bar, self.countries_pie, self.provinces_bar, self.provinces_pie)


class GetDataCsv:
    def __init__(self):
        self.vaccinations = pd.read_csv(r'data_csv/vaccinations.csv')
        self.vaccinations_data = pd.read_csv('data_csv/data_vaccinations.csv')
        self.confirmed_global = pd.read_csv('data_csv/time_series_covid19_confirmed_global.csv')
        self.deaths_global = pd.read_csv('data_csv/time_series_covid19_deaths_global.csv')
        self.recovered_global = pd.read_csv('data_csv/time_series_covid19_recovered_global.csv')
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

    def get_time_series_data(self, df):
        result = df.groupby(['Country/Region']).sum().drop(['Lat', 'Long'],
                                                           axis=1).stack()  # 由于美国等国数据是按二级行政区划提供的，需按国家进行汇总
        result = result.reset_index()
        result.columns = ['Country', 'date', 'value']
        result['date_'] = pd.to_datetime(result.date)  # 生成时间索引
        result = result.sort_values(by='date_', axis=0, ascending=True)  # 按时间排序
        result = result.replace('\*', '', regex=True)  # 去掉国名中的*

        country_list = result.Country.drop_duplicates()
        temp = result.copy()
        re = pd.DataFrame()
        for i in country_list:  # 按国家分别进行重抽样，并合并数据
            r_temp = temp.loc[temp.Country == i]
            r_temp = r_temp.drop_duplicates(['date_'])
            r_temp = r_temp.set_index('date_')
            r_temp = r_temp.resample('W').asfreq().dropna()
            r_temp = r_temp.reset_index()
            re = pd.concat([re, r_temp])
        return re.sort_values(by='date_',axis=0,ascending=True)


if __name__ == "__main__":

    # get_data = GetDataApi()
    # resData = {
    #     "resCode": 0,  # 非0即错误 1
    #     "data": get_data.dict2front,  # 数据位置，一般为数组
    #     "message": '搜索结果'
    # }
    # import json
    #
    # with open("charts_data2front.json", "w", encoding='utf-8') as f:
    #     json.dump(resData, f, ensure_ascii=False)

    get_data_csv = GetDataCsv()
    data = get_data_csv.get_time_series_data(get_data_csv.confirmed_global)

    print(data)
