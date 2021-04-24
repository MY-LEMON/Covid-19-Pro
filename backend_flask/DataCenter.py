import requests
import json

class GetData:
    def __init__(self):
        self.url = "https://lab.isaaclin.cn/nCoV/"  # 原网址
        self.url_area = 'api/area?latest=1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50'}
        self.encoding = 'utf-8'
        self.res = requests.get(self.url+self.url_area, headers=self.headers)  # request
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
        


if __name__ == "__main__":
    get_data = GetData()
    get_data.get_china_data()
    data = get_data.data_china_2front
    print(data)