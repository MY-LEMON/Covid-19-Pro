from pymysql import connect
from pymysql.cursors import DictCursor  # 为了返回字典形式
from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
import logging
from crawler.NewsCrawler import GetNews
import json

logging.basicConfig(level=logging.NOTSET)  # 设置日志级别


class News(object):
    def __init__(self):  # 创建对象同时要执行的代码
        self.conn = connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset='utf8'
        )
        self.cursor = self.conn.cursor(DictCursor)  # 这个可以让他返回字典的形式

        self.db_sum = self.get_db_sum()

    def __del__(self):  # 释放对象同时要执行的代码
        self.cursor.close()
        self.conn.close()

    def get_db_sum(self):
        sql = 'SELECT count(*) FROM covid19.news;'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()[0]['count(*)']
        return data


    def insert_news(self):
        get_news = GetNews()
        news_list = get_news.get_text()
        # sql = "insert into covid19.news values('20210426A06FS300','印度疫情发酵，哪些行业受冲击最大？','https://new.qq.com/omn/20210426/20210426A06FS300.html','http://inews.gtimg.com/newsapp_ls/0/13458082131_640330/0')"
        # try:
        #     self.cursor.execute(sql)
        #     self.conn.commit()
        #     logging.info('成功插入')
        # except:
        #     self.conn.rollback()
        #     logging.info('插入失败')
        for new in iter(news_list):
            sql = "insert into covid19.news values('{0}','{1}','{2}','{3}')".format(new['id_news'],
                                                                                    new['abstract_news'],
                                                                                    new['src_news'],
                                                                                    ','.join(new['imgs_news']))
            print(sql)
            try:
                self.cursor.execute(sql)
                self.conn.commit()
                logging.info('成功插入', new['abstract_news'])
            except:
                self.conn.rollback()
                logging.info('插入失败', new['abstract_news'])

    def get_news_limit(self, index_a, index_b):
        limit_num = int(index_b) - int(index_a)  # 索引（3，5）则返回3，4两条数据
        sql = 'SELECT * FROM covid19.news order by id_news desc limit {0},{1}'.format(index_a, limit_num)
        self.cursor.execute(sql)
        data = []
        for temp in self.cursor.fetchall():
            news_data = {"id": temp["id_news"], "abstract": temp["abstract_news"], "src": temp["src_news"],
                         "imgs": temp["imgs_news"].split(',')}
            data.append(news_data)
        return data


if __name__ == "__main__":
    news = News()
    print(news.insert_news()) # 每日新闻爬取，创建好html后需运行一次
    from_key = 280
    to_key = 290
    total = to_key - from_key
    from_key = from_key % news.db_sum
    to_key = from_key + total
    print(from_key,to_key)
    print(news.get_news_limit(from_key, to_key))

    resData = {
        "resCode": 0,  # 非0即错误 1
        "data": news.get_news_limit(3, 5),  # 数据位置，一般为数组
        "message": '搜索结果'
    }
    import json

    with open("news_data2front.json", "w", encoding='utf-8') as f:
        json.dump(resData, f, ensure_ascii=False)
