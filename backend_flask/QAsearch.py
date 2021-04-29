from settings import *
from py2neo import Graph, Node, Relationship
import random
from settings import NODE_COLORS


class CovidGraph:
    def __init__(self):
        self.graph = Graph(NEO4J_HOST, username=NEO4J_USER, password=NEO4J_PASSWORD)
        self.name_dict = ["Disease", "Alias", "Symptom", "Complication", "infectorname", "place", "date", "transport",
                          "hospital", "type"]

    def question_parser(self, data):

        """
        主要是根据不同的实体和意图构造cypher查询语句
        :param data
        :return:return:格式[{意图：***，CQL语句：，sql_graph：]
        """
        sqls = []
        print(data, "*********this is data 函数question_parser********")
        if data:
            for intent in data["intentions"]:
                sql_ = {}
                sql_["intention"] = intent
                sql_['sql_sent'] = []
                sql_['sql_graph'] = []
                sql_sent = []  # 单一答案，用于写人话
                sql_graph = []  # 节点+关系，用于画图谱
                for name in iter(self.name_dict):
                    if data.get(name):
                        sql_sent = self.transfor_to_sql(name + "_sent", data[name], intent)
                        sql_graph = self.transfor_to_sql(name + "_graph", data[name], intent)
                    if sql_sent:
                        sql_['sql_sent'] = sql_sent
                    if sql_graph:
                        sql_['sql_graph'] = sql_graph
                    if sql_['sql_sent'] or sql_['sql_graph']:
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
        entity = ''
        for e in entities:
            entity = entity + e
        # 查询症状
        if intent == "query_symptom" and label == "Disease_sent":
            sql = [
                "match (n:entity)-[r:relation]->(p:entity)  WHERE n.label_zh='{0}' and r.label_zh=~'.*症状' return n.label_zh,p.label_zh".format(
                    e) for e in entities]
        if intent == "query_symptom" and label == "Disease_graph":
            sql = [
                "match (n:entity)-[r:relation]->(p:entity)  WHERE n.label_zh='{0}' and r.label_zh=~'.*症状' return id(n),properties(n),properties(r),id(p),properties(p)".format(
                    e) for e in entities]

        # 查询传播方式
        if intent == "query_route" and label == "Disease_sent":
            sql = [
                "match (n:entity)-[r:relation]-(p:entity) WHERE n.label_zh=~'新型冠状病毒.*'and r.label_zh=~'.+传播途径' return distinct n.label_zh,p.label_zh".format(
                    entity)]
        if intent == "query_route" and label == "Disease_graph":
            sql = [
                "match (n:entity)-[r:relation]-(p:entity) WHERE n.label_zh=~'新型冠状病毒.*'and r.label_zh=~'.+传播途径' return distinct id(n),properties(n),properties(r),id(p),properties(p)".format(
                    entity)]

        # 查询治疗方法
        if intent == "query_cureway" and label == "Disease_sent":
            sql = [
                "match (n:entity)WHERE exists (n.`治疗方法`) and n.label_zh = '{}' return distinct n.label_zh,n.`治疗方法` AS Treatment".format(
                    entity)]
        if intent == "query_cureway" and label == "Disease_graph":
            sql = [
                "".format(entity)]

        # 查询新冠是什么
        if intent == "query_cov" and label == "Disease_sent":
            sql = [
                "match (n:entity)-[r:relation]-(p:entity)  WHERE n.label_zh='新型冠状病毒肺炎' return distinct properties(n)".format(
                    entity)]
        if intent == "query_cov" and label == "Disease_graph":
            sql = [
                "match (n:entity)-[r:relation]->(p:entity)  WHERE n.label_zh='新型冠状病毒肺炎'return id(n),"
                "properties(n),properties(r),id(p),properties(p)".format(entity)]

            # 查询科室
        if intent == "query_belong" and label == "Disease_sent":
            sql = [
                "match (n:entity)-[r:relation]->(p:entity) WHERE r.label_zh='医学专科' and n.label_zh = '{}' return distinct n.label_zh,p.label_zh".format(
                    entity)]
        if intent == "query_belong" and label == "Disease_graph":
            sql = [
                "match (n:entity)-[r:relation]->(p:entity) WHERE r.label_zh='医学专科' and n.label_zh = '{}' return distinct id(n),properties(n),properties(r),id(p),properties(p)".format(
                    entity)]

        # 查询预防方法
        if intent == "query_prevent" and label == "Disease_sent":
            sql = [
                "match (n:entity)WHERE exists (n.`预防`) and n.label_zh='{}' return distinct n.label_zh,n.`预防` AS `prevention`".format(
                    entity)]
        if intent == "query_prevent" and label == "Disease_graph":
            sql = [
                "".format(entity)]

        # 查询就诊医院
        if intent == "query_hospital" and label == "infectorname_sent":
            sql = [
                "match (n:`病例`)-[r:`就诊`]-(p:`医院`) where n.`名称`='{0}' return n.名称,p.名称".format(entities[-1])]
        if intent == "query_hospital" and label == "infectorname_graph":
            sql = [
                "match (n:`病例`)-[r:`就诊`]-(p:`医院`) where n.`名称`='{0}' return n.名称,p.名称".format(entities[-1])]

        # 查询出发地
        if intent == "query_sp" and label == "infectorname_sent":
            sql = [
                "match (n:`病例`)-[r:`出发地点`]-(p:`地点`) where n.`名称`='{0}' return n.名称,p.名称".format(entities[-1])]
        if intent == "query_hospital" and label == "infectorname_graph":
            sql = [
                "match (n:`病例`)-[r:`出发地点`]-(p:`地点`) where n.`名称`='{0}' return n.名称,p.名称".format(entities[-1])]

        # 查询某天确诊人数
        if intent == "query_def" and label == "date_sent":
            sql = [
                "match (n:`病例`)-[r:`境外输入无症状感染者`]-(p:`日期`) where p.`名称`='2月21日' return n.名称,p.名称".format(entities[-1])]
        if intent == "query_hospital" and label == "infectorname_graph":
            sql = [
                "match (n:`病例`)-[r:`境外输入无症状感染者`]-(p:`日期`) where p.`名称`='2月21日' return n.名称,p.名称".format(entities[-1])]

        print(sql, "*********this is sql 函数trans********")
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
                    data_json = self.data2json(resp)
                    node_relation.append(data_json)

        return final_answers, node_relation

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

        if intent == "query_route":
            disease_dic = {}
            for data in answers:
                n = data['n.label_zh']
                p = data['p.label_zh']
                if n not in disease_dic:
                    disease_dic[n] = [p]
                else:
                    disease_dic[n].append(p)
            for k, v in disease_dic.items():
                final_answer += "疾病 {0} 的传播方式有：{1}\n".format(k, ','.join(list(set(v))))

        if intent == "query_cureway":
            disease_dic = {}
            for data in answers:
                n = data['n.label_zh']
                p = data['Treatment']
                if n not in disease_dic:
                    disease_dic[n] = [p]
                else:
                    disease_dic[n].append(p)
            for k, v in disease_dic.items():
                final_answer += "疾病 {0} 的治疗方式有：{1}\n".format(k, ','.join(list(set(v))))

        if intent == "query_belong":
            disease_dic = {}
            for data in answers:
                n = data['n.label_zh']
                p = data['p.label_zh']
                if n not in disease_dic:
                    disease_dic[n] = [p]
                else:
                    disease_dic[n].append(p)
            for k, v in disease_dic.items():
                final_answer += "疾病 {0} 应该挂：{1}\n".format(k, ','.join(list(set(v))))

        if intent == "query_prevent":
            disease_dic = {}
            for data in answers:
                n = data['n.label_zh']
                p = data['prevention']
                if n not in disease_dic:
                    disease_dic[n] = [p]
                else:
                    disease_dic[n].append(p)
            for k, v in disease_dic.items():
                final_answer += "疾病 {0} 的预防方法是：{1}\n".format(k, ','.join(list(set(v))))

        if intent == "query_cov":
            print(answers[0]['properties(n)']['症状'])
            n = [answers[0]['properties(n)']['症状'], answers[0]['properties(n)']['潜伏期'],
                 answers[0]['properties(n)']['转运原则'], answers[0]['properties(n)']['临床表现'],
                 answers[0]['properties(n)']['解除隔离和出院标准'], answers[0]['properties(n)']['临床治疗期重症期表现']]
            final_answer = "新型冠状病毒肺炎有以下特征:\n症状：{0}\n潜伏期：{1}\n转运原则:{2}\n临床表现：{3}\n解除隔离和出院标准:\n{4}\n临床治疗期重症期表现:{5}".format(
                n[0],
                n[1], n[2], n[3], n[4], n[5])
            # print(final_answer)

        if intent == "query_hospital":
            hospital_dic = {}
            for data in answers:
                n = data['n.名称']
                p = data['p.名称']
                if n not in hospital_dic:
                    hospital_dic[n] = [p]
                else:
                    hospital_dic[n].append(p)
            for k, v in hospital_dic.items():
                final_answer += "{0}的就诊医院是：{1}\n".format(k, ','.join(list(set(v))))

        if intent == "query_sp":
            sp_dic = {}
            for data in answers:
                n = data['n.名称']
                p = data['p.名称']
                if n not in sp_dic:
                    sp_dic[n] = [p]
                else:
                    sp_dic[n].append(p)
            for k, v in sp_dic.items():
                final_answer += "{0}是从{1}出发的\n".format(k, ','.join(list(set(v))))

        if intent == "query_def":
            def_dic = {}
            for data in answers:
                n = data['n.名称']
                p = data['p.名称']
                if p not in def_dic:
                    def_dic[p] = [n]
                else:
                    def_dic[p].append(n)
            for k, v in def_dic.items():
                final_answer += "{0}确诊的病例有：{1}\n".format(k, ','.join(list(set(v))))

        return final_answer

    def data2json(self, resp):

        rootID = resp[0]['id(n)']
        nodes = []
        links = []
        color_dict = {}
        color_list = random.sample(NODE_COLORS, len(NODE_COLORS))  # 随机取出一组颜色
        for nrp in iter(resp):

            node_a = {'id': '', 'name': '', 'data': {}}
            node_b = {'id': '', 'name': '', 'data': {}}
            link = {'from': '', 'to': '', 'text': '', 'data': {}}

            node_a['id'] = str(nrp['id(n)'])
            node_a['name'] = nrp['properties(n)']['label_zh']
            node_a['data'] = nrp['properties(n)']

            node_b['id'] = str(nrp['id(p)'])
            node_b['name'] = nrp['properties(p)']['label_zh']
            node_b['data'] = nrp['properties(p)']

            link['from'] = node_a['id']
            link['to'] = node_b['id']
            link['text'] = nrp['properties(r)']['label_zh']
            link['data'] = nrp['properties(r)']

            if link['text'] not in color_dict:
                color_dict[link['text']] = [color_list.pop(), link['to']]
            else:
                color_dict[link['text']].append(link['to'])  # 根据关系标签标记对应节点颜色

            if node_a not in nodes:
                nodes.append(node_a)
            if node_b not in nodes:
                nodes.append(node_b)
            links.append(link)

        node2color = {str(rootID): color_list.pop()}
        for node_type in color_dict:  # key：节点序号，value:颜色
            color = color_dict[node_type][0]
            for i in range(1, len(color_dict[node_type])):
                node2color[color_dict[node_type][i]] = color

        for node in nodes:
            try:
                color = node2color[node['id']]
                node['color'], node['borderColor'] = color
            except:
                pass

        import json
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump({'rootId': str(rootID), 'nodes': nodes, 'links': links}, f, ensure_ascii=False)

        return {'rootId': str(rootID), 'nodes': nodes, 'links': links}
