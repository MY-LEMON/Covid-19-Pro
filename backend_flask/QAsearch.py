from settings import *
from py2neo import Graph, Node, Relationship

class CovidGraph:
    def __init__(self):
        self.graph = Graph(NEO4J_HOST, username=NEO4J_USER, password=NEO4J_PASSWORD)

    def question_parser(self, data):
        """
        主要是根据不同的实体和意图构造cypher查询语句
        :param data
        :return:
        """
        sqls = []
        if data:
            for intent in data["intentions"]:
                sql_ = {}
                sql_["intention"] = intent
                sql = []
                if data.get("Disease"):
                    sql = self.transfor_to_sql("Disease", data["Disease"], intent)
                elif data.get("Alias"):
                    sql = self.transfor_to_sql("Alias", data["Alias"], intent)
                elif data.get("Symptom"):
                    sql = self.transfor_to_sql("Symptom", data["Symptom"], intent)
                elif data.get("Complication"):
                    sql = self.transfor_to_sql("Complication", data["Complication"], intent)

                if sql:
                    sql_['sql'] = sql
                    sqls.append(sql_)
        return sqls

    def transfor_to_sql(self, label, entities, intent):
        """
        将问题转变为cypher查询语句
        :param label:实体标签
        :param entities:实体列表
        :param intent:查询意图
        :return:cypher查询语句
        """
        if not entities:
            return []
        sql = []

        # 查询症状
        '''
        match (n:entity)-[r:relation]->(p:entity)  WHERE n.label_zh='新型冠状病毒肺炎' and r.label_zh=~'.*症状' return p.label_zh
        '''
        if intent == "query_symptom" and label == "Disease":
            sql = ["match (n:entity)-[r:relation]->(p:entity)  WHERE n.label_zh='{0}' and r.label_zh=~'.*症状' return p.label_zh".format(e)
                   for e in entities]



        return sql

    def searching(self, sqls):
        """
        执行cypher查询，返回结果
        :param sqls:
        :return:str
        """
        final_answers = []
        for sql_ in sqls:
            intent = sql_['intention']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.graph.run(query).data()
                print(ress)
            final_answer = ress
            if final_answer:
                final_answers.append(final_answer)
        return final_answers
