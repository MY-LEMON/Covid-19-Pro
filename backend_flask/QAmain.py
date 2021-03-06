from QAsearch import CovidGraph
from QAsystem import EntityExtractor


class KGQA:
    def __init__(self):
        self.extractor = EntityExtractor()
        self.searcher = CovidGraph()

    def qa_main(self, input_str):
        answer = [""]
        graph = [""]
        entities = self.extractor.extractor(input_str)
        if not entities:  # 无法辨别实体
            return answer, graph
        sqls = self.searcher.question_parser(entities)
        final_answer, node_relation = self.searcher.searching(sqls)
        if not final_answer:
            return answer, graph
        else:
            return final_answer, node_relation


if __name__ == "__main__":
    while True:
        handler = KGQA()
        question = input("用户：")
        if not question:
            break
        final_answer, node_relation = handler.qa_main(question)
        resData = {
            "resCode": 0,  # 非0即错误 1
            "data": [final_answer[0], node_relation[0]],  # 数据位置，一般为数组
            "message": '搜索结果'
        }
        print("——" * 50)
        import json

        with open("kg_data2front.json", "w", encoding='utf-8') as f:
            json.dump(resData, f, ensure_ascii=False)
