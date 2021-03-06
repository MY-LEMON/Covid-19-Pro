import re
from settings import *
import ahocorasick
import jieba
from gensim.models import KeyedVectors
import string
import joblib
import numpy as np


class EntityExtractor:
    def __init__(self):

        self.result = {}
        self.name_dict = ["Disease", "Alias", "Symptom", "Complication", "infectorname", "place", "date", "transport",
                          "hospital", "type"]

        # 所有词汇导入
        self.disease_path = data_dir + 'disease_vocab.txt'  # 所有疾病词汇
        self.symptom_path = data_dir + 'symptom_vocab.txt'
        self.alias_path = data_dir + 'alias_vocab.txt'
        self.complication_path = data_dir + 'complications_vocab.txt'

        self.infectorname_path = data_dir + 'gz_病例.txt'
        self.place_path = data_dir + 'gz_地点.txt'
        self.date_path = data_dir + 'gz_日期.txt'
        self.transport_path = data_dir + 'gz_入境方式.txt'
        self.hospital_path = data_dir + 'gz_医院.txt'
        self.type_path = data_dir + 'gz_症状.txt'

        # 构建领域词词库
        self.disease_entities = [w.strip() for w in open(self.disease_path, encoding='utf8') if w.strip()]
        self.symptom_entities = [w.strip() for w in open(self.symptom_path, encoding='utf8') if w.strip()]
        self.alias_entities = [w.strip() for w in open(self.alias_path, encoding='utf8') if w.strip()]
        self.complication_entities = [w.strip() for w in open(self.complication_path, encoding='utf8') if w.strip()]

        self.infectorname_entities = [w.strip() for w in open(self.infectorname_path, encoding='utf8') if w.strip()]
        self.place_entities = [w.strip() for w in open(self.place_path, encoding='utf8') if w.strip()]
        self.date_entities = [w.strip() for w in open(self.date_path, encoding='utf8') if w.strip()]
        self.transport_entities = [w.strip() for w in open(self.transport_path, encoding='utf8') if w.strip()]
        self.hospital_entities = [w.strip() for w in open(self.hospital_path, encoding='utf8') if w.strip()]
        self.type_entities = [w.strip() for w in open(self.type_path, encoding='utf8') if w.strip()]

        # 构建ac树加快查询
        self.disease_tree = self.build_actree(list(set(self.disease_entities)))
        self.alias_tree = self.build_actree(list(set(self.alias_entities)))
        self.symptom_tree = self.build_actree(list(set(self.symptom_entities)))
        self.complication_tree = self.build_actree(list(set(self.complication_entities)))

        self.infectorname_tree = self.build_actree(list(set(self.infectorname_entities)))
        self.place_tree = self.build_actree(list(set(self.place_entities)))
        self.date_tree = self.build_actree(list(set(self.date_entities)))
        self.transport_tree = self.build_actree(list(set(self.transport_entities)))
        self.hospital_tree = self.build_actree(list(set(self.hospital_entities)))
        self.type_tree = self.build_actree(list(set(self.type_entities)))

        # 训练模型
        self.vocab_path = data_dir + 'vocab.txt'  # 所有词汇
        self.word2vec_path = word2vec_dir  # 中文预训练词向量
        self.stopwords_path = data_dir + 'stop_words.utf8'
        self.stopwords = [w.strip() for w in open(self.stopwords_path, 'r', encoding='utf8') if w.strip()]  # 停词

        # 训练模型
        self.tfidf_path = data_dir + 'tfidf_model.m'
        self.nb_path = data_dir + 'intent_reg_model.m'
        self.tfidf_model = joblib.load(self.tfidf_path)
        self.nb_model = joblib.load(self.nb_path)

        # 问句词典
        self.symptom_qwds = ['什么症状', '哪些症状', '症状有哪些', '症状是什么', '什么表征', '哪些表征', '表征是什么',
                             '什么现象', '哪些现象', '现象有哪些', '症候', '什么表现', '哪些表现', '表现有哪些',
                             '什么行为', '哪些行为', '行为有哪些', '什么状况', '哪些状况', '状况有哪些', '现象是什么',
                             '表现是什么', '行为是什么', '症状']  # 询问症状
        self.cureway_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片', '吃什么药', '用什么药', '怎么办',
                             '买什么药', '怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治',
                             '医治方式', '疗法', '咋治', '咋办', '咋治', '治疗方法']  # 询问治疗方法
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时',
                              '几个小时', '多少年', '多久能好', '痊愈', '康复']  # 询问治疗周期
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例',
                              '可能性', '能治', '可治', '可以治', '可以医', '能治好吗', '可以治好吗', '会好吗',
                              '能好吗', '治愈吗']  # 询问治愈率
        self.check_qwds = ['检查什么', '检查项目', '哪些检查', '什么检查', '检查哪些', '项目', '检测什么',
                           '哪些检测', '检测哪些', '化验什么', '哪些化验', '化验哪些', '哪些体检', '怎么查找',
                           '如何查找', '怎么检查', '如何检查', '怎么检测', '如何检测']  # 询问检查项目
        self.belong_qwds = ['属于什么科', '什么科', '科室', '挂什么', '挂哪个', '哪个科', '哪些科']  # 询问科室
        self.disase_qwds = ['什么病', '啥病', '得了什么', '得了哪种', '怎么回事', '咋回事', '回事',
                            '什么情况', '什么问题', '什么毛病', '啥毛病', '哪种病']  # 询问疾病
        self.prevent_qwds = ['预防', '防治', '预防方法', '什么方法', '怎么预防', '怎么防治', '预防措施', '防治措施', '如何预防',
                             '如何防治', '怎样预防', '咋预防', '咋防治']
        self.route_qwds = ['传播途径', '途径', '方式', '怎么传播', '传播', '传播方式', '如何传播', '什么方式传播', '什么途径', '什么方式']
        self.cov_qwds = ['新型冠状病毒肺炎是什么', '新型冠状病毒肺炎是啥', '介绍新型冠状病毒肺炎', '了解新型冠状病毒肺炎']

        self.queryhos_qwds = ['哪家医院', '医院', '在哪就医', '送哪个医院', '在哪就诊', '就诊医院']  # 询问就诊地点
        self.querysp_qwds = ['从哪里出发', '从哪来', '从哪出发', '出发地', '境外输入地']  # 询问出发地点
        self.queryst_qwds = ['几号启程', '什么时候出发', '什么时候来', '几号的飞机', '什么时候离开', '何时离开']  # 询问出发时间
        self.queryep_qwds = ['在哪入境', '从哪进来', '在哪确诊', '飞到哪', '在哪']  # 询问入境地点
        self.queryet_qwds = ['几号到的', '什么时候到的', '何时到达', '何时入境', '什么时候入境', '几号入境']  # 询问入境时间
        self.querydef_qwds = ['有哪些确诊病例', '确诊的都有谁', '确诊了哪些人', '哪些病例被确诊']  # 询问确诊病例
        self.queryns_qwds = ['有哪些无症状感染者', '无症状感染者有哪些', '有哪些人被检测成无症状', '谁是无症状感染者']  # 询问无症状感染者
        self.queryway_qwsd = ['交通工具', '怎么进来', '如何入境', '何种方式入境', '航班号', '入境途径']  # 询问病例入境方式
        self.queryna_qwsd = ['是哪的人', '籍贯', '什么地方的人', '病例老家是哪', '哪里人']  # 询问病例籍贯

    def build_actree(self, wordlist):
        """
        构造actree，加速过滤
        :param wordlist:
        :return:
        """
        actree = ahocorasick.Automaton()
        # 向树中添加单词
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def editDistanceDP(self, s1, s2):
        """
        采用DP方法计算编辑距离，用于词向量计算余弦
        :param s1:
        :param s2:
        :return:
        """
        m = len(s1)
        n = len(s2)
        solution = [[0 for j in range(n + 1)] for i in range(m + 1)]
        for i in range(len(s2) + 1):
            solution[0][i] = i
        for i in range(len(s1) + 1):
            solution[i][0] = i

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    solution[i][j] = solution[i - 1][j - 1]
                else:
                    solution[i][j] = 1 + min(solution[i][j - 1], min(solution[i - 1][j],
                                                                     solution[i - 1][j - 1]))
        return solution[m][n]

    def simCal(self, word, entities, flag):
        """
        计算词语和字典中的词的相似度
        相同字符的个数/min(|A|,|B|) + 余弦相似度
        :param word: str
        :param entities:List
        :return:
        """
        a = len(word)
        scores = []
        for entity in entities:
            sim_num = 0
            b = len(entity)
            c = len(set(entity + word))
            temp = []
            for w in word:
                if w in entity:
                    sim_num += 1
            if sim_num != 0:
                score1 = sim_num / c  # overlap score
                temp.append(score1)
            try:
                score2 = self.model.similarity(word, entity)  # 余弦相似度分数
                temp.append(score2)
            except:
                pass
            score3 = 1 - self.editDistanceDP(word, entity) / (a + b)  # 编辑距离分数
            if score3:
                temp.append(score3)

            score = sum(temp) / len(temp)
            if score >= 0.7:
                scores.append((entity, score, flag))

        scores.sort(key=lambda k: k[1], reverse=True)
        return scores

    def find_sim_words(self, question):
        """
        当全匹配失败时，就采用相似度计算来找相似的词
        :param question:
        :return:
        """
        jieba.load_userdict(self.vocab_path)
        self.model = KeyedVectors.load_word2vec_format(self.word2vec_path, binary=False)

        sentence = re.sub("[{}]", re.escape(string.punctuation), question)
        sentence = re.sub("[，。‘’；：？、！【】]", " ", sentence)
        sentence = sentence.strip()

        words = [w.strip() for w in jieba.cut(sentence) if w.strip() not in self.stopwords and len(w.strip()) >= 2]

        alist = []

        for word in words:
            temp = [self.disease_entities, self.alias_entities, self.symptom_entities,
                    self.complication_entities]  # 待添加
            for i in range(len(temp)):
                flag = ''
                if i == 0:
                    flag = "Disease"
                elif i == 1:
                    flag = "Alias"
                elif i == 2:
                    flag = "Symptom"
                else:
                    flag = "Complication"
                scores = self.simCal(word, temp[i], flag)
                alist.extend(scores)
        temp1 = sorted(alist, key=lambda k: k[1], reverse=True)
        if temp1:
            self.result[temp1[0][2]] = [temp1[0][0]]

    def entity_reg(self, question):
        '''
        通过查询AC树，判别实体
        :param question:
        :return:
        '''

        ac_tree = [self.disease_tree, self.alias_tree, self.symptom_tree, self.complication_tree,
                   self.infectorname_tree, self.place_tree, self.date_tree, self.transport_tree, self.hospital_tree,
                   self.type_tree]
        for index in range(len(self.name_dict)):
            for i in ac_tree[index].iter(question):
                word = i[1][1]
                if self.name_dict[index] not in self.result:
                    self.result[self.name_dict[index]] = [word]
                else:
                    self.result[self.name_dict[index]].append(word)
        # if len(self.result['Disease']) > 1:
        #     self.result['Disease'] = self.result['Disease'][0]

        return self.result

    def tfidf_features(self, text, vectorizer):
        """
        提取问题的TF-IDF特征
        :param text:
        :param vectorizer:
        :return:
        """
        jieba.load_userdict(self.vocab_path)
        words = [w.strip() for w in jieba.cut(text) if w.strip() and w.strip() not in self.stopwords]
        sents = [' '.join(words)]

        tfidf = vectorizer.transform(sents).toarray()
        return tfidf

    def other_features(self, text):
        """
        提取问题的关键词特征
        :param text:
        :return:
        """
        features = [0] * 7
        for d in self.disase_qwds:
            if d in text:
                features[0] += 1

        for s in self.symptom_qwds:
            if s in text:
                features[1] += 1

        for c in self.cureway_qwds:
            if c in text:
                features[2] += 1

        for c in self.check_qwds:
            if c in text:
                features[3] += 1
        for p in self.lasttime_qwds:
            if p in text:
                features[4] += 1

        for r in self.cureprob_qwds:
            if r in text:
                features[5] += 1

        for d in self.route_qwds:
            if d in text:
                features[6] += 1

        m = max(features)
        n = min(features)
        normed_features = []
        if m == n:
            normed_features = features
        else:
            for i in features:
                j = (i - n) / (m - n)
                normed_features.append(j)

        return np.array(normed_features)

    def model_predict(self, x, model):
        """
        预测意图
        :param x:
        :param model:
        :return:
        """
        pred = model.predict(x)
        return pred

    def check_words(self, words, sent):
        """
        基于特征词分类
        :param words:
        :param sent:
        :return:
        """
        for wd in words:
            if wd in sent:
                return True
        return False

    def extractor(self, question):
        """
        识别实体、预测意图主函数
        :param question:
        :return:
        """
        self.entity_reg(question)
        # if not self.result:
        #     self.find_sim_words(question)

        types = []  # 实体类型
        for v in self.result.keys():
            types.append(v)

        intentions = []  # 查询意图

        tfidf_feature = self.tfidf_features(question, self.tfidf_model)
        other_feature = self.other_features(question)
        m = other_feature.shape
        other_feature = np.reshape(other_feature, (1, m[0]))

        feature = np.concatenate((tfidf_feature, other_feature), axis=1)

        predicted = self.model_predict(feature, self.nb_model)
        intentions.append(predicted[0])

        # 预测失败时删除错误结果，防止意图混淆
        intentions.clear()

        # 已知疾病，查询症状
        if self.check_words(self.symptom_qwds, question) and ('Disease' in types or 'Alia' in types):
            intention = "query_symptom"
            if intention not in intentions:
                intentions.append(intention)

        # 查询预防
        if self.check_words(self.prevent_qwds, question) and ('Disease' in types or 'Alia' in types):
            intention = "query_prevent"
            if intention not in intentions:
                intentions.append(intention)

        # 查询路线
        if self.check_words(self.route_qwds, question) and ('Disease' in types or 'Alia' in types):
            intention = "query_route"
            if intention not in intentions:
                intentions.append(intention)

        # 查询治疗方式
        if self.check_words(self.cureway_qwds, question) and ('Disease' in types or 'Alia' in types):
            intention = "query_cureway"
            if intention not in intentions:
                intentions.append(intention)

        # 查询属于
        if self.check_words(self.belong_qwds, question) and ('Disease' in types or 'Alia' in types):
            intention = "query_belong"
            if intention not in intentions:
                intentions.append(intention)

        # 查询疾病基本信息
        if self.check_words(self.cov_qwds, question) and ('Disease' in types or 'Alia' in types):
            intention = "query_cov"
            if intention not in intentions:
                intentions.append(intention)

        # 查询医院就诊
        if self.check_words(self.queryhos_qwds, question) and ('infectorname' in types):
            intention = "query_hospital"
            if intention not in intentions:
                intentions.append(intention)

        # 查询出发地
        if self.check_words(self.querysp_qwds, question) and ('infectorname' in types):
            intention = "query_sp"
            if intention not in intentions:
                intentions.append(intention)

        # 查询出发日期
        if self.check_words(self.querydef_qwds, question) and ('date' in types):
            intention = "query_def"
            if intention not in intentions:
                intentions.append(intention)


        """
        more
        """
        # 若没有识别出实体或意图则调用其它方法
        if not intentions or not types:
            intention = "QA_matching"
            if intention not in intentions:
                intentions.append(intention)

        self.result["intentions"] = intentions

        return self.result
