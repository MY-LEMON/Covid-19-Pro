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
                sql_sent = []  # 单一答案，用于写人话
                sql_graph = []  # 节点+关系，用于画图谱
                if data.get("Disease"):
                    sql_sent = self.transfor_to_sql("Disease_sent", data["Disease"], intent)
                    sql_graph = self.transfor_to_sql("Disease_graph", data["Disease"], intent)
                elif data.get("Alias"):
                    sql_sent = self.transfor_to_sql("Alias", data["Alias"], intent)
                    sql_graph = self.transfor_to_sql("Alias", data["Alias"], intent)
                elif data.get("Symptom"):
                    sql_sent = self.transfor_to_sql("Symptom", data["Symptom"], intent)
                    sql_graph = self.transfor_to_sql("Symptom", data["Symptom"], intent)
                elif data.get("Complication"):
                    sql_sent = self.transfor_to_sql("Complication", data["Complication"], intent)
                    sql_graph = self.transfor_to_sql("Complication", data["Complication"], intent)
                if sql_sent:
                    sql_['sql_sent'] = sql_sent
                if sql_graph:
                    sql_['sql_graph'] = sql_graph
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
        if intent == "query_symptom" and label == "Disease_sent":
            sql = [
                "match (n:entity)-[r:relation]->(p:entity)  WHERE n.label_zh='{0}' and r.label_zh=~'.*症状' return n.label_zh,p.label_zh".format(
                    e) for e in entities]
        if intent == "query_symptom" and label == "Disease_graph":
            sql = [
                "".format(e) for e in entities]
        #

        return sql

    def searching(self, sqls):
        """
        执行cypher查询，返回结果
        :param sqls:
        :return:str
        """
        final_answers = []  # 返回给前端的string
        node_relation = []  # 返回给前端用于构建图谱的json

        for sql_ in sqls:
            intent = sql_['intention']

            queries_sent = sql_['sql_sent']
            for query in queries_sent:
                resp = self.graph.run(query).data()
                print(resp)
                if resp:
                    answer = self.answer_template(intent, resp)
                    final_answers.append(answer)

            queries_graph = sql_['sql_graph']
            for query in queries_graph:
                resp = self.graph.run(query).data()
                print(resp)
                if resp:
                    node_relation.append(resp)

        return final_answers, node_relation

    [{'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '呼吸困难'}, {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '咽痛'},
     {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '流涕'}, {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '腹泻'},
     {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '乏力'}, {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '脓毒症休克'},
     {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '多器官功能衰竭'}, {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '急性呼吸窘迫综合征'},
     {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '鼻塞'}, {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '干咳'},
     {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '低氧血症'}, {'n.label_zh': '新型冠状病毒肺炎', 'p.label_zh': '发热'}]

    def answer_template(self, intent, answers):
        """
        根据不同意图，返回不同模板的答案
        :param intent: 查询意图
        :param answers: 知识图谱查询结果
        :return: str
        """
        final_answer = ""
        if not answers:
            return ""
        # 查询症状
        if intent == "query_symptom":
            disease_dic = {}
            for data in answers:
                n = data['n.label_zh']
                p = data['p.label_zh']
                if n not in disease_dic:
                    disease_dic[n] = [p]
                else:
                    disease_dic[n].append(p)
            for k, v in disease_dic.items():
                final_answer += "疾病 {0} 的症状有：{1}\n".format(k, ','.join(list(set(v))))

        return final_answer