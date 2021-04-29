import newspaper
from settings import news_html_dir
from bs4 import BeautifulSoup
import requests
import re
import time

total = 100
group = 10
news_title = []
news_text = []
today = time.strftime("%Y.%m.%d", time.localtime())



def newsUrl(url):
    news_build = newspaper.build(url, language='zh', memoize_articles=False)  # 构建新闻源
    news = news_build.articles
    print(news)

    for j in range(0, total, group):
        for i in range(group):
            paper = news[j]
            try:
                paper.download()
                paper.parse()
                news_title.append(paper.title)
                news_text.append(paper.text)
            except:
                news_title.append('NULL')
                news_text.append('NULL')
                print("当前读取新闻失败")
                continue
            j = j + 1
        print(j, '_' * 30)


class GetNews:
    def __init__(self):
        self.url = "https://new.qq.com/ch/antip/"  # 原网址
        self.pages = 20  # 页数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50'}
        self.encoding = 'utf-8'
        self.res = requests.get(self.url, headers=self.headers)  # request
        self.news_info = []

    def get_text(self):

        with open(news_html_dir + today +'.html', "rb") as f:
            html_text = f.read()
            f.close()

        soup_news = BeautifulSoup(html_text, "html5lib")

        for news in soup_news.find_all('li', class_='item cf itme-ls'):
            info = {"id_news": "", "abstract_news": "", "src_news": "", "imgs_news": []}
            picture = news.find('a', class_='picture')
            if picture:
                info["src_news"] = picture.get('href')
                info["id_news"] = ''.join(re.findall(r'.*/(.+?).html', info["src_news"]))
                img = news.find_all('img')
                for i in img:
                    info["abstract_news"] = i.get('alt')
                    info["imgs_news"].append(i.get('src'))
                self.news_info.append(info)

        for news3 in soup_news.find_all('li', class_='item-pics cf itme-ls'):
            info = {"id_news": "", "abstract_news": "", "src_news": "", "imgs_news": []}
            picture = news3.find('a', class_='cf pics')
            if picture:
                info["src_news"] = picture.get('href')
                info["id_news"] = ''.join(re.findall(r'.*/(.+?).html', info["src_news"]))
                img = news3.find_all('img')
                for i in img:
                    info["abstract_news"] = i.get('alt')
                    info["imgs_news"].append(i.get('src'))
                self.news_info.append(info)
        print(self.news_info)

        return self.news_info


if __name__ == "__main__":
    news = GetNews()
    news.get_text()
